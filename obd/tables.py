"""Sums over the rows of a campaign's two logs, by ten-minute block.

Every estimator is a function of these tables, so a bootstrap replicate only
rescales them by the multiplicities of the blocks.
"""

from dataclasses import dataclass, fields, replace

import numpy as np
import pandas as pd

from obd.data import BLOCK_US, FEATURES, N_BLOCKS, WEEK_START_US

HOURS = N_BLOCKS // 6
P_MIN = 0.001  # eligibility bound of H2, low-propensity bound of H6


@dataclass(frozen=True)
class Tables:
    """`b_` is the BTS log, `r_` the random log, `x_` the exploratory item.

    Axes: block (ten minutes), half (five minutes within the block), item,
    position, user (combination of the four user features), side (0 at or
    below the cell's median of `x`, 1 above). `g_` arrays hold the rows of the
    random log by (block, item, position, user), one entry per group that has
    rows.
    """

    b_rows: np.ndarray  # [block, half, item, position]
    b_clicks: np.ndarray  # [block]
    b_inv_p: np.ndarray  # [block, item, position], sum of 1/propensity
    b_inv_p_clicks: np.ndarray  # [block], sum of click/propensity
    b_users: np.ndarray  # [block, user]
    r_rows: np.ndarray  # [block, half, item, position]
    r_clicks: np.ndarray  # [block, half, item, position]
    r_users: np.ndarray  # [block, user]
    x_rows: np.ndarray  # [block, item, position, side]
    x_clicks: np.ndarray  # [block, item, position, side]
    g_rows: np.ndarray  # [group]
    g_clicks: np.ndarray  # [group]
    g_block: np.ndarray  # [group], fixed
    g_cell: np.ndarray  # [group], flat index into [hour, item, position], fixed
    g_user: np.ndarray  # [group], fixed
    user_features: np.ndarray  # [user, feature], codes of the four features, fixed

    def resample(self, multiplicities):
        """The tables of logs in which the rows of block j count multiplicities[j] times."""
        scaled = {
            f.name: (getattr(self, f.name).T * multiplicities).T
            for f in fields(self)
            if f.name[:2] in ("b_", "r_", "x_")
        }
        by_group = multiplicities[self.g_block]
        return replace(
            self, **scaled, g_rows=self.g_rows * by_group, g_clicks=self.g_clicks * by_group
        )


def _sum(shape, index, weights=None):
    flat = np.ravel_multi_index(index, shape)
    return np.bincount(flat, weights, minlength=np.prod(shape)).reshape(shape)


def _in_week(log):
    since = log["timestamp"].to_numpy() - WEEK_START_US
    inside = (since >= 0) & (since < N_BLOCKS * BLOCK_US)
    return log[inside], int((~inside).sum())


def _index(log):
    """Block, half, item and position of each row."""
    since = log["timestamp"].to_numpy() - WEEK_START_US
    half = since % BLOCK_US // (BLOCK_US // 2)
    return since // BLOCK_US, half, log["item_id"].to_numpy(), log["position"].to_numpy() - 1


def _feature_codes(random, bts):
    """Codes of the four user features as written, for the rows of both logs, random first.

    Also, by feature, the value written differently in the two files if there is
    one: when exactly one value occurs only in the random log and exactly one
    only in the BTS log, their codes and what is reported about them.
    """
    codes, sizes, matches = [], [], []
    for name in FEATURES:
        values = pd.api.types.union_categoricals([random[name], bts[name]]).categories
        r, b = (pd.Categorical(log[name], categories=values).codes for log in (random, bts))
        r_share, b_share = (np.bincount(c, minlength=len(values)) / len(c) for c in (r, b))
        only_r = np.flatnonzero((r_share > 0) & (b_share == 0))
        only_b = np.flatnonzero((b_share > 0) & (r_share == 0))
        match = None
        if len(only_r) == len(only_b) == 1:
            report = {
                "random": values[only_r[0]],
                "bts": values[only_b[0]],
                "share_of_random_rows": r_share[only_r[0]],
                "share_of_bts_rows": b_share[only_b[0]],
            }
            match = (only_r[0], only_b[0], report)
        codes.append(np.concatenate([r, b]).astype(np.int64))
        sizes.append(len(values))
        matches.append(match)
    return np.stack(codes), sizes, matches


def _users(codes, sizes, n_random):
    """Codes of the combinations of user features: random rows, BTS rows, [user, feature]."""
    combinations, user = np.unique(np.ravel_multi_index(codes, sizes), return_inverse=True)
    return user[:n_random], user[n_random:], np.stack(np.unravel_index(combinations, sizes), axis=1)


