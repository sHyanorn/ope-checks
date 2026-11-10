"""Post hoc: the ratios of H3 under three resampling units, and two measures of dependence."""

import numpy as np

from obd import estimators as est
from obd.data import BLOCK_US, FEATURES, N_BLOCKS, WEEK_START_US

UNITS = ("rows", "impressions", "blocks")  # the index is part of the random stream
BLOCK_MINUTES = (1, 10, 60)
MINUTE_US = 60_000_000


def impressions(log):
    """The impression of each row, numbered in time order.

    As in Section 7 of the registration: a maximal run of rows, in timestamp
    order, with the same user features, each less than a second after the one before.
    """
    t = log["timestamp"].to_numpy()
    order = np.argsort(t, kind="stable")
    user = log.groupby(FEATURES, observed=True).ngroup().to_numpy()[order]
    starts = np.r_[True, (user[1:] != user[:-1]) | (np.diff(t[order]) >= 1_000_000)]
    impression = np.empty(len(log), np.int64)
    impression[order] = np.cumsum(starts) - 1
    return impression


def _unit_sums(log, unit, columns):
    """Sums of each column over the rows of each resampling unit: [unit, column]."""
    if unit == "blocks":
        ids, n = (log["timestamp"].to_numpy() - WEEK_START_US) // BLOCK_US, N_BLOCKS
    else:
        ids = np.arange(len(log)) if unit == "rows" else impressions(log)
        n = ids.max() + 1
    return np.stack([np.bincount(ids, column, n) for column in columns], axis=1)


