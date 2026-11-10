"""Post hoc: the statistic S of H2 by cell, by eligibility bound and by day."""

import numpy as np

from obd import estimators as est
from obd import run
from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US

BOUNDS = (0.001, 0.0005, 0.0001)  # the registered bound of H2 and two lower ones
GRID = 200_000  # recorded propensities are multiples of 1 / GRID
DAYS = 7
LOW = (0.1, 0.5)  # hourly S under which a cell counts as nearly missing from the hour


def cell_sums(bts, n_items):
    """Sums over the BTS log by cell.

    `rows` and `inv_p` (sum of 1/propensity) by [block, item, position];
    `min_p` and `grid_bias` by [item, position]. `grid_bias` is the first-order
    upward bias of S if each recorded propensity is the share of GRID Monte
    Carlo draws: the sum of (1 - p) / (GRID p^2) over the rows of the cell, over
    the rows of its position.
    """
    block = (bts["timestamp"].to_numpy() - WEEK_START_US) // BLOCK_US
    item, position = bts["item_id"].to_numpy(), bts["position"].to_numpy() - 1
    p = bts["propensity_score"].to_numpy()
    shape = (N_BLOCKS, n_items, 3)
    flat = np.ravel_multi_index((block, item, position), shape)
    rows = np.bincount(flat, minlength=np.prod(shape)).reshape(shape)
    min_p = np.full(shape[1:], np.inf)
    np.minimum.at(min_p, (item, position), p)
    cell = 3 * item.astype(np.int64) + position
    excess = np.bincount(cell, (1 - p) / (GRID * p**2), 3 * n_items).reshape(shape[1:])
    with np.errstate(invalid="ignore"):  # undefined for a position without rows
        grid_bias = excess / rows.sum(axis=(0, 1))
    return {
        "rows": rows,
        "inv_p": np.bincount(flat, 1 / p, np.prod(shape)).reshape(shape),
        "min_p": min_p,
        "grid_bias": grid_bias,
    }


def statistic(inv_p, rows, multiplicities):
    """S by [replicate, item, position] in logs where block j counts multiplicities[:, j] times."""
    by_position = np.tensordot(multiplicities, rows.sum(axis=1), 1)
    with np.errstate(invalid="ignore"):  # undefined for a position without rows
        return np.tensordot(multiplicities, inv_p, 1) / by_position[:, None, :]


def mean_s(inv_p, rows, cells, multiplicities, blocks=slice(None)):
    """M, the mean of S over `cells[item, position]`, from the blocks given, with its interval."""
    inv_p, rows, multiplicities = inv_p[blocks], rows[blocks], multiplicities[:, blocks]
    estimate = statistic(inv_p, rows, np.ones((1, len(rows))))[0, cells].mean()
    replicates = statistic(inv_p, rows, multiplicities)[:, cells].mean(axis=1)
    return run.summarise(estimate, replicates)


def hourly(x):
    """[block, ...] to [hour, ...]."""
    return x.reshape(-1, 6, *x.shape[1:]).sum(axis=1)


def low_hours(inv_p, rows, below):
    """The hours in which a cell is shown far less often than its recorded propensities imply.

    From sums by [hour, item, position]. The hourly S of a cell is its sum of
    1/propensity in the hour over the rows of its position in the hour. Returns,
    by [hour, item, position], whether it is under `below`, and the part of
    1 - S that the hour then accounts for: its share of the position's rows
    times (1 - hourly S).
    """
    by_position = rows.sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore"):  # undefined for a position without rows
        s = inv_p / by_position
        low = s < below
        shortfall = np.where(low, by_position / by_position.sum(axis=0) * (1 - s), 0.0)
    return low, shortfall


def analyse(bts, n_items, n_replicates=est.N_REPLICATES):
    """S by cell, and M with rough sizes of the two biases of Section 8 at each bound.

    Intervals come from the registered multiplicities of the ten-minute blocks.
    """
    sums = cell_sums(bts, n_items)
    rows, inv_p, min_p = sums["rows"], sums["inv_p"], sums["min_p"]
    multiplicities = np.array([est.multiplicities(i) for i in range(n_replicates)])
    s = statistic(inv_p, rows, np.ones((1, N_BLOCKS)))[0]
    hourly_rows, hourly_inv_p = hourly(rows), hourly(inv_p)
    lows = {below: low_hours(hourly_inv_p, hourly_rows, below) for below in LOW}
    day = N_BLOCKS // DAYS

    def in_low_hours(item, k, below):
        hours = lows[below][0][:, item, k]
        cell_rows = hourly_rows[hours, item, k].sum()
        return {
            "hours": int(hours.sum()),
            "rows": int(cell_rows),
            "rows_of_position": int(hourly_rows[hours, :, k].sum()),
            "harmonic_mean_propensity": float(cell_rows / hourly_inv_p[hours, item, k].sum())
            if cell_rows
            else None,
            "shortfall": float(lows[below][1][:, item, k].sum()),
        }

    by_bound = {}
    for bound in BOUNDS:
        cells = np.isfinite(min_p) & (min_p >= bound)
        by_bound[bound] = {
            "cells": int(cells.sum()),
            "share_of_rows": float(rows.sum(axis=0)[cells].sum() / rows.sum()),
            "m": mean_s(inv_p, rows, cells, multiplicities),
            "m_by_day": [
                mean_s(inv_p, rows, cells, multiplicities, slice(d * day, (d + 1) * day))
                for d in range(DAYS)
            ],
            "grid_bias": float(sums["grid_bias"][cells].mean()),
            "shortfall_in_low_hours": {
                below: {
                    "mean": float(shortfall[:, cells].sum(axis=0).mean()),
                    "by_day": shortfall[:, cells]
                    .reshape(DAYS, 24, -1)
                    .sum(axis=1)
                    .mean(axis=1)
                    .tolist(),
                }
                for below, (_, shortfall) in lows.items()
            },
        }
    return {
        "by_bound": by_bound,
        "cells": [
            {
                "item": int(item),
                "position": int(k + 1),
                "rows": int(rows[:, item, k].sum()),
                "min_propensity": float(min_p[item, k]),
                "s": float(s[item, k]),
                "grid_bias": float(sums["grid_bias"][item, k]),
                "low_hours": {below: in_low_hours(item, k, below) for below in LOW},
            }
            for item, k in zip(*np.nonzero(np.isfinite(min_p) & (min_p >= BOUNDS[-1])), strict=True)
        ],
    }
