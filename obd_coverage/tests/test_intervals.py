import numpy as np
import pytest

from obd.posthoc import blocks
from obd.posthoc.units import _unit_sums, resampled
from obd_coverage import model
from obd_coverage.intervals import QUANTITIES, UNITS, Resampler, quantities
from obd_coverage.tests import small

N = 300


def resampler(seed=0, n=N):
    logs, clicks, pi0 = small.logs(seed)
    return Resampler(*logs, np.random.default_rng(5), n), [np.flatnonzero(c) for c in clicks], pi0


def test_quantities():
    r, b = np.array([6.0, 4.0, 3.0]), np.array([10.0, 20.0])
    assert quantities(r, b) == pytest.approx([4, 3, 2, 0.5])
    assert QUANTITIES == ("ips_ratio", "snips_ratio", "ips", "v_on")
    assert UNITS == ("rows", "impressions", 5, 10, 20, 30, 60, 180)


def test_block_replicates_are_those_of_the_post_hoc_analysis():
    random, bts = small.frames(0)
    r, clicked, pi0 = resampler()
    stored = blocks.h3_by_length(random, bts, pi0, N)
    sums = r.sums(*clicked)
    for minutes in blocks.MINUTES:
        replicates = r.blocks(*sums, minutes)
        assert replicates[:, 0] == pytest.approx(stored[minutes][1]["ips"])
        assert replicates[:, 1] == pytest.approx(stored[minutes][1]["snips"])
    estimate, by_unit = r.replicates(*clicked, np.random.default_rng(0))
    assert estimate[:2] == pytest.approx([stored[10][0]["ips"], stored[10][0]["snips"]])
    assert by_unit.shape == (len(UNITS), N, len(QUANTITIES))


def reference(frames, pi0, unit, clicked, n):
    """Replicates from the sums of every unit, as the post hoc analysis draws them."""
    random, bts = frames
    w = len(pi0) * pi0[random["item_id"].to_numpy(), random["position"].to_numpy() - 1]
    click = [np.zeros(len(f)) for f in frames]
    for c, rows in zip(click, clicked, strict=True):
        c[rows] = 1
    rng = np.random.default_rng(9)
    r = resampled(_unit_sums(random, unit, (w * click[0], w, np.ones(len(w)))), rng, n)
    b = resampled(_unit_sums(bts, unit, (click[1], np.ones(len(bts)))), rng, n)
    return quantities(r, b)


@pytest.mark.parametrize("unit", ["rows", "impressions"])
def test_rows_and_impressions_spread_like_the_post_hoc_resamples(unit):
    r, clicked, pi0 = resampler(n=3000)
    ours = getattr(r, unit)(*clicked, np.random.default_rng(0))
    theirs = reference(small.frames(0), pi0, unit, clicked, 3000)
    assert ours.mean(axis=0) == pytest.approx(theirs.mean(axis=0), rel=0.01)
    assert ours.std(axis=0) == pytest.approx(theirs.std(axis=0), rel=0.06)


def test_impression_replicates_count_each_impression_as_often_as_the_plan_says():
    r, clicked, _ = resampler()
    times, fixed = r.plan()
    log = r.random
    assert (times.sum(axis=0) == len(log.size)).all()
    weight = np.bincount(log.impression, log.weight)
    assert fixed == pytest.approx(np.column_stack([times.T @ weight, times.T @ log.size]))
    ours = r.impressions(*clicked, np.random.default_rng(0))
    weighted = np.bincount(log.impression[clicked[0]], log.weight[clicked[0]], len(log.size))
    assert ours[:, 2] == pytest.approx((times.T @ weighted) / fixed[:, 1])


def test_clicks_that_come_together_widen_impressions_but_not_rows():
    logs, _, _ = small.logs(0)
    r = Resampler(*logs, np.random.default_rng(5), 2000)
    rng = np.random.default_rng(0)
    q = [np.full(len(log.t), 0.1) for log in logs]
    clicked = [
        model.draw(rng, x, log.impression, None, (6, 0, 0)) for log, x in zip(logs, q, strict=True)
    ]
    by_rows = r.rows(*clicked, rng).std(axis=0)
    by_impressions = r.impressions(*clicked, rng).std(axis=0)
    assert (by_impressions / by_rows)[3] == pytest.approx((1 + 2 * 0.1 * 6 / 0.9) ** 0.5, rel=0.08)