def resampled(units, rng, n_replicates):
    """Column sums of resamples, with replacement, of the rows of `units[unit, column]`.

    A sum depends only on how often each distinct row is drawn, and those counts
    are multinomial. Returns [replicate, column].
    """
    kinds, counts = np.unique(units, axis=0, return_counts=True)
    batch = max(1, 20_000_000 // len(kinds))
    return np.concatenate(
        [
            rng.multinomial(len(units), counts / len(units), min(batch, n_replicates - done))
            @ kinds
            for done in range(0, n_replicates, batch)
        ]
    )


def ratios(r, b):
    """IPS and SNIPS of the fixed-prior target over the on-policy value.

    `r[..., (weight x click, weight, rows)]` are sums over the random log and
    `b[..., (clicks, rows)]` over the BTS log.
    """
    v_on = b[..., 0] / b[..., 1]
    return {"ips": r[..., 0] / r[..., 2] / v_on, "snips": r[..., 0] / r[..., 1] / v_on}


def h3_by_unit(random, bts, pi0, stream, n_replicates=est.N_REPLICATES):
    """The two ratios of H3 with interval and standard deviation under each resampling unit.

    Rows and impressions are drawn in each log on its own. Blocks are the
    registered bootstrap: the same ten-minute blocks in both logs, with the
    registered multiplicities.
    """
    weight = len(pi0) * pi0[random["item_id"].to_numpy(), random["position"].to_numpy() - 1]
    logs = {
        "random": (random, (weight * random["click"].to_numpy(), weight, np.ones(len(random)))),
        "bts": (bts, (bts["click"].to_numpy(), np.ones(len(bts)))),
    }
    out = {}
    for u, unit in enumerate(UNITS):
        r, b = (_unit_sums(log, unit, columns) for log, columns in logs.values())
        if unit == "blocks":
            drawn = np.array([est.multiplicities(i) for i in range(n_replicates)])
            replicates = ratios(drawn @ r, drawn @ b)
        else:
            replicates = ratios(
                *(
                    resampled(x, np.random.default_rng([20261110, 2, stream, u, log]), n_replicates)
                    for log, x in enumerate((r, b))
                )
            )
        estimate = ratios(r.sum(axis=0), b.sum(axis=0))
        out[unit] = {"units": {"random": len(r), "bts": len(b)}} | {
            name: {
                "estimate": float(estimate[name]),
                "interval": np.percentile(replicates[name], [2.5, 97.5]).tolist(),
                "sd": float(replicates[name].std(ddof=1)),
            }
            for name in replicates
        }
    out["sd_of_blocks_over"] = {
        unit: {name: out["blocks"][name]["sd"] / out[unit][name]["sd"] for name in ("ips", "snips")}
        for unit in UNITS[:2]
    }
    return out


def list_reuse(log, impression):
    """How often a complete impression shows the same list as the complete impression before it.

    An impression is complete if it has exactly three rows holding positions
    1, 2 and 3 once each; its list is the three items in the order of the positions.
    """
    n = impression.max() + 1
    position = log["position"].to_numpy() - 1
    complete = (np.bincount(3 * impression + position, minlength=3 * n).reshape(n, 3) == 1).all(1)
    items = np.zeros((n, 3), np.int64)
    items[impression, position] = log["item_id"].to_numpy()
    lists = items[complete]
    return {
        "impressions": int(n),
        "complete_impressions": int(complete.sum()),
        "same_list_as_previous": float((lists[1:] == lists[:-1]).all(axis=1).mean()),
    }


def variance_ratio(start, clicks, rows, minutes, small_sample=True):
    """Variance of the difference in click rate between adjacent time blocks, over the
    variance it would have if impressions were independent.

    `start`, `clicks` and `rows` are, by impression, the time of the first row in
    microseconds since the start of the week, the sum of clicks and the number of
    rows. The week is cut into blocks of `minutes`, and the blocks are paired
    without overlap: the first with the second, the third with the fourth. The
    numerator sums the squared difference of the two click rates over the pairs.
    The denominator sums, over the same pairs, the two blocks' variance of a click
    rate with impressions as independent clusters: for a block of G impressions,
    G / (G - 1) times the sum over them of (clicks - rate x rows) squared, over
    the squared rows of the block. A pair with a block of fewer than two
    impressions is left out.

    Without `small_sample` the factor G / (G - 1) is dropped and only pairs with
    an empty block are left out. That ratio exceeds 1 for independent impressions
    when blocks hold few of them.
    """
    block = start // (minutes * MINUTE_US)
    n_blocks = N_BLOCKS * 10 // minutes
    g = np.bincount(block, minlength=n_blocks)
    n, total = np.bincount(block, rows, n_blocks), np.bincount(block, clicks, n_blocks)
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = total / n
        variance = np.bincount(block, (clicks - rate[block] * rows) ** 2, n_blocks) / n**2
        if small_sample:
            variance *= g / (g - 1)
    rate, variance = (x.reshape(-1, 2) for x in (rate, variance))
    kept = (g.reshape(-1, 2) >= (2 if small_sample else 1)).all(axis=1)
    return float(((rate[kept, 0] - rate[kept, 1]) ** 2).sum() / variance[kept].sum())


def dependence(log):
    """List reuse and the variance ratios of one log.

    The variance ratio is given for the clicks, for the clicks minus the click
    rate of their (item, position) in the log, and for the clicks without the
    small-sample factor.
    """
    impression = impressions(log)
    n = impression.max() + 1
    start = np.full(n, np.iinfo(np.int64).max)
    np.minimum.at(start, impression, log["timestamp"].to_numpy() - WEEK_START_US)
    click = log["click"].to_numpy()
    cell = 3 * log["item_id"].to_numpy().astype(np.int64) + log["position"].to_numpy() - 1
    with np.errstate(invalid="ignore"):  # cells without rows are not looked up
        residual = click - (np.bincount(cell, click) / np.bincount(cell))[cell]
    rows = np.bincount(impression)
    clicks, residuals = np.bincount(impression, click), np.bincount(impression, residual)
    return list_reuse(log, impression) | {
        "variance_ratio": {
            minutes: {
                "clicks": variance_ratio(start, clicks, rows, minutes),
                "residuals": variance_ratio(start, residuals, rows, minutes),
                "clicks_without_factor": variance_ratio(start, clicks, rows, minutes, False),
            }
            for minutes in BLOCK_MINUTES
        }
    }
