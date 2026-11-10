"""Post hoc: the ratios of H3 with clock blocks of several lengths as resampling units."""

import numpy as np

from obd import estimators as est
from obd.data import BLOCK_US, N_BLOCKS, WEEK_START_US
from obd.posthoc.units import MINUTE_US, ratios

MINUTES = (5, 10, 20, 30, 60, 180)  # the length is part of the random stream
REGISTERED = BLOCK_US // MINUTE_US
WEEK_MINUTES = N_BLOCKS * REGISTERED


def multiplicities(minutes, i):
    """How often each block of `minutes` is drawn in replicate i.

    At the registered length these are the registered multiplicities.
    """
    if minutes == REGISTERED:
        return est.multiplicities(i)
    n = WEEK_MINUTES // minutes
    return np.random.default_rng([20261110, 3, minutes, i]).multinomial(n, np.full(n, 1 / n))


def block_sums(random, bts, pi0, minutes):
    """Sums over the rows of each block of `minutes`, counted from the start of the week.

    Random log: [block, (weight x click, weight, rows)], with the weights of the
    fixed-prior target. BTS log: [block, (clicks, rows)].
    """

    def sums(log, columns):
        block = (log["timestamp"].to_numpy() - WEEK_START_US) // (minutes * MINUTE_US)
        return np.stack(
            [np.bincount(block, column, WEEK_MINUTES // minutes) for column in columns], axis=1
        )

    weight = len(pi0) * pi0[random["item_id"].to_numpy(), random["position"].to_numpy() - 1]
    return (
        sums(random, (weight * random["click"].to_numpy(), weight, np.ones(len(random)))),
        sums(bts, (bts["click"].to_numpy(), np.ones(len(bts)))),
    )


def h3_by_length(random, bts, pi0, n_replicates=est.N_REPLICATES):
    """The two ratios of H3 at each block length: {minutes: (estimate, replicates)}.

    A replicate draws as many blocks as the week holds, the same blocks in both
    logs. `estimate` and `replicates` map "ips" and "snips" to a number and to
    an array over the replicates.
    """
    out = {}
    for minutes in MINUTES:
        r, b = block_sums(random, bts, pi0, minutes)
        drawn = np.array([multiplicities(minutes, i) for i in range(n_replicates)])
        out[minutes] = (ratios(r.sum(axis=0), b.sum(axis=0)), ratios(drawn @ r, drawn @ b))
    return out


def pooled(by_campaign, weights):
    """The weighted sum of campaigns, replicate by replicate, in the form of `h3_by_length`."""
    return {
        minutes: tuple(
            {
                name: sum(w * by_campaign[c][minutes][part][name] for c, w in weights.items())
                for name in ("ips", "snips")
            }
            for part in (0, 1)
        )
        for minutes in MINUTES
    }


def summarise(by_length):
    """Interval and standard deviation of each ratio at each length, the latter also
    over the one at the registered length."""
    sd = {
        minutes: {name: float(x.std(ddof=1)) for name, x in replicates.items()}
        for minutes, (_, replicates) in by_length.items()
    }
    return {
        minutes: {"blocks": WEEK_MINUTES // minutes}
        | {
            name: {
                "estimate": float(estimate[name]),
                "interval": np.percentile(replicates[name], [2.5, 97.5]).tolist(),
                "sd": sd[minutes][name],
                "sd_over_ten_minutes": sd[minutes][name] / sd[REGISTERED][name],
            }
            for name in replicates
        }
        for minutes, (estimate, replicates) in by_length.items()
    }
