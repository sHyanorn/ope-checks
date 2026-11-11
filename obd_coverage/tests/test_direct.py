import numpy as np
import pytest

from obd.posthoc import blocks
from obd.posthoc.units import MINUTE_US, variance_ratio
from obd_coverage import direct, model
from obd_coverage.tests import small


def log_of(impression, kind=None, start=None, weight=None):
    """A log of which only the impressions, their kinds, times and weights matter."""
    impression = np.asarray(impression)
    n = impression.max() + 1
    start = np.zeros(n, np.int64) if start is None else np.asarray(start)
    return model.Log(
        t=start[impression],
        step=start[impression] // (model.STEP * MINUTE_US),
        cell=np.zeros(len(impression), np.int64),
        weight=np.ones(len(impression)) if weight is None else np.asarray(weight, float),
        impression=impression,
        start=start,
        size=np.bincount(impression),
        kind=np.zeros(n, np.int64) if kind is None else np.asarray(kind),
    )


def test_double_clicks_and_the_pairs_expected_of_independent_rows():
    log = log_of([0, 0, 0, 1, 1, 2])
    q = np.array([0.1, 0.2, 0.3, 0.5, 0.5, 0.9])
    assert direct.double_clicks(log, np.array([0, 1, 2, 3])).tolist() == [3, 0, 0]
    assert direct.double_clicks(log, np.array([0, 2, 3, 4, 5])).tolist() == [1, 1, 0]
    expected = [0.1 * 0.2 + 0.1 * 0.3 + 0.2 * 0.3, 0.25, 0]
    assert direct.expected_pairs(log, q) == pytest.approx(expected)


def test_the_excess_of_double_clicks_estimates_the_excess_of_the_model():
    rng = np.random.default_rng(0)
    log = log_of(np.repeat(np.arange(200_000), 3))
    q = rng.uniform(0.02, 0.1, 600_000)
    for e in (0, 4):
        clicked = model.draw(rng, q, log.impression, None, (e, 0, 0))
        pairs = direct.double_clicks(log, clicked).sum()
        assert pairs / direct.expected_pairs(log, q).sum() - 1 == pytest.approx(e, abs=0.2)


def test_the_terms_of_the_variance_ratio_add_up_to_the_published_statistic():
    (random, _), clicks, _ = small.logs(0, n_random=60_000)
    by_impression = np.bincount(random.impression, clicks[0])
    for minutes in direct.RATIO_MINUTES:
        numerator, denominator = direct.variance_ratio_terms(
            random.start, by_impression, random.size, minutes
        )
        assert len(numerator) == len(denominator) <= 10080 // minutes // 2
        expected = variance_ratio(random.start, by_impression, random.size, minutes)
        assert numerator.sum() / denominator.sum() == pytest.approx(expected, rel=1e-12)


def test_a_resampled_ratio_is_drawn_with_whole_units():
    rng = np.random.default_rng(0)
    denominator = rng.uniform(1, 2, 500)
    assert direct.resampled_ratio(3 * denominator, denominator, rng) == pytest.approx([3, 3])
    numerator = denominator * rng.normal(1, 0.5, 500)
    low, high = direct.resampled_ratio(numerator, denominator, np.random.default_rng(1))
    ratio = numerator.sum() / denominator.sum()
    assert low < ratio < high
    assert high - low == pytest.approx(4 * 0.5 / 500**0.5, rel=0.3)
    again = direct.resampled_ratio(numerator, denominator, np.random.default_rng(1))
    assert (again == [low, high]).all()


def test_residuals_of_a_type_add_to_zero_and_carry_the_weights():
    rng = np.random.default_rng(0)
    n = 5000
    start = np.sort(rng.integers(0, 10080 * MINUTE_US, n))
    log = log_of(np.arange(n), rng.integers(0, 3, n), start, rng.uniform(0.5, 2, n))
    q = np.full(n, 0.2)
    of = direct.typed(log, q)
    clicked = np.flatnonzero(rng.random(n) < np.where(log.kind == 0, 0.4, 0.1))
    residual = direct.residuals(of, clicked)
    assert residual.shape == (model.N_STEPS, 3)
    assert residual.sum(axis=0) == pytest.approx(0, abs=1e-12)
    one = np.flatnonzero((log.step == log.step[clicked[0]]) & (log.kind == log.kind[clicked[0]]))
    rate = log.weight[clicked][log.kind[clicked] == log.kind[one[0]]].sum() / (
        0.2 * log.weight[log.kind == log.kind[one[0]]].sum()
    )
    got = log.weight[np.intersect1d(one, clicked)].sum() - rate * 0.2 * log.weight[one].sum()
    cell = residual[log.step[one[0]], log.kind[one[0]]]
    assert cell == pytest.approx(got / log.weight[clicked].sum())


