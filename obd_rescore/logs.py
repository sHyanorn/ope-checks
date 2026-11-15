"""The logs on this study's side: reading, the files obp reads, ten-minute blocks.

Logs are read from the archive with `float_precision="round_trip"` (Section 3).
"""

import zipfile

import numpy as np
import pandas as pd

from obd import data
from obd import estimators as obd_estimators
from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US

ROOT = "open_bandit_dataset"
SAMPLE = 100_000  # rows of a run of C1


def member(policy, campaign, name=None):
    return f"{ROOT}/{policy}/{campaign}/{name or campaign + '.csv'}"


def chunks(data_dir, policy, campaign, columns, chunksize=2_000_000):
    """Chunks of one log, read from the archive."""
    with (
        zipfile.ZipFile(data_dir / data.ARCHIVE) as archive,
        archive.open(member(policy, campaign)) as f,
    ):
        yield from pd.read_csv(
            f, usecols=columns, float_precision="round_trip", chunksize=chunksize
        )


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