def _context_sides(random, user, prior_mean):
    """Rows of complete impressions of the random log, and their side of the median of x.

    An impression is a maximal run of rows, in timestamp order, with the same
    user features, each less than a second after the one before.
    """
    order = np.argsort(random["timestamp"].to_numpy(), kind="stable")
    t, u = random["timestamp"].to_numpy()[order], user[order]
    item, position = random["item_id"].to_numpy()[order], random["position"].to_numpy()[order]
    starts = np.r_[True, (u[1:] != u[:-1]) | (t[1:] - t[:-1] >= 1_000_000)]
    impression = np.cumsum(starts) - 1
    n_impressions = impression[-1] + 1
    once_each = (_sum((n_impressions, 3), (impression, position - 1)) == 1).all(axis=1)
    rows = pd.DataFrame(
        {"row": order, "impression": impression, "item": item, "position": position}
    )[once_each[impression]]
    i, k = rows["impression"].to_numpy(), rows["position"].to_numpy() - 1
    mean = np.zeros((n_impressions, 3))  # prior mean of the item at each position
    mean[i, k] = prior_mean[rows["item"].to_numpy()]
    rows["x"] = (mean[i, (k + 1) % 3] + mean[i, (k + 2) % 3]) / 2
    rows["side"] = rows["x"] > rows.groupby(["item", "position"])["x"].transform("median")
    counts = {"impressions": int(n_impressions), "complete_impressions": int(once_each.sum())}
    return rows["row"].to_numpy(), rows["side"].to_numpy().astype(int), counts


def build(random, bts, prior_mean):
    """Tables of a campaign and facts of its full logs that are not resampled.

    `random` and `bts` are logs as returned by `data.read_log`; `prior_mean` is
    alpha / (alpha + beta) by item. Rows outside the week are counted and left out.
    """
    n_items = len(prior_mean)
    (random, r_outside), (bts, b_outside) = _in_week(random), _in_week(bts)
    codes, sizes, matches = _feature_codes(random, bts)
    written_r, written_b, written = _users(codes, sizes, len(random))
    for feature, match in zip(codes, matches, strict=True):
        if match:
            feature[feature == match[0]] = match[1]
    r_user, b_user, user_features = _users(codes, sizes, len(random))
    cells = (N_BLOCKS, 2, n_items, 3)

    b = _index(bts)
    b_click = bts["click"].to_numpy()
    p = bts["propensity_score"].to_numpy()
    inv_p, low = 1 / p, p < P_MIN
    on_grid = np.abs(200_000 * p - np.round(200_000 * p)) < 1e-4
    min_p = np.full((n_items, 3), np.inf)
    np.minimum.at(min_p, b[2:], p)

    r = _index(random)
    r_click = random["click"].to_numpy()
    groups, group = np.unique(
        np.ravel_multi_index(
            (r[0], r[2], r[3], r_user), (N_BLOCKS, n_items, 3, len(user_features))
        ),
        return_inverse=True,
    )
    g_block, g_item, g_position, g_user = np.unravel_index(
        groups, (N_BLOCKS, n_items, 3, len(user_features))
    )
    x_row, x_side, facts = _context_sides(random, r_user, prior_mean)
    x = (r[0][x_row], r[2][x_row], r[3][x_row], x_side)

    tables = Tables(
        b_rows=_sum(cells, b),
        b_clicks=np.bincount(b[0], b_click, N_BLOCKS),
        b_inv_p=_sum(cells[:1] + cells[2:], (b[0], *b[2:]), inv_p),
        b_inv_p_clicks=np.bincount(b[0], b_click * inv_p, N_BLOCKS),
        b_users=_sum((N_BLOCKS, len(user_features)), (b[0], b_user)),
        r_rows=_sum(cells, r),
        r_clicks=_sum(cells, r, r_click),
        r_users=_sum((N_BLOCKS, len(user_features)), (r[0], r_user)),
        x_rows=_sum((N_BLOCKS, n_items, 3, 2), x),
        x_clicks=_sum((N_BLOCKS, n_items, 3, 2), x, r_click[x_row]),
        g_rows=np.bincount(group),
        g_clicks=np.bincount(group, r_click),
        g_block=g_block,
        g_cell=np.ravel_multi_index((g_block // 6, g_item, g_position), (HOURS, n_items, 3)),
        g_user=g_user,
        user_features=user_features,
    )
    facts |= {
        "rows_outside_week": {"random": r_outside, "bts": b_outside},
        "user_values_matched": [match and match[2] for match in matches],
        "users_as_written": {  # rows by combination of values as written, [user]
            "random": np.bincount(written_r, minlength=len(written)),
            "bts": np.bincount(written_b, minlength=len(written)),
            "features": written,
        },
        "min_propensity": min_p,  # [item, position], inf where the cell has no row
        "rows_below_1e-5": int((p < 1e-5).sum()),
        "rows_off_grid": int((~on_grid).sum()),
        "sum_inv_p_squared": float((inv_p**2).sum()),
        "low_inv_p": float(inv_p[low].sum()),
        "low_inv_p_clicks": float((b_click * inv_p)[low].sum()),
    }
    return tables, facts
