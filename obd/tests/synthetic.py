"""Synthetic logs in the layout of the released files. No real data.

    python -m obd.tests.synthetic DIR

writes logs of the size of the All campaign to DIR and times the full run on them.
"""

import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from obd import data, run
from obd.data import BLOCK_US, FEATURES, N_BLOCKS, WEEK_START_US, timestamps_us


def raw_log(rng, n_rows, policy, click_rate):
    """A log of impressions of three rows, one per position.

    `policy[k, a]` is the probability of item `a` at position `k + 1` and is
    recorded as the propensity; `click_rate[a]` is the click probability of
    item `a`. Rows of an impression share the user features and lie within a
    millisecond; impressions are spread uniformly over the week, unsorted.
    """
    n_impressions = -(-n_rows // 3)
    n_items = policy.shape[1]
    start = rng.integers(0, N_BLOCKS * BLOCK_US - 1000, n_impressions)
    item = np.stack([rng.choice(n_items, n_impressions, p=p) for p in policy], axis=1)
    values = np.array([f"{v:032x}" for v in range(4)])
    features = values[rng.integers(0, 4, (n_impressions, 4))]
    log = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                (WEEK_START_US + start[:, None] + 200 * np.arange(3)).ravel(), unit="us", utc=True
            ),
            "item_id": item.ravel(),
            "position": np.tile([1, 2, 3], n_impressions),
            "click": (rng.random(3 * n_impressions) < click_rate[item.ravel()]).astype(int),
            "propensity_score": policy[np.arange(3), item].ravel(),
        }
        | {name: np.repeat(features[:, i], 3) for i, name in enumerate(FEATURES)}
    )
    return log.iloc[:n_rows]


def uniform(n_items):
    return np.full((3, n_items), 1 / n_items)


def converted(raw):
    """A raw log as `data.read_log` returns it after conversion."""
    return raw.assign(timestamp=timestamps_us(raw["timestamp"])).astype(
        dict.fromkeys(FEATURES, "category")
    )


def write_archive(data_dir, campaigns, rng):
    """An archive and a prior file as `obd.run` reads them.

    `campaigns` maps a campaign to its number of items and its rows by policy.
    The BTS logs follow a policy that differs from the prior.
    """
    prior = {}
    with zipfile.ZipFile(data_dir / data.ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for campaign, (n_items, rows) in campaigns.items():
            prior[campaign] = {
                "alpha": rng.uniform(1, 50, n_items).tolist(),
                "beta": rng.uniform(1000, 5000, n_items).tolist(),
            }
            click_rate = rng.uniform(0.003, 0.007, n_items)
            policies = {"random": uniform(n_items), "bts": rng.dirichlet(np.full(n_items, 5.0), 3)}
            affinity = [f"user-item_affinity_{i}" for i in range(n_items)]
            for policy, n_rows in rows.items():
                member = f"open_bandit_dataset/{policy}/{campaign}/{campaign}.csv"
                with z.open(member, "w", force_zip64=True) as f:
                    for start in range(0, n_rows, 999_999):
                        chunk = raw_log(
                            rng, min(999_999, n_rows - start), policies[policy], click_rate
                        )
                        chunk.index += start
                        if start == 0:
                            f.write((",".join(["", *chunk.columns, *affinity]) + "\n").encode())
                        text = chunk.to_csv(header=False, lineterminator="\n")
                        f.write(text.replace("\n", ",0.0" * n_items + "\n").encode())
    (data_dir / data.PRIOR).write_text(yaml.safe_dump(prior))


if __name__ == "__main__":
    import resource

    directory = Path(sys.argv[1])
    sizes = {policy: data.ROWS[policy, "all"] for policy in ("random", "bts")}
    write_archive(directory, {"all": (80, sizes)}, np.random.default_rng(0))
    start = time.perf_counter()
    result = run.run(directory, ["all"])["all"]
    print(
        json.dumps(
            {
                "seconds": round(time.perf_counter() - start),
                "peak_rss_gb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20, 2),
                "h4": result["h4"],
                "h3.ips": result["quantities"]["h3.ips"],
            },
            indent=1,
        )
    )
