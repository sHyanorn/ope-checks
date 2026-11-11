"""Replicates of the quantities under the eight resampling units (Section 6)."""

import numpy as np

from obd.posthoc import blocks
from obd.posthoc.units import ratios, resampled_kinds
from obd_coverage.model import N_STEPS, STEP

UNITS = ("rows", "impressions", *blocks.MINUTES)
QUANTITIES = ("ips_ratio", "snips_ratio", "ips", "v_on")
N_REPLICATES = 2000


def quantities(r, b):
    """The four quantities, on the last axis.

    `r[..., (weight x click, weight, rows)]` are sums over the random log and
    `b[..., (clicks, rows)]` over the BTS log, as for `obd.posthoc.units.ratios`.
    """
    both = ratios(r, b)
    return np.stack(
        [both["ips"], both["snips"], r[..., 0] / r[..., 2], b[..., 0] / b[..., 1]], axis=-1
    )


def _by_block(x, minutes):
    return x.reshape(-1, minutes // STEP, *x.shape[1:]).sum(axis=1)


class Resampler:
    """Everything about the replicates that does not depend on the clicks of a data set.

    `plan_rng` draws, once, how often each impression of the random log enters
    each replicate. Block multiplicities are those of `obd.posthoc.blocks`.
    """

    def __init__(self, random, bts, plan_rng, n_replicates=N_REPLICATES):
        self.random, self.bts, self.n = random, bts, n_replicates
        self.r_fixed = np.stack(
            [
                np.bincount(random.step, random.weight, N_STEPS),
                np.bincount(random.step, None, N_STEPS),
            ],
            axis=1,
        )
        self.b_rows = np.bincount(bts.step, minlength=N_STEPS).astype(float)
        self.drawn = {
            minutes: np.array(
                [blocks.multiplicities(minutes, i) for i in range(n_replicates)], dtype=float
            )
            for minutes in blocks.MINUTES
        }
        self.cell_weight = np.zeros(random.cell.max() + 1)
        self.cell_weight[random.cell] = random.weight
        self.cell_rows = np.bincount(random.cell)
        self.plan_rng, self._plan = plan_rng, None
        self.bts_sizes = int(bts.size.max()) + 1

    def plan(self):
        """How often each impression of the random log enters each replicate, as
        [impression, replicate], and the sums of weight and rows of each replicate."""
        if self._plan is None:
            size = self.random.size
            weight = np.bincount(self.random.impression, self.random.weight)
            times = np.empty((len(size), self.n), np.uint8)
            fixed = np.empty((self.n, 2))
            for i in range(self.n):
                drawn = np.bincount(
                    self.plan_rng.integers(len(size), size=len(size)), minlength=len(size)
                )
                times[:, i] = drawn
                fixed[i] = drawn @ weight, drawn @ size
            self._plan = times, fixed
        return self._plan

    def sums(self, r_clicked, b_clicked):
        """Sums by five-minute block of a data set: [step, 3] and [step, 2]."""
        r, b = self.random, self.bts
        weighted = np.bincount(r.step[r_clicked], r.weight[r_clicked], N_STEPS)
        clicks = np.bincount(b.step[b_clicked], minlength=N_STEPS)
        return (
            np.column_stack([weighted, self.r_fixed]),
            np.column_stack([clicks, self.b_rows]),
        )

    def blocks(self, r_sums, b_sums, minutes):
        drawn = self.drawn[minutes]
        return quantities(drawn @ _by_block(r_sums, minutes), drawn @ _by_block(b_sums, minutes))

    def rows(self, r_clicked, b_clicked, rng):
        r, b = self.random, self.bts
        clicks = np.bincount(r.cell[r_clicked], minlength=len(self.cell_rows))
        w = self.cell_weight
        kinds = np.concatenate(
            [np.column_stack([w, w, np.ones(len(w))]), np.column_stack([0 * w, w, np.ones(len(w))])]
        )
        counts = np.concatenate([clicks, self.cell_rows - clicks])
        r_sums = resampled_kinds(kinds, counts, rng, self.n)
        b_counts = np.array([len(b_clicked), len(b.t) - len(b_clicked)])
        b_sums = resampled_kinds(np.array([[1.0, 1.0], [0.0, 1.0]]), b_counts, rng, self.n)
        return quantities(r_sums, b_sums)

    def impressions(self, r_clicked, b_clicked, rng):
        r, b = self.random, self.bts
        weighted = np.bincount(r.impression[r_clicked], r.weight[r_clicked], len(r.size))
        hit = np.flatnonzero(weighted)
        times, fixed = self.plan()
        r_sums = np.column_stack([weighted[hit] @ times[hit], fixed])
        clicks = np.bincount(b.impression[b_clicked], minlength=len(b.size))
        count = np.bincount(clicks * self.bts_sizes + b.size)
        kind = np.flatnonzero(count)
        kinds = np.column_stack([kind // self.bts_sizes, kind % self.bts_sizes]).astype(float)
        return quantities(r_sums, resampled_kinds(kinds, count[kind], rng, self.n))

    def replicates(self, r_clicked, b_clicked, rng):
        """The estimates [quantity] and their replicates [unit, replicate, quantity].

        `rng` draws the replicates of rows (random log, then BTS log) and then
        of the impressions of the BTS log.
        """
        r_sums, b_sums = self.sums(r_clicked, b_clicked)
        by_unit = [
            self.rows(r_clicked, b_clicked, rng),
            self.impressions(r_clicked, b_clicked, rng),
        ]
        by_unit += [self.blocks(r_sums, b_sums, minutes) for minutes in blocks.MINUTES]
        return quantities(r_sums.sum(axis=0), b_sums.sum(axis=0)), np.stack(by_unit)
