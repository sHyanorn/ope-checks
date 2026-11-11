"""Direct measurements of the dependence among clicks (Section 2 of the extension).

Each takes the kept rows of a log and the rows clicked, real or simulated.
"""

from dataclasses import dataclass

import numpy as np

from obd.posthoc import blocks
from obd.posthoc.units import MINUTE_US
from obd_coverage.model import N_STEPS, STEP, WEEK_MINUTES

RATIO_MINUTES = (1, 2, 5, 10, 20, 30, 60, 180)
N_RESAMPLES = 2000
SUMS = ("v", "w", "v_random", "w_random", "v_bts", "w_bts", "between")


def clicks_by_impression(log, clicked):
    return np.bincount(log.impression[clicked], minlength=len(log.size))


def expected_pairs(log, q):
    """By impression: the sum of q_i q_j over its pairs of rows."""
    return (np.bincount(log.impression, q) ** 2 - np.bincount(log.impression, q**2)) / 2


def double_clicks(log, clicked):
    """By impression: the pairs of clicked rows."""
    k = clicks_by_impression(log, clicked)
    return k * (k - 1) / 2


def variance_ratio_terms(start, clicks, rows, minutes):
    """Numerator and denominator of `obd.posthoc.units.variance_ratio`, by pair of blocks kept."""
    block = start // (minutes * MINUTE_US)
    n_blocks = WEEK_MINUTES // minutes
    g = np.bincount(block, minlength=n_blocks)
    n, total = np.bincount(block, rows, n_blocks), np.bincount(block, clicks, n_blocks)
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = total / n
        spread = np.bincount(block, (clicks - rate[block] * rows) ** 2, n_blocks)
        variance = spread / n**2 * g / (g - 1)
    rate, variance = (x.reshape(-1, 2) for x in (rate, variance))
    kept = (g.reshape(-1, 2) >= 2).all(axis=1)
    return (rate[kept, 0] - rate[kept, 1]) ** 2, variance[kept].sum(axis=1)


def resampled_ratio(numerator, denominator, rng, n_resamples=N_RESAMPLES):
    """Percentile interval of sum(numerator) / sum(denominator) over resamples of the units.

    The contribution of a unit is computed once and drawn with the unit.
    """
    n = len(numerator)
    drawn = rng.multinomial(n, np.full(n, 1 / n), n_resamples)
    return np.percentile((drawn @ numerator) / (drawn @ denominator), [2.5, 97.5])


@dataclass(frozen=True)
class Typed:
    """What the residuals of a log need of its rows, apart from the clicks."""

    cell: np.ndarray  # [row] five-minute block x user type
    weight: np.ndarray  # [row]
    expected: np.ndarray  # [step, type] sum of weight x q


def typed(log, q):
    n_types = int(log.kind.max()) + 1
    cell = log.step * n_types + log.kind[log.impression]
    expected = np.bincount(cell, log.weight * q, N_STEPS * n_types)
    return Typed(cell, log.weight, expected.reshape(N_STEPS, n_types))


def residuals(of, clicked):
    """[step, type]: the weighted clicks minus what the type's own rate expects, over the
    weighted clicks of the log. The residuals of a type add to zero over the week."""
    got = np.bincount(of.cell[clicked], of.weight[clicked], of.expected.size)
    got = got.reshape(of.expected.shape)
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = np.nan_to_num(got.sum(axis=0) / of.expected.sum(axis=0))
    return (got - rate * of.expected) / got.sum()


def block_sums(random, bts, minutes):
    """The sums of squares of D3 at one block length, in the order of `SUMS`.

    `random` and `bts` are the residuals of the two logs. `v` sums the squared
    block residuals of the ratio, `w` the squared residuals by block, log and
    type; `between` is the product of the two logs' block residuals over the
    root of the product of their sums of squares.
    """
    by_type = [x.reshape(-1, minutes // STEP, x.shape[1]).sum(axis=1) for x in (random, bts)]
    r, b = (x.sum(axis=1) for x in by_type)
    w_r, w_b = (float((x**2).sum()) for x in by_type)
    v_r, v_b = float((r**2).sum()), float((b**2).sum())
    between = float((r * b).sum()) / (v_r * v_b) ** 0.5
    return float(((r - b) ** 2).sum()), w_r + w_b, v_r, w_r, v_b, w_b, between


def all_block_sums(of, clicked):
    """`block_sums` at every block length: [length, sum]. `of` and `clicked` by log."""
    random, bts = (residuals(x, rows) for x, rows in zip(of, clicked, strict=True))
    return np.array([block_sums(random, bts, minutes) for minutes in blocks.MINUTES])


def explanation(real, within, drift):
    """The label of Section 4 from the real G and the two ranges, each (low, high)."""
    if real > within[1] and real >= drift[0]:
        return "more like a drift"
    if real < drift[0] and real <= within[1]:
        return "more like dependence"
    return "not separated"
