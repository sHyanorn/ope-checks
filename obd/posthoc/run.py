"""Run the post hoc analyses.

    python -m obd.posthoc.run                    all three
    python -m obd.posthoc.run units features     some of them

Results go to obd/posthoc/results/<analysis>.json. The data directory is that of `obd.run`.
"""

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

from obd import data
from obd import estimators as est
from obd.posthoc import features, propensities, units

HERE = Path(__file__).parent
RESULTS = HERE / "results"
REGISTERED = HERE.parent / "results"


def load(data_dir, policy, campaign):
    """A log, converted if needed, without the rows outside the week."""
    log = data.read_log(data.to_parquet(data_dir, policy, campaign))
    since = log["timestamp"] - data.WEEK_START_US
    return log[(since >= 0) & (since < data.N_BLOCKS * data.BLOCK_US)]


def resampling_units(data_dir):
    out = {}
    for stream, campaign in enumerate(data.CAMPAIGNS):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        pi0 = est.fixed_prior_target(*data.read_prior(data_dir, campaign), stream)
        out[campaign] = {
            "h3": units.h3_by_unit(random, bts, pi0, stream),
            "dependence": {"random": units.dependence(random), "bts": units.dependence(bts)},
        }
    return out


def unmatched_features(data_dir):
    out = {}
    for campaign in ("all", "women"):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        found = features.one_log_values(random, bts)
        pairs = features.same_category(found)
        out[campaign] = found | {"taken_as_one_value": pairs}
        if not pairs:
            continue
        registered = json.loads((REGISTERED / f"{campaign}.json").read_text())["quantities"]
        post_hoc = features.quantities(
            features.rewritten(random, pairs),
            bts,
            *data.read_prior(data_dir, campaign),
            data.CAMPAIGNS.index(campaign),
        )
        moved = differing(registered, post_hoc)
        if moved:  # only H7 reads the user features
            raise SystemExit(f"{campaign}: differs from the registered result: {moved}")
        out[campaign]["h7"] = {
            name: {"registered": registered[name], "post_hoc": post_hoc[name]}
            for name in registered
            if name.startswith("h7.")
        }
    return out


def differing(registered, post_hoc):
    """The quantities outside H7 whose estimate or interval is not the registered one."""
    return [
        name
        for name in registered
        if not name.startswith("h7.")
        and not np.allclose(
            [post_hoc[name]["estimate"], *post_hoc[name]["interval"]],
            [registered[name]["estimate"], *registered[name]["interval"]],
            rtol=1e-9,
            atol=0,
            equal_nan=True,
        )
    ]


def propensity_identity(data_dir):
    return {
        campaign: propensities.analyse(
            load(data_dir, "bts", campaign), len(data.read_prior(data_dir, campaign)[0])
        )
        for campaign in data.CAMPAIGNS
    }


ANALYSES = {
    "units": resampling_units,
    "features": unmatched_features,
    "propensities": propensity_identity,
}


def _code_commit():
    """The commit of the code, marked if the code differs from it."""

    def git(*args):
        done = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, check=True)
        return done.stdout.strip()

    changed = git("status", "--porcelain", "--", ":(glob)../**/*.py")
    return git("rev-parse", "HEAD") + ("-dirty" if changed else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("analyses", nargs="*", choices=list(ANALYSES))
    parser.add_argument("--data-dir", type=Path, default=data.DEFAULT_DIR)
    args = parser.parse_args()
    data.fetch(args.data_dir)
    provenance = {
        "post_hoc": True,
        "code_commit": _code_commit(),
        "numpy": np.__version__,
        "replicates": est.N_REPLICATES,
        "command": " ".join(["python -m obd.posthoc.run", *args.analyses]),
    }
    RESULTS.mkdir(exist_ok=True)
    for name in args.analyses or ANALYSES:
        result = provenance | ANALYSES[name](args.data_dir)
        text = json.dumps(result, indent=1, default=lambda x: x.item())
        (RESULTS / f"{name}.json").write_text(text + "\n")
        print(f"wrote {RESULTS / name}.json")


if __name__ == "__main__":
    main()
