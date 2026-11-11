"""Small synthetic logs for the tests. No real data."""

import numpy as np

from obd.posthoc import blocks
from obd.tests import synthetic
from obd_coverage import model

# Published numbers of the kind the calibration is solved from.
TARGET = {
    "impressions_over_rows": 1.05,
    "blocks_over_rows": 1.2,
    "variance_ratio": {log: {1: 1.02, 10: 1.1, 60: 1.1} for log in ("random", "bts")},
    "sd_over_ten_minutes": dict.fromkeys(blocks.MINUTES, 1.0) | {180: 1.04},
}


def frames(seed, n_random=6000, n_bts=30000, n_items=6):
    """A random and a BTS log in the layout of the released files, as loaded."""
    rng = np.random.default_rng(seed)
    policy = rng.dirichlet(np.ones(n_items), size=3)
    rate = rng.uniform(0.05, 0.15, n_items)
    return (
        synthetic.converted(synthetic.raw_log(rng, n_random, synthetic.uniform(n_items), rate)),
        synthetic.converted(synthetic.raw_log(rng, n_bts, policy, rate)),
    )


def logs(seed, **sizes):
    """The kept logs, their clicks, and a target for the random log's weights."""
    random, bts = frames(seed, **sizes)
    n_items = int(random["item_id"].max()) + 1
    pi0 = np.random.default_rng(seed + 1).dirichlet(np.ones(n_items), size=3).T
    kept = [model.kept(random, pi0), model.kept(bts)]
    return kept, [random["click"].to_numpy(), bts["click"].to_numpy()], pi0
