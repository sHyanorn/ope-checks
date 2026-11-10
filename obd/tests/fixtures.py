"""Small hand-built logs with known answers."""

import numpy as np
import pandas as pd

from obd import tables
from obd.data import FEATURES, WEEK_START_US


def log(rows):
    """A log as `data.read_log` returns it.

    Each row is a dict with `minute` (since the start of the week, may be
    fractional) and optionally `item`, `position`, `click`, `p`, `user` (the
    four user features, or one string for the first of them).
    """
    frame = pd.DataFrame(
        {
            "timestamp": [WEEK_START_US + round(row["minute"] * 60e6) for row in rows],
            "item_id": [row.get("item", 0) for row in rows],
            "position": [row.get("position", 1) for row in rows],
            "click": [row.get("click", 0) for row in rows],
            "propensity_score": [row.get("p", 0.5) for row in rows],
        }
    )
    users = [row.get("user", "a") for row in rows]
    users = [(user, "-", "-", "-") if isinstance(user, str) else user for user in users]
    for i, name in enumerate(FEATURES):
        frame[name] = pd.Categorical([user[i] for user in users])
    return frame


def rows(n, clicks=0, **row):
    """`n` identical rows, the first `clicks` of them clicked."""
    return [row | {"click": int(i < clicks)} for i in range(n)]


def campaign(random, bts, n_items=2, prior_mean=None):
    prior_mean = np.full(n_items, 0.5) if prior_mean is None else np.asarray(prior_mean)
    return tables.build(log(random), log(bts), prior_mean)
