"""The estimators of the pre-registration, as functions of the block tables.

`estimate` returns every bootstrapped quantity. Called on `tables.resample(m)`
it returns the same quantities for a replicate, so that frequencies, counts,
coverage, fallbacks and the on-policy value are all recomputed there.
"""

import numpy as np

from obd.data import N_BLOCKS
from obd.tables import HOURS, P_MIN

M = 5  # minimum rows of the random log in a cell of H4
WIDTHS = (1, 3, 6, 24)  # hours
WEEK = HOURS
N_REPLICATES = 10_000
N_DRAWS = 1_000_000


def multiplicities(i):
    """How often each ten-minute block is drawn in replicate i (Section 5)."""
    rng = np.random.default_rng([20261110, 0, i])
    return rng.multinomial(N_BLOCKS, np.full(N_BLOCKS, 1 / N_BLOCKS))


def fixed_prior_target(alpha, beta, stream):
    """pi0[item, position]: how often an item ranks first, second, third (Section 5)."""
    n_items = len(alpha)
    draws = np.random.default_rng([20261110, 1, stream]).beta(alpha, beta, size=(N_DRAWS, n_items))
    counts = np.zeros((n_items, 3))
    for part in np.array_split(draws, 20):
        top = np.argsort(-part, axis=1)[:, :3]
        for position in range(3):
            counts[:, position] += np.bincount(top[:, position], minlength=n_items)
    return counts / N_DRAWS


def _share(x, axis=None):
    """x over its sum along `axis`; zero where the sum is zero."""
    total = x.sum(axis=axis, keepdims=True)
    return np.divide(x, total, out=np.zeros(x.shape), where=total > 0)


def _tv(p, q, axis=None):
    return 0.5 * np.abs(p - q).sum(axis=axis)


def hours(x):
    """[block, half, item, position] to [hour, item, position]."""
    return x.reshape(HOURS, -1, *x.shape[2:]).sum(axis=1)


def _periods(x, width):
    """[hour, ...] to [period, ...] for periods of `width` hours."""
    return x.reshape(-1, width, *x.shape[1:]).sum(axis=1)


def _shift(x, by):
    """x moved `by` steps along the first axis, zeros moving in."""
    out = np.zeros_like(x)
    if by > 0:
        out[by:] = x[:-by]
    else:
        out[:by] = x[-by:]
    return out


def h1(rows, target):
    """D and D0 of H1 from rows[block, item, position] and target[item, position]."""
    halves = rows.reshape(HOURS, 3, 2, *rows.shape[1:]).sum(axis=1)
    even, odd = halves[:, 0], halves[:, 1]  # the first, third, fifth block; the others
    hour = even + odd
    weight = hour.sum(axis=1) * ((even.sum(axis=1) > 0) & (odd.sum(axis=1) > 0))
    distance = _tv(_share(hour, 1), target, axis=1)
    floor = _tv(_share(even, 1), _share(odd, 1), axis=1)
    return {
        "d": float((weight * distance).sum() / weight.sum()),
        "d0": float((weight * floor).sum() / weight.sum()),
        "left_out": float(1 - weight.sum() / rows.sum()),
        "first_hour": distance[0].tolist(),
    }


def eligible_cells(min_propensity):
    """Cells of H2: at least one row, and none with a propensity below P_MIN."""
    return np.isfinite(min_propensity) & (min_propensity >= P_MIN)


