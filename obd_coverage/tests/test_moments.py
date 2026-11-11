import numpy as np
import pytest

from obd.posthoc.units import variance_ratio
from obd_coverage import model, moments
from obd_coverage.tests import small

EXCESS = (2.5, 1.2, 0.4)


def setting(seed=0):
    """Two small logs with groupings, click probabilities and a few hundred data sets."""
    logs, _, _ = small.logs(seed)
    rng = np.random.default_rng(seed)
    groups = [model.groupings(log.start, 5, 60, rng) for log in logs]
    q = [rng.uniform(0.05, 0.25, len(log.t)) for log in logs]
    return logs, groups, q, rng


def data_sets(rng, logs, groups, q, excess, n):
    for _ in range(n):
        yield [
            model.draw(rng, x, log.impression, g, excess)
            for log, g, x in zip(logs, groups, q, strict=True)
        ]


def test_variance_of_a_weighted_sum_of_clicks_matches_simulation():
    logs, groups, q, rng = setting()
    log, lay = logs[0], moments.layout(logs[0], groups[0])
    a = rng.uniform(0.5, 2, len(log.t))
    p = moments.part(lay, q[0], a, np.zeros(len(a)), EXCESS)
    by_hour = lay.step // 12
    sums = np.array(
        [
            np.bincount(log.step[rows] // 12, a[rows], model.HOURS)
            for rows, _ in data_sets(rng, logs, groups, q, EXCESS, 1500)
        ]
    )
    assert moments.variance(p) == pytest.approx(sums.sum(axis=1).var(), rel=0.1)
    assert moments.variance(p, by_hour) == pytest.approx(sums.var(axis=0).sum(), rel=0.03)
    independent = moments.part(lay, q[0], a, np.zeros(len(a)))
    assert moments.variance(independent) == pytest.approx((a**2 * q[0] * (1 - q[0])).sum())
    assert moments.variance(p) > 1.5 * moments.variance(independent)


def test_a_grouping_wider_than_the_unit_adds_nothing_inside_it():
    logs, groups, q, _ = setting()
    lay = moments.layout(logs[0], groups[0])
    a = np.ones(len(q[0]))
    within = [moments.part(lay, q[0], a, 0 * a, e) for e in ((2.5, 0, 0), (2.5, 2.5, 2.5))]
    by_impression = [moments.variance(p, lay.impression) for p in within]
    assert by_impression[0] == pytest.approx(by_impression[1])
    assert moments.variance(within[1]) > moments.variance(within[0])


def test_true_values_are_exact_sums_and_the_linearised_variance_matches_simulation():
    logs, groups, q, rng = setting()
    lays = [moments.layout(log, g) for log, g in zip(logs, groups, strict=True)]
    parts, truth = moments.quantity_parts(*logs, *q, *lays, EXCESS, EXCESS)
    w = logs[0].weight
    assert truth["v_on"] == pytest.approx(q[1].mean())
    assert truth["ips"] == pytest.approx((w * q[0]).mean())
    assert truth["ips_ratio"] == pytest.approx((w * q[0]).mean() / q[1].mean())
    assert truth["snips_ratio"] == pytest.approx((w * q[0]).sum() / w.sum() / q[1].mean())
    seen = np.array(
        [
            [w[r].sum() / len(w) / (len(b) / len(q[1])), w[r].sum() / len(w), len(b) / len(q[1])]
            for r, b in data_sets(rng, logs, groups, q, EXCESS, 1500)
        ]
    )
    relative = seen.var(axis=0) / np.array([truth[k] for k in ("ips_ratio", "ips", "v_on")]) ** 2
    predicted = [moments.true_variance(parts[k]) for k in ("ips_ratio", "ips", "v_on")]
    assert predicted == pytest.approx(relative, rel=0.1)
    assert predicted[0] == pytest.approx(predicted[1] + predicted[2])


def test_under_independence_every_unit_expects_about_the_true_variance():
    logs, _, q, _ = setting()
    lays = [moments.layout(log) for log in logs]
    parts, _ = moments.quantity_parts(*logs, *q, *lays, (0, 0, 0), (0, 0, 0))
    for quantity in parts:
        true = moments.true_variance(parts[quantity])
        for unit in ("rows", "impressions", 10, 60):
            assert moments.bootstrap_variance(parts[quantity], unit) == pytest.approx(true, rel=0.2)
        assert moments.predicted_coverage(parts[quantity], "rows") == pytest.approx(0.95, abs=0.02)


def test_units_see_the_dependence_inside_them_only():
    logs, groups, q, _ = setting()
    lays = [moments.layout(log, g) for log, g in zip(logs, groups, strict=True)]
    parts = moments.quantity_parts(*logs, *q, *lays, EXCESS, EXCESS)[0]["ips_ratio"]
    expected = [moments.bootstrap_variance(parts, u) for u in ("rows", "impressions", 5, 60, 180)]
    assert expected == sorted(expected)
    assert expected[-1] < moments.true_variance(parts) * 1.1
    assert moments.predicted_coverage(parts, "rows") < moments.predicted_coverage(parts, 60) < 0.96


def test_coverage_of_an_interval_with_the_wrong_variance():
    assert moments.coverage(1) == pytest.approx(0.95)
    assert moments.coverage(0.5) == pytest.approx(0.8342, abs=1e-4)


def test_the_calibration_equations_return_the_strengths_they_were_built_from():
    logs, groups, q, _ = setting()
    lays = [moments.layout(log, g) for log, g in zip(logs, groups, strict=True)]

    def ips_ratio(excess):
        return moments.quantity_parts(*logs, *q, *lays, excess, excess)[0]["ips_ratio"]

    def expected(excess, unit):
        return moments.bootstrap_variance(ips_ratio(excess), unit)

    e_i, e_s, e_l = EXCESS
    by_rows = expected((0, 0, 0), "rows")
    ratio = expected((e_i, 0, 0), "impressions") / by_rows
    solved = moments.solve(
        ratio, [expected((e, 0, 0), "impressions") for e in (0, 1)], (by_rows, by_rows)
    )
    assert solved == pytest.approx(e_i)
    widening = expected(EXCESS, 180) / expected(EXCESS, 10)
    solved = moments.solve(
        widening,
        [expected((e_i, e_s, e), 180) for e in (0, 1)],
        [expected((e_i, e_s, e), 10) for e in (0, 1)],
    )
    assert solved == pytest.approx(e_l)


def test_expected_variance_ratio_matches_the_statistic_on_simulated_clicks():
    log = small.logs(0, n_bts=300_000)[0][1]
    rng = np.random.default_rng(0)
    groups = model.groupings(log.start, 5, None, rng)
    q = rng.uniform(0.05, 0.25, len(log.t))
    e_i, e_s = 2.5, 1.2
    for minutes in (10, 60):
        (n0, n1), (d0, d1) = moments.variance_ratio_moments(log, q, groups.session, e_i, minutes)
        seen = [
            variance_ratio(
                log.start,
                np.bincount(log.impression[rows], minlength=len(log.size)),
                log.size,
                minutes,
            )
            for (rows,) in data_sets(rng, [log], [groups], [q], (e_i, e_s, 0), 60)
        ]
        expected = (n0 + e_s * (n1 - n0)) / (d0 + e_s * (d1 - d0))
        assert expected == pytest.approx(np.mean(seen), rel=0.03)
        assert moments.solve(expected, (n0, n1), (d0, d1)) == pytest.approx(e_s)
        assert n0 / d0 == pytest.approx(1, abs=0.05) and expected > 1.3
