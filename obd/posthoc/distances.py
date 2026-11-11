"""Post hoc: distances between a target, the whole week and the hours of a log.

Reads the timestamp, item and position of a row and nothing else.
"""

import numpy as np

from obd import estimators as est
from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US

COLUMNS = ["timestamp", "item_id", "position"]


def rows_by_block(log, n_items):
    """Row counts by [ten-minute block, item, position]."""
    shape = (N_BLOCKS, n_items, 3)
    at = (
        (log["timestamp"].to_numpy() - WEEK_START_US) // BLOCK_US,
        log["item_id"].to_numpy(),
        log["position"].to_numpy() - 1,
    )
    return np.bincount(np.ravel_multi_index(at, shape), minlength=np.prod(shape)).reshape(shape)


def _by_position(p, q, rows):
    """TV(p, q) at each position, averaged with the positions' shares of `rows`."""
    return float((rows * est._tv(p, q, axis=0)).sum() / rows.sum())


def analyse(rows, target):
    """The distances of a log from rows[block, item, position] and target[item, position].

    `d`, `d0`, `left_out` and the distance of the first hour are those of H1.
    Alternate blocks are the first, third and fifth ten-minute block of an
    hour against the other three.
    """
    registered = est.h1(rows, target)
    even, odd = rows[0::2].sum(axis=0), rows[1::2].sum(axis=0)
    week = est._share(even + odd, 0)
    by_position = (even + odd).sum(axis=0)
    first = rows[:6]
    return {
        "d": registered["d"],
        "d0": registered["d0"],
        "left_out": registered["left_out"],
        "prior_to_week": _by_position(week, target, by_position),
        "prior_to_week_reference": _by_position(
            est._share(even, 0), est._share(odd, 0), by_position
        ),
        "hours_to_week": est.h1(rows, week)["d"],
        "first_hour": {
            "distance": registered["first_hour"],
            "floor": est._tv(
                est._share(first[0::2].sum(axis=0), 0), est._share(first[1::2].sum(axis=0), 0), 0
            ).tolist(),
            "rows": first.sum(axis=(0, 1)).tolist(),
        },
    }
