"""The logs on this study's side: reading, the files obp reads, ten-minute blocks.

Logs are read from the archive with `float_precision="round_trip"` (Section 3), which
pandas 3.1 no longer distinguishes from the default; `float_parsing` records the check.
"""

import io
import warnings
import zipfile

import numpy as np
import pandas as pd

from obd import data
from obd import estimators as obd_estimators
from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US

ROOT = "open_bandit_dataset"
SAMPLE = 100_000  # rows of a run of C1
FLOAT_PRECISION = "round_trip"  # Section 3


def member(policy, campaign, name=None):
    return f"{ROOT}/{policy}/{campaign}/{name or campaign + '.csv'}"


def chunks(data_dir, policy, campaign, columns, chunksize=2_000_000):
    """Chunks of one log, read from the archive."""
    with (
        zipfile.ZipFile(data_dir / data.ARCHIVE) as archive,
        archive.open(member(policy, campaign)) as f,
    ):
        yield from pd.read_csv(
            f, usecols=columns, float_precision=FLOAT_PRECISION, chunksize=chunksize
        )


def float_parsing():
    """How read_csv parses floats in this environment, for the provenance of the run."""
    rng = np.random.default_rng(0)
    n, m = 500_000, 300_000
    values = [rng.random(n), rng.random(n) * 1e-4, 1 / rng.integers(1, 10**6, n)]
    values = np.concatenate(values).tolist()
    strings = [repr(x) for x in values]
    strings += [f"{x:.17g}" for x in values[:m]] + [f"{x:.18f}" for x in values[:m]]
    expected = np.array([float(s) for s in strings])
    text = "x\n" + "\n".join(strings)
    differ, messages = {}, set()
    for mode in (None, "round_trip", "high"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            parsed = pd.read_csv(io.StringIO(text), float_precision=mode)["x"].to_numpy()
        differ[str(mode)] = int((parsed != expected).sum())
        messages.update(f"{type(w.message).__name__}: {w.message}" for w in caught)
    return {
        "float_precision_of_the_logs": FLOAT_PRECISION,
        "note": (
            "pandas deprecated float_precision in 3.1.0; since then every mode uses the same "
            "converter (read_csv documentation). The logs are read with "
            "float_precision='round_trip', as registered."
        ),
        "method": (
            "Parse with read_csv, with float_precision None, 'round_trip' and 'high', the repr "
            f"of {3 * n} draws of numpy default_rng(0) ({n} each of random(), random() * 1e-4 "
            f"and 1 / integers(1, 10**6)) and the first {m} of them with %.17g and with %.18f; "
            "count the values that differ from Python's float() of the same string."
        ),
        "n_strings": len(strings),
        "differ_from_float": differ,
        "warnings": sorted(messages),
    }


def extract(data_dir, out_dir, logs):
    """The files obp reads for each (policy, campaign) in `logs`, under out_dir/ROOT."""
    with zipfile.ZipFile(data_dir / data.ARCHIVE) as archive:
        for policy, campaign in logs:
            for name in (None, "item_context.csv"):
                archive.extract(member(policy, campaign, name), out_dir)
    return out_dir / ROOT


def blocks(timestamps):
    """The ten-minute block of each timestamp (ISO 8601 strings), numbered from 0."""
    block = (data.timestamps_us(timestamps).to_numpy() - WEEK_START_US) // BLOCK_US
    if not ((block >= 0) & (block < N_BLOCKS)).all():
        raise SystemExit("a row lies outside the week")
    return block


def tables(data_dir, policy, campaign, n_items):
    """Sums of one log by [block, item, position]: rows and clicks, and on the random
    log click/pscore and 1/pscore."""
    shape = (N_BLOCKS, n_items, 3)
    names = ["rows", "clicks"] + (["click_w", "w"] if policy == "random" else [])
    out = {name: np.zeros(np.prod(shape)) for name in names}
    columns = ["timestamp", "item_id", "position", "click", "propensity_score"]
    for chunk in chunks(data_dir, policy, campaign, columns):
        cell = np.ravel_multi_index(
            (blocks(chunk["timestamp"]), chunk["item_id"], chunk["position"] - 1), shape
        )
        click = chunk["click"].to_numpy().astype(float)
        w = 1 / chunk["propensity_score"].to_numpy()
        values = {"rows": None, "clicks": click, "click_w": click * w, "w": w}
        for name in names:
            out[name] += np.bincount(cell, values[name], len(out[name]))
    return {name: x.reshape(shape) for name, x in out.items()}


def on_policy_value(bts):
    """V_on, the mean click of the whole BTS log, from its tables."""
    return int(bts["clicks"].sum()) / int(bts["rows"].sum())


def blocks_per_run(campaign):
    """b of Section 7.1: blocks drawn in a run of the block arm of C1."""
    return round(N_BLOCKS * SAMPLE / data.ROWS["random", campaign])


def c1_multiplicities(campaign, t):
    """How often each block is drawn in run t of the block arm of C1 (Section 7.1)."""
    rng = np.random.default_rng([20261115, 0, data.CAMPAIGNS.index(campaign), t])
    return rng.multinomial(blocks_per_run(campaign), np.full(N_BLOCKS, 1 / N_BLOCKS))


c2_multiplicities = obd_estimators.multiplicities  # replicate i of Section 7.2