def matched(b, r, rc, width, rv=None, rvc=None):
    """V_M of H4 and the share of BTS rows resolved at each level.

    `b`, `r`, `rc` are BTS rows, random rows and random clicks by [hour, item,
    position]. A cell takes the click rate of the narrowest level, from `width`
    up to the week, that holds at least M random rows of its item and position.
    Cells with fewer in the week are dropped, under the key "dropped". With
    `rv` and `rvc`, sums of user weights and of weight times click, the click
    rate is weighted wherever the weights do not sum to zero (H7).
    """
    cells = _periods(b, width)
    rate = np.zeros(cells.shape)
    open_ = np.ones(cells.shape, bool)
    shares = {}
    for level in (w for w in (*WIDTHS, WEEK) if w >= width):
        n, clicks = (np.repeat(_periods(x, level), level // width, axis=0) for x in (r, rc))
        hit = open_ & (n >= M)
        if rv is not None:
            weight, weighted = (
                np.repeat(_periods(x, level), level // width, axis=0) for x in (rv, rvc)
            )
            n, clicks = np.where(weight > 0, weight, n), np.where(weight > 0, weighted, clicks)
        rate[hit] = clicks[hit] / n[hit]
        shares[level] = cells[hit].sum() / cells.sum()
        open_ &= ~hit
    shares["dropped"] = cells[open_].sum() / cells.sum()
    kept = cells[~open_].sum()
    return ((cells * rate).sum() / kept if kept else np.nan), shares


def choose_width(b, r):
    """The width of H4 and the coverage C(W) of every width, from hourly rows."""
    coverage = {}
    for width in WIDTHS:
        cells = _periods(b, width)
        covered = cells[_periods(r, width) >= M].sum()
        coverage[width] = (covered / cells.sum(), 100 * covered >= 99 * cells.sum())  # tau = 0.99
    width = next((w for w in WIDTHS if coverage[w][1]), 24)
    return width, {w: c for w, (c, _) in coverage.items()}


def windowed(target, r, rc, weight, keep=True):
    """IPS on the random log against BTS frequencies taken from a window.

    `target[unit, item, position]` holds the BTS rows of the window of each
    time unit; `r` and `rc` hold the random rows and clicks of the unit;
    `weight[group, position]` the BTS rows of each group of consecutive units
    (an hour, or the unit itself). Rows of a unit whose window is empty, or
    where `keep[unit, position]` is false, are left out; so is a group left
    without rows. Returns the estimate and the share of random rows left out.
    """
    n_items = target.shape[1]
    has = (target.sum(axis=1) > 0) & keep
    total = n_items * (_share(target, 1) * rc).sum(axis=1) * has
    rows = r.sum(axis=1) * has
    total, rows = (x.reshape(len(weight), -1, 3).sum(axis=1) for x in (total, rows))
    kept = rows > 0
    estimate = (weight[kept] * total[kept] / rows[kept]).sum() / weight[kept].sum()
    return estimate, 1 - rows.sum() / r.sum()


def user_distances(users_p, users_q, hours_p, hours_q, features):
    """TV distances of H7 between two sets of rows.

    One for each user feature, one for their combinations ("joint") and one for
    the shares of rows by hour, from rows by [user] and by [hour].
    """
    p, q = _share(users_p), _share(users_q)
    out = {
        f"feature_{i}": _tv(np.bincount(codes, p), np.bincount(codes, q))
        for i, codes in enumerate(features.T)
    }
    return out | {"joint": _tv(p, q), "hours": _tv(_share(hours_p), _share(hours_q))}


def between_alternate_blocks(users, rows, features):
    """The distances of H7 between the even and the odd ten-minute blocks of one log.

    `users[block, user]` and `rows[block]` are row counts.
    """
    by_hour = rows.reshape(HOURS, 3, 2).sum(axis=1)
    return user_distances(
        users[0::2].sum(axis=0), users[1::2].sum(axis=0), by_hour[:, 0], by_hour[:, 1], features
    )


def estimate(t, pi0, width, eligible):
    """Every bootstrapped quantity of a campaign, by name.

    `pi0`, the H4 `width` and the `eligible` cells of H2 are fixed on the full
    data. A quantity that cannot be computed is nan.
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        return _estimate(t, pi0, width, eligible)


def _estimate(t, pi0, width, eligible):
    n_items = len(pi0)
    b, r, rc = hours(t.b_rows), hours(t.r_rows), hours(t.r_clicks)
    n_b, n_r = b.sum(), r.sum()
    v_on = t.b_clicks.sum() / n_b
    out = {"v_on": v_on}

    s = t.b_inv_p.sum(axis=0) / b.sum(axis=(0, 1))
    out |= {
        f"h2.s.{item}.{k + 1}": s[item, k] for item, k in zip(*np.nonzero(eligible), strict=False)
    }
    out["h2.m"] = s[eligible].mean() if eligible.any() else np.nan

    def ips(target):
        """IPS, SNIPS and the mean weight on the random log for target[item, position]."""
        w = n_items * target
        clicks, weights = (w * rc.sum(axis=0)).sum(), (w * r.sum(axis=0)).sum()
        return clicks / n_r, clicks / weights, weights / n_r

    ips_prior, snips_prior, mean_weight = ips(pi0)
    out |= {
        "h3.ips": ips_prior / v_on,
        "h3.snips": snips_prior / v_on,
        "h3.mean_weight": mean_weight,
    }

    for w in WIDTHS:
        v_m, shares = matched(b, r, rc, w)
        out |= {
            f"h4.rho.{w}": v_m / v_on,
            f"h4.d.{w}": v_m / v_on - out["h3.ips"],
            f"h4.rho_minus_snips.{w}": v_m / v_on - out["h3.snips"],
        }
        out |= {f"h4.share.{w}.{level}": share for level, share in shares.items()}
    pb, pr, prc = (_periods(x, width) for x in (b, r, rc))
    out["h4.ips_form"] = windowed(pb, pr, prc, pb.sum(axis=1))[0] / v_on
    out["h4.ips_week"] = ips(_share(b.sum(axis=0), 0))[0] / v_on

    def quarters(x):
        return x.reshape(4 * HOURS, 3, *x.shape[2:]).sum(axis=1)

    hour_weight = b.sum(axis=1)
    before, after = _shift(b, 1), _shift(b, -1)
    both = (before.sum(axis=1) > 0) & (after.sum(axis=1) > 0)
    windows = {
        "before_15": windowed(
            _shift(quarters(t.b_rows), 1), quarters(t.r_rows), quarters(t.r_clicks), hour_weight
        ),
        "before": windowed(before, r, rc, hour_weight),
        "after": windowed(after, r, rc, hour_weight),
    }
    paired_before, left_out = windowed(before, r, rc, hour_weight, both)
    paired_after, _ = windowed(after, r, rc, hour_weight, both)
    windows["after_minus_before"] = (paired_after - paired_before, left_out)
    for name, (value, left_out) in windows.items():
        out[f"h5.{name}"] = value / v_on
        out[f"h5.left_out.{name}"] = left_out

    click_rate_r = rc.sum() / n_r
    out |= {
        "h6.ips": t.b_inv_p_clicks.sum() / n_items / n_b / click_rate_r,
        "h6.snips": t.b_inv_p_clicks.sum() / t.b_inv_p.sum() / click_rate_r,
    }

    users_b, users_r = _share(t.b_users.sum(axis=0)), _share(t.r_users.sum(axis=0))
    distances = user_distances(
        users_b, users_r, b.sum(axis=(1, 2)), r.sum(axis=(1, 2)), t.user_features
    )
    out |= {f"h7.tv.{name}": distance for name, distance in distances.items()}
    out["h7.absent"] = users_b[users_r == 0].sum()
    v = np.divide(users_b, users_r, out=np.zeros(len(users_b)), where=users_r > 0)[t.g_user]
    rv = np.bincount(t.g_cell, t.g_rows * v, minlength=b.size).reshape(b.shape)
    rvc = np.bincount(t.g_cell, t.g_clicks * v, minlength=b.size).reshape(b.shape)
    out["h7.rho_change"] = matched(b, r, rc, width, rv, rvc)[0] / v_on - out[f"h4.rho.{width}"]

    n, clicks = t.x_rows.sum(axis=0), t.x_clicks.sum(axis=0)
    two_sided = (n > 0).all(axis=-1)
    rates = clicks[two_sided] / n[two_sided]
    weight = n[two_sided].sum(axis=1)
    difference = (weight * (rates[:, 1] - rates[:, 0])).sum() / weight.sum()
    out["exploratory"] = difference / (clicks.sum() / n.sum())
    return out
