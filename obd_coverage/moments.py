"""Second moments of the click model: the calibration and the predicted coverage (Section 5).

Nothing here generates a click. A quantity is linearised as a sum over rows of
a_i c_i minus a centring c_i, one `Part` per log; its variance follows from the
pair probabilities of Section 3.
"""

import math
from dataclasses import dataclass

import numpy as np

from obd.posthoc.units import MINUTE_US
from obd_coverage.model import N_STEPS, STEP, WEEK_MINUTES

Z = 1.959963984540054  # 97.5th percentile of the standard normal


@dataclass(frozen=True)
class Layout:
    """The rows of a log cut into atoms: the rows of one impression in one five-minute block."""

    atom: np.ndarray  # [row]
    impression: np.ndarray  # [atom]
    step: np.ndarray  # [atom]
    session: np.ndarray | None  # [atom]
    long: np.ndarray | None  # [atom]


def layout(log, groups=None):
    key, atom = np.unique(log.impression * N_STEPS + log.step, return_inverse=True)
    impression = key // N_STEPS
    session = None if groups is None else groups.session[impression]
    long = None if groups is None or groups.long is None else groups.long[session]
    return Layout(atom, impression, key % N_STEPS, session, long)


@dataclass(frozen=True)
class Part:
    x: np.ndarray  # [atom] sum of a q
    mean: np.ndarray  # [atom] sum of a q - centring: the expected contribution
    x2: float  # sum over rows of (a q)^2
    v0: float  # sum over rows of a^2 q (1 - q): the variance under independence
    rows_mean2: float  # sum over rows of (a q - centring)^2
    lay: Layout
    excess: tuple  # (e_I, e_S, e_L)


def part(lay, q, a, centring, excess=(0, 0, 0)):
    aq, n = a * q, len(lay.impression)
    return Part(
        x=np.bincount(lay.atom, aq, n),
        mean=np.bincount(lay.atom, aq - centring, n),
        x2=float((aq**2).sum()),
        v0=float((a * aq * (1 - q)).sum()),
        rows_mean2=float(((aq - centring) ** 2).sum()),
        lay=lay,
        excess=excess,
    )


def _squares(x, *ids):
    """Sum, over the sets of atoms that share every id, of the squared sum of x."""
    key = ids[0]
    for i in ids[1:]:
        key = key * (int(i.max()) + 1) + i
    return float((np.bincount(np.unique(key, return_inverse=True)[1], x) ** 2).sum())


def variance(p, unit=None):
    """Variance of the part's sum over each unit, added over the units.

    `unit[atom]` cuts the log into pieces whose sums are taken separately, so
    only pairs of rows inside one unit count. Without it the log is one unit.
    """
    ids = () if unit is None else (unit,)
    e_i, e_s, e_l = p.excess
    total, inner = p.v0, 0.0
    for e, group in ((e_i, p.lay.impression), (e_s, p.lay.session), (e_l, p.lay.long)):
        if not e:
            break
        pairs = _squares(p.x, group, *ids) - p.x2
        total += e * (pairs - inner)
        inner = pairs
    return total


def true_variance(parts):
    return sum(variance(p) for p in parts)


