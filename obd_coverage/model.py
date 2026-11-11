"""The kept rows of a log, the synthetic groupings and the click model (Sections 2 to 4)."""

from dataclasses import dataclass

import numpy as np

from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US
from obd.posthoc.units import MINUTE_US, impressions

STEP = 5  # minutes: the shortest block, a divisor of every block length
WEEK_MINUTES = N_BLOCKS * BLOCK_US // MINUTE_US
N_STEPS = WEEK_MINUTES // STEP
HOURS = WEEK_MINUTES // 60
SESSION_SIZE = 5.5  # impressions, Section 3
SESSIONS_PER_LONG_GROUP = 3
SPANS = (1, 2, 3, 5, 10)  # minutes: the session spans tried in the calibration


@dataclass(frozen=True)
class Log:
    """The rows of one log inside the week. Clicks are not part of it."""

    t: np.ndarray  # [row] microseconds since the start of the week
    step: np.ndarray  # [row] five-minute block
    cell: np.ndarray  # [row] 3 x item + position - 1
    weight: np.ndarray  # [row] n_items x pi0(item | position), or 1 where no target applies
    impression: np.ndarray  # [row]
    start: np.ndarray  # [impression] time of its first row
    size: np.ndarray  # [impression] number of rows


def kept(frame, pi0=None):
    """The kept part of a log as `obd.posthoc.run.load` returns it.

    With `pi0[item, position]` the rows carry the weights of the fixed-prior
    target against the uniform policy; without it, weights of 1.
    """
    t = frame["timestamp"].to_numpy() - WEEK_START_US
    item, position = frame["item_id"].to_numpy(), frame["position"].to_numpy() - 1
    impression = impressions(frame)
    start = np.full(impression.max() + 1, np.iinfo(np.int64).max)
    np.minimum.at(start, impression, t)
    return Log(
        t=t,
        step=t // (STEP * MINUTE_US),
        cell=3 * item.astype(np.int64) + position,
        weight=np.ones(len(t)) if pi0 is None else len(pi0) * pi0[item, position],
        impression=impression,
        start=start,
        size=np.bincount(impression),
    )


@dataclass(frozen=True)
class Groups:
    session: np.ndarray  # [impression]
    long: np.ndarray | None  # [session]


def groupings(start, minutes, long_minutes, rng):
    """Sessions of span `minutes` and, with `long_minutes`, long groups of that span.

    The draws for the sessions come first, so the sessions do not depend on
    whether long groups follow.
    """
    span = minutes * MINUTE_US
    n_labels = max(1, round(len(start) * minutes / WEEK_MINUTES / SESSION_SIZE))
    label = rng.integers(n_labels, size=len(start))
    offset = rng.integers(span, size=n_labels)
    window = (start + offset[label]) // span
    n_windows = WEEK_MINUTES // minutes + 1
    keys, session = np.unique(label * n_windows + window, return_inverse=True)
    if not long_minutes:
        return Groups(session, None)
    label, window = keys // n_windows, keys % n_windows
    per_group = long_minutes // minutes
    n_sub = max(1, round(per_group / SESSIONS_PER_LONG_GROUP))
    sub = rng.integers(n_sub, size=len(keys))
    shift = rng.integers(per_group, size=(n_labels, n_sub))
    period = (window + shift[label, sub]) // per_group
    key = (label * n_sub + sub) * (n_windows // per_group + 2) + period
    return Groups(session, np.unique(key, return_inverse=True)[1])


def on_probabilities(excess):
    """Of a long group, a session and an impression, for excesses (e_I, e_S, e_L)."""
    e_i, e_s, e_l = excess
    if not 0 <= e_l <= e_s <= e_i:
        raise ValueError(f"excesses must satisfy 0 <= e_L <= e_S <= e_I, got {excess}")
    return 1 / (1 + e_l), (1 + e_l) / (1 + e_s), (1 + e_s) / (1 + e_i)


def draw(rng, q, impression, groups, excess):
    """The rows clicked in one data set.

    `q[row]` is the marginal click probability. Two rows are both clicked with
    probability q_i q_j (1 + e): e is `excess[0]` in one impression, `excess[1]`
    in one session, `excess[2]` in one long group, and 0 otherwise.
    """
    if not any(excess):
        return np.flatnonzero(rng.random(len(q)) < q)
    if (1 + excess[0]) * q.max() > 1:
        raise ValueError("the excess within an impression is more than the click rates allow")
    p_long, p_session, p_impression = on_probabilities(excess)
    on = rng.random(impression.max() + 1) < p_impression
    if excess[1]:
        session_on = rng.random(groups.session.max() + 1) < p_session
        if excess[2]:
            session_on &= (rng.random(groups.long.max() + 1) < p_long)[groups.long]
        on &= session_on[groups.session]
    rows = np.flatnonzero(on[impression])
    return rows[rng.random(len(rows)) < q[rows] * (1 + excess[0])]


def cell_rates(logs, clicks, n_cells):
    """Click rate by cell over several logs together."""
    rows = sum(np.bincount(log.cell, minlength=n_cells) for log in logs)
    clicked = sum(np.bincount(log.cell, c, n_cells) for log, c in zip(logs, clicks, strict=True))
    return clicked / rows


def fitted_drift(logs, clicks, rate):
    """`m` at the midpoint of each clock hour (scenario D), before scaling.

    Day d times hour of day h: each is the clicks of the logs in it over the
    sum of `rate[cell]` over their rows.
    """
    hour = [log.t // (60 * MINUTE_US) for log in logs]
    clicked = sum(np.bincount(h, c, HOURS) for h, c in zip(hour, clicks, strict=True))
    expected = sum(np.bincount(h, rate[log.cell], HOURS) for h, log in zip(hour, logs, strict=True))
    clicked, expected = clicked.reshape(-1, 24), expected.reshape(-1, 24)
    day = clicked.sum(axis=1) / expected.sum(axis=1)
    hour_of_day = clicked.sum(axis=0) / expected.sum(axis=0)
    return np.outer(day, hour_of_day).ravel()


def drift(t, by_hour):
    """`m(t)`: linear between the midpoints of the clock hours, constant outside them."""
    return np.interp(t / (60 * MINUTE_US), np.arange(HOURS) + 0.5, by_hour)
