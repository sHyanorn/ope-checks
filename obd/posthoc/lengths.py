"""Post hoc: the intervals behind the labels of H4, H5 and H6 by block length."""

import math

import numpy as np

from obd import estimators as est
from obd.data import WEEK_START_US
from obd.posthoc.blocks import MINUTES, REGISTERED, WEEK_MINUTES, multiplicities
from obd.posthoc.units import MINUTE_US
from obd.tables import HOURS

STEP = 5  # minutes: the shortest block, and a divisor of every length
POOLED = ("h3.ips", "h4.rho", "h4.d")  # the registration pools H3 and H4 only


def sums(random, bts, n_items):
    """Sums over the rows of each five-minute clock interval of the week.

    `r_rows`, `r_clicks` and `b_rows` by [step, item, position]; clicks of the
    BTS log, its 1/propensity and its click/propensity by [step].
    """

    def index(log):
        step = (log["timestamp"].to_numpy() - WEEK_START_US) // (STEP * MINUTE_US)
        return step, log["item_id"].to_numpy(), log["position"].to_numpy() - 1

    def cells(at, weights=None):
        shape = (WEEK_MINUTES // STEP, n_items, 3)
        flat = np.ravel_multi_index(at, shape)
        return np.bincount(flat, weights, minlength=math.prod(shape)).reshape(shape)

    r, b = index(random), index(bts)
    click, inv_p = bts["click"].to_numpy(), 1 / bts["propensity_score"].to_numpy()
    return {
        "r_rows": cells(r),
        "r_clicks": cells(r, random["click"].to_numpy()),
        "b_rows": cells(b),
        "b_clicks": np.bincount(b[0], click, WEEK_MINUTES // STEP),
        "b_inv_p": np.bincount(b[0], inv_p, WEEK_MINUTES // STEP),
        "b_inv_p_clicks": np.bincount(b[0], click * inv_p, WEEK_MINUTES // STEP),
    }


def quantities(s, pi0, width):
    """The quantities by name, from sums over equal clock intervals of an hour or less.

    As `est.estimate` computes them: the IPS ratio of H3, `rho` and `d` of H4
    at `width`, the difference (iii) minus (ii) of H5, the two ratios of H6.
    """
    b, r, rc = (
        s[name].reshape(HOURS, -1, *pi0.shape).sum(axis=1)
        for name in ("b_rows", "r_rows", "r_clicks")
    )
    n_items = len(pi0)
    v_on = s["b_clicks"].sum() / b.sum()
    click_rate_r = rc.sum() / r.sum()
    ips = (n_items * pi0 * rc.sum(axis=0)).sum() / r.sum() / v_on
    rho = est.matched(b, r, rc, width)[0] / v_on
    before, after = est._shift(b, 1), est._shift(b, -1)
    both = (before.sum(axis=1) > 0) & (after.sum(axis=1) > 0)
    hour_weight = b.sum(axis=1)
    paired = [est.windowed(target, r, rc, hour_weight, both)[0] for target in (after, before)]
    weighted_clicks = s["b_inv_p_clicks"].sum()
    return {
        "h3.ips": ips,
        "h4.rho": rho,
        "h4.d": rho - ips,
        "h5.after_minus_before": (paired[0] - paired[1]) / v_on,
        "h6.ips": weighted_clicks / n_items / b.sum() / click_rate_r,
        "h6.snips": weighted_clicks / s["b_inv_p"].sum() / click_rate_r,
    }


def by_length(random, bts, pi0, width, n_replicates=est.N_REPLICATES):
    """The quantities at each block length: {minutes: (estimate, replicates)}.

    A replicate draws as many blocks as the week holds, the same blocks in both
    logs, with the multiplicities of `blocks`. `estimate` and `replicates` map
    the names of `quantities` to a number and to an array over the replicates.
    """
    fine = sums(random, bts, len(pi0))
    out = {}
    with np.errstate(divide="ignore", invalid="ignore"):
        estimate = quantities(fine, pi0, width)
        for minutes in MINUTES:
            unit = math.gcd(minutes, 60)  # blocks are scaled as wholes; hours stay intact
            s = {
                name: x.reshape(-1, unit // STEP, *x.shape[1:]).sum(axis=1)
                for name, x in fine.items()
            }
            replicates = []
            for i in range(n_replicates):
                drawn = np.repeat(multiplicities(minutes, i), minutes // unit)
                scaled = {name: (x.T * drawn).T for name, x in s.items()}
                replicates.append(list(quantities(scaled, pi0, width).values()))
            out[minutes] = (estimate, dict(zip(estimate, np.array(replicates).T, strict=True)))
    return out


def pooled(by_campaign, weights):
    """The weighted sum of campaigns for the pooled quantities, replicate by replicate."""
    return {
        minutes: tuple(
            {
                name: sum(w * by_campaign[c][minutes][part][name] for c, w in weights.items())
                for name in POOLED
            }
            for part in (0, 1)
        )
        for minutes in MINUTES
    }


def summarise(by_length):
    """Interval and standard deviation of each quantity at each length, over the
    replicates in which it is defined; the latter also over the one at ten minutes."""
    defined = {
        minutes: {name: x[np.isfinite(x)] for name, x in replicates.items()}
        for minutes, (_, replicates) in by_length.items()
    }
    return {
        minutes: {
            name: {
                "estimate": float(estimate[name]),
                "interval": np.percentile(defined[minutes][name], [2.5, 97.5]).tolist(),
                "sd": float(defined[minutes][name].std(ddof=1)),
                "sd_over_ten_minutes": float(
                    defined[minutes][name].std(ddof=1) / defined[REGISTERED][name].std(ddof=1)
                ),
                "undefined_replicates": len(replicates[name]) - len(defined[minutes][name]),
            }
            for name in replicates
        }
        for minutes, (estimate, replicates) in by_length.items()
    }