def bootstrap_variance(parts, unit):
    """Expected variance of the replicates under a resampling unit.

    `unit` is "rows", "impressions" (each log on its own) or a block length in
    minutes (the same blocks in every log).
    """
    if unit == "rows":
        return sum(p.v0 + p.rows_mean2 for p in parts)
    if unit == "impressions":
        return sum(
            variance(p, p.lay.impression)
            + float((np.bincount(p.lay.impression, p.mean) ** 2).sum())
            for p in parts
        )
    k = unit // STEP
    mean = sum(np.bincount(p.lay.step // k, p.mean, N_STEPS // k) for p in parts)
    return sum(variance(p, p.lay.step // k) for p in parts) + float((mean**2).sum())


def coverage(variance_ratio):
    """Coverage of a nominal 95% interval whose variance is `variance_ratio` times the true
    one and that is otherwise right (normal approximation)."""
    return math.erf(Z * math.sqrt(variance_ratio) / 2**0.5)


def predicted_coverage(parts, unit):
    return coverage(bootstrap_variance(parts, unit) / true_variance(parts))


def quantity_parts(random, bts, q_random, q_bts, lay_random, lay_bts, excess_random, excess_bts):
    """The parts of each quantity of Section 6, and their true values."""
    w = random.weight
    n_star, c_star = float((w * q_random).sum()), float(q_bts.sum())
    a = w / n_star
    r_rows = part(lay_random, q_random, a, np.full(len(w), 1 / len(w)), excess_random)
    r_weights = part(lay_random, q_random, a, w / w.sum(), excess_random)
    b = part(
        lay_bts,
        q_bts,
        np.full(len(q_bts), -1 / c_star),
        np.full(len(q_bts), -1 / len(q_bts)),
        excess_bts,
    )
    v_on, ips = c_star / len(q_bts), n_star / len(w)
    parts = {"ips_ratio": [r_rows, b], "snips_ratio": [r_weights, b], "ips": [r_rows], "v_on": [b]}
    truth = {
        "ips_ratio": ips / v_on,
        "snips_ratio": n_star / float(w.sum()) / v_on,
        "ips": ips,
        "v_on": v_on,
    }
    return parts, truth


def solve(target, numerator, denominator):
    """e with numerator(e) / denominator(e) = target, both linear in e, as (value at 0, at 1)."""
    (n0, n1), (d0, d1) = numerator, denominator
    return (target * d0 - n0) / ((n1 - n0) - target * (d1 - d0))


def variance_ratio_moments(log, q, session, e_i, minutes):
    """Expectations behind `obd.posthoc.units.variance_ratio` on one log.

    Returns the expected numerator and the expected denominator, each summed
    over the pairs of blocks that the statistic keeps and each as (value
    without sessions, value at e_S = 1); both are linear in e_S.
    """
    mu = np.bincount(log.impression, q)  # expected clicks of an impression
    s2 = np.bincount(log.impression, q**2)
    own = mu - s2 + e_i * (mu**2 - s2)  # variance of its clicks
    block = log.start // (minutes * MINUTE_US)
    n_blocks = WEEK_MINUTES // minutes
    g = np.bincount(block, minlength=n_blocks)
    n = np.bincount(block, log.size, n_blocks)

    def shared(x, unit, n_units):
        """By unit: the sum of x_g x_h over pairs of its impressions in one session."""
        _, cell = np.unique(session * n_units + unit, return_inverse=True)
        by_cell = np.bincount(cell, x)
        of_cell = np.zeros(len(by_cell), np.int64)
        of_cell[cell] = unit
        return np.bincount(of_cell, by_cell**2, n_units) - np.bincount(unit, x**2, n_units)

    with np.errstate(invalid="ignore", divide="ignore"):
        rate = np.bincount(block, mu, n_blocks) / n
        within = np.bincount(block, own, n_blocks) / n**2
        spread = np.bincount(block, (mu - rate[block] * log.size) ** 2, n_blocks) / n**2
        # The statistic estimates a block's variance from the spread of its impressions,
        # which misses what impressions of one session have in common.
        missed = shared(mu, block, n_blocks) / ((g - 1) * n**2)
        signed = np.where(block % 2 == 0, 1, -1) * mu / n[block]
    between = shared(signed, block // 2, n_blocks // 2)
    kept = (g.reshape(-1, 2) >= 2).all(axis=1)
    rate, within, spread, missed = (x.reshape(-1, 2)[kept] for x in (rate, within, spread, missed))
    numerator = float(((rate[:, 0] - rate[:, 1]) ** 2).sum() + within.sum())
    denominator = float(within.sum() + spread.sum())
    return (
        (numerator, numerator + float(between[kept].sum())),
        (denominator, denominator - float(missed.sum())),
    )