def sums_over_data_sets(logs, q, groups, excess, n=60, seed=0):
    rng = np.random.default_rng(seed)
    of = [direct.typed(log, np.full(len(log.t), 0.1)) for log in logs]
    total = 0
    for _ in range(n):
        clicked = [
            model.draw(rng, p, log.impression, g, excess)
            for log, p, g in zip(logs, q, groups, strict=True)
        ]
        total = total + direct.all_block_sums(of, clicked)
    named = dict(zip(direct.SUMS, total.T, strict=True))
    return named | {"g": 1 - named["w"] / named["v"]}


@pytest.fixture(scope="module")
def typed_logs():
    logs, _, _ = small.logs(0, n_random=40_000, n_bts=200_000)
    return logs, [np.full(len(log.t), 0.1) for log in logs]


def test_independent_clicks_leave_nothing_between_types_or_logs(typed_logs):
    logs, q = typed_logs
    sums = sums_over_data_sets(logs, q, (None, None), (0, 0, 0))
    assert sums["g"] == pytest.approx(0, abs=0.03)
    assert sums["v"] == pytest.approx(sums["v_random"] + sums["v_bts"], rel=0.05)


def test_dependence_within_types_widens_the_blocks_and_leaves_the_share_at_zero(typed_logs):
    logs, q = typed_logs
    groups = [
        model.groupings(log.start, 10, 1440, np.random.default_rng(1), kind=log.kind)
        for log in logs
    ]
    independent = sums_over_data_sets(logs, q, (None, None), (0, 0, 0))
    dependent = sums_over_data_sets(logs, q, groups, (4, 4, 4))
    last = blocks.MINUTES.index(180)
    assert dependent["v"][last] > 1.5 * independent["v"][last]
    assert dependent["g"] == pytest.approx(0, abs=0.05)


def test_a_drift_in_one_log_shows_between_types_and_more_so_in_long_blocks(typed_logs):
    logs, q = typed_logs
    hour = logs[1].t // (60 * MINUTE_US)
    moved = [q[0], q[1] * (1 + 0.6 * np.sin(2 * np.pi * hour / 24))]
    sums = sums_over_data_sets(logs, moved, (None, None), (0, 0, 0))
    ten, last = blocks.MINUTES.index(10), blocks.MINUTES.index(180)
    assert sums["g"][last] > 0.5 > sums["g"][ten] > 0.03
    assert 1 - sums["w_bts"][last] / sums["v_bts"][last] > 0.9
    assert 1 - sums["w_random"][last] / sums["v_random"][last] == pytest.approx(0, abs=0.05)


def test_a_drift_that_both_logs_share_leaves_the_ratio(typed_logs):
    logs, q = typed_logs
    moved = [
        p * (1 + 0.6 * np.sin(2 * np.pi * (log.t // (60 * MINUTE_US)) / 24))
        for log, p in zip(logs, q, strict=True)
    ]
    sums = sums_over_data_sets(logs, moved, (None, None), (0, 0, 0))
    last = blocks.MINUTES.index(180)
    assert 1 - sums["w_bts"][last] / sums["v_bts"][last] > 0.9
    assert sums["between"][last] / 60 > 0.5
    assert sums["g"][last] < 0.15


def test_the_label_of_an_explanation():
    within, drift = (-0.3, 0.3), (0.1, 0.6)
    assert direct.explanation(0.4, within, drift) == "more like a drift"
    assert direct.explanation(0.7, within, drift) == "more like a drift"
    assert direct.explanation(0.0, within, drift) == "more like dependence"
    assert direct.explanation(-0.5, within, drift) == "more like dependence"
    assert direct.explanation(0.2, within, drift) == "not separated"
    assert direct.explanation(0.35, within, (0.5, 0.8)) == "not separated"
