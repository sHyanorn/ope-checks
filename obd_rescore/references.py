"""The references of Section 6 and their intervals, from the tables of `logs`."""

import numpy as np

from obd_rescore import logs

N_INTERVAL_REPLICATES = 10_000  # obd Section 5


def applied(pi, target):
    """pi*[a, k], the probability that weights a row with item a at position k.

    `pi[a, k]` is the target's probability of item a at position k. Under the
    published target of C1 the row reads index j = k n_A + a of the published
    reshape, which holds pi(j div 3 | j mod 3) (Section 2.1).
    """
    if target == "own":
        return pi
    n_items = pi.shape[-2]
    j = np.arange(3) * n_items + np.arange(n_items)[:, None]
    return pi.reshape(*pi.shape[:-2], -1)[..., j]


def values(random, pi_star):
    """R_IPS and R_SNIPS of each target in pi_star[..., a, k], from the random log's tables."""
    click_w, w = random["click_w"].sum(axis=0), random["w"].sum(axis=0)
    weighted = (pi_star * click_w).sum(axis=(-2, -1))
    return {
        "r_ips": weighted / random["rows"].sum(),
        "r_snips": weighted / (pi_star * w).sum(axis=(-2, -1)),
    }


def intervals(random, bts, pi_star, n_replicates=N_INTERVAL_REPLICATES):
    """95% intervals of V_on, R_IPS, R_SNIPS and of the ratios to V_on over the replicates
    of obd Section 5, which draw blocks jointly in both logs."""
    by_block = {
        "rows": random["rows"].sum(axis=(1, 2)),
        "click_w": (random["click_w"] * pi_star).sum(axis=(1, 2)),
        "w": (random["w"] * pi_star).sum(axis=(1, 2)),
        "bts_rows": bts["rows"].sum(axis=(1, 2)),
        "bts_clicks": bts["clicks"].sum(axis=(1, 2)),
    }
    m = np.array([logs.c2_multiplicities(i) for i in range(n_replicates)], float)
    s = {name: m @ x for name, x in by_block.items()}
    replicates = {"v_on": s["bts_clicks"] / s["bts_rows"]}
    replicates["r_ips"] = s["click_w"] / s["rows"]
    replicates["r_snips"] = s["click_w"] / s["w"]
    replicates["r_ips_over_v_on"] = replicates["r_ips"] / replicates["v_on"]
    replicates["r_snips_over_v_on"] = replicates["r_snips"] / replicates["v_on"]
    return {
        name: [float(x) for x in np.percentile(r, [2.5, 97.5], method="linear")]
        for name, r in replicates.items()
    }
