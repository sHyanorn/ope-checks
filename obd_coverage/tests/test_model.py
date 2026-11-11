import numpy as np
import pytest

from obd.posthoc.units import MINUTE_US
from obd_coverage import model
from obd_coverage.tests import small


def test_kept_rows_carry_block_cell_weight_and_impression():
    (random, bts), _, pi0 = small.logs(0)
    frame = small.frames(0)[0]
    item, position = frame["item_id"].to_numpy(), frame["position"].to_numpy() - 1
    assert (random.cell == 3 * item + position).all()
    assert np.allclose(random.weight, len(pi0) * pi0[item, position])
    assert (bts.weight == 1).all()
    assert (random.step == random.t // (5 * MINUTE_US)).all() and random.step.max() < model.N_STEPS
    assert random.size.sum() == len(random.t)
    assert (random.start[random.impression] <= random.t).all()


def groups_of(seed, minutes, long_minutes):
    start = np.sort(np.random.default_rng(seed).integers(0, 10080 * MINUTE_US, 200_000))
    return start, model.groupings(start, minutes, long_minutes, np.random.default_rng(1))


def test_a_session_holds_about_five_and_a_half_impressions_within_its_span():
    start, groups = groups_of(0, 5, None)
    first, last = (np.full(groups.session.max() + 1, x) for x in (np.inf, -np.inf))
    np.minimum.at(first, groups.session, start)
    np.maximum.at(last, groups.session, start)
    assert (last - first < 5 * MINUTE_US).all()
    assert np.bincount(groups.session).mean() == pytest.approx(model.SESSION_SIZE, rel=0.02)
    assert groups.long is None


def test_long_groups_hold_about_three_sessions_and_leave_the_sessions_as_they_were():
    start, groups = groups_of(0, 5, 60)
    assert (groups.session == groups_of(0, 5, None)[1].session).all()
    assert np.bincount(groups.long).mean() == pytest.approx(3, rel=0.05)
    first, last = (np.full(groups.long.max() + 1, x) for x in (np.inf, -np.inf))
    np.minimum.at(first, groups.long[groups.session], start)
    np.maximum.at(last, groups.long[groups.session], start)
    assert (last - first < 60 * MINUTE_US).all()
    assert (last - first > 20 * MINUTE_US).mean() > 0.5  # they reach beyond a session


def test_long_groups_do_not_start_on_the_clock_hour():
    start, groups = groups_of(0, 5, 60)
    first = np.full(groups.long.max() + 1, np.inf)
    np.minimum.at(first, groups.long[groups.session], start)
    minute = first % (60 * MINUTE_US) / MINUTE_US
    assert np.histogram(minute, bins=6, range=(0, 60))[0].min() > 0.1 * len(first)


def pair_counts(clicks, *groups):
    """Ordered pairs of clicked rows that share each grouping, narrowest first."""
    return [(np.bincount(g, clicks) ** 2).sum() - clicks.sum() for g in groups]


def test_clicks_have_the_marginal_rate_and_the_pair_probabilities_of_each_grouping():
    rng = np.random.default_rng(0)
    n_impressions, e = 30_000, (2.5, 1.2, 0.4)
    impression = np.repeat(np.arange(n_impressions), 3)
    start = np.sort(rng.integers(0, 10080 * MINUTE_US, n_impressions))
    groups = model.groupings(start, 5, 60, rng)
    q = rng.uniform(0.05, 0.25, len(impression))
    session, long = groups.session[impression], groups.long[groups.session][impression]
    expected = np.array(pair_counts(q, impression, session, long)) - np.array(
        [(q**2).sum() - q.sum()] * 3
    )
    expected = np.diff(expected, prepend=0) * (1 + np.array(e))  # pairs sharing exactly this much
    seen, total = np.zeros(3), 0
    for _ in range(300):
        clicks = np.zeros(len(q))
        clicks[model.draw(rng, q, impression, groups, e)] = 1
        seen += np.diff(pair_counts(clicks, impression, session, long), prepend=0)
        total += clicks.sum()
    assert total / 300 == pytest.approx(q.sum(), rel=0.01)
    assert seen / 300 == pytest.approx(expected, rel=0.03)


def test_independent_clicks_have_binomial_mean_and_variance():
    rng = np.random.default_rng(0)
    q = np.full(20_000, 0.02)
    counts = [len(model.draw(rng, q, np.arange(20_000), None, (0, 0, 0))) for _ in range(2000)]
    assert np.mean(counts) == pytest.approx(400, rel=0.01)
    assert np.var(counts) == pytest.approx(400 * 0.98, rel=0.1)


def test_within_an_impression_only_the_impression_is_drawn():
    rng = np.random.default_rng(0)
    impression = np.repeat(np.arange(50_000), 2)
    clicks = np.zeros(100_000)
    clicks[model.draw(rng, np.full(100_000, 0.1), impression, None, (4, 0, 0))] = 1
    both = (np.bincount(impression, clicks) == 2).mean()
    assert both == pytest.approx(0.1 * 0.1 * 5, rel=0.05)


def test_excesses_must_be_nested_and_within_what_the_rates_allow():
    with pytest.raises(ValueError, match="e_L <= e_S <= e_I"):
        model.on_probabilities((1, 2, 0))
    with pytest.raises(ValueError, match="allow"):
        model.draw(np.random.default_rng(0), np.array([0.3]), np.array([0]), None, (3, 0, 0))


def test_cell_rates_pool_the_logs():
    (random, bts), clicks, _ = small.logs(0)
    rate = model.cell_rates([random, bts], clicks, 18)
    cell = 7
    rows = (random.cell == cell).sum() + (bts.cell == cell).sum()
    clicked = clicks[0][random.cell == cell].sum() + clicks[1][bts.cell == cell].sum()
    assert rate[cell] == pytest.approx(clicked / rows)


def test_fitted_drift_is_day_times_hour_of_day():
    (random, bts), _, _ = small.logs(0, n_random=200_000, n_bts=200_000)
    rate = np.full(18, 0.1)
    hour = [log.t // (60 * MINUTE_US) for log in (random, bts)]
    truth = np.outer(1 + 0.1 * np.arange(7), 1 + 0.02 * np.arange(24)).ravel()
    rng = np.random.default_rng(0)
    clicks = [rng.random(len(h)) < 0.1 * truth[h] for h in hour]
    fitted = model.fitted_drift([random, bts], clicks, rate)
    assert fitted / fitted.mean() == pytest.approx(truth / truth.mean(), abs=0.15)
    assert fitted.reshape(7, 24)[6].mean() / fitted.reshape(7, 24)[0].mean() == pytest.approx(
        1.6, rel=0.05
    )


def test_drift_is_linear_between_the_midpoints_of_the_hours():
    by_hour = np.arange(1.0, model.HOURS + 1)
    t = np.array([0, 30, 60, 90, 10080]) * MINUTE_US
    assert model.drift(t, by_hour) == pytest.approx([1, 1, 1.5, 2, model.HOURS])


def test_sizes_of_sessions_and_long_groups_can_be_set():
    start = np.sort(np.random.default_rng(0).integers(0, 10080 * MINUTE_US, 200_000))
    groups = model.groupings(start, 5, 60, np.random.default_rng(1), size=11, per_long=6)
    assert np.bincount(groups.session).mean() == pytest.approx(11, rel=0.02)
    assert np.bincount(groups.long).mean() == pytest.approx(6, rel=0.05)


def test_sessions_within_kinds_hold_one_kind_and_keep_their_size_and_span():
    rng = np.random.default_rng(0)
    start = np.sort(rng.integers(0, 10080 * MINUTE_US, 200_000))
    kind = rng.choice(3, 200_000, p=[0.7, 0.2999, 0.0001])
    groups = model.groupings(start, 5, 60, np.random.default_rng(1), kind=kind)
    kinds = np.zeros((groups.session.max() + 1, 3), bool)
    kinds[groups.session, kind] = True
    assert (kinds.sum(axis=1) == 1).all()
    for k in range(2):  # as close to 5.5 as a whole number of labels allows
        in_a_span = (kind == k).sum() * 5 / 10080
        sizes = np.bincount(groups.session[kind == k])
        expected = in_a_span / round(in_a_span / model.SESSION_SIZE)
        assert sizes[sizes > 0].mean() == pytest.approx(expected, rel=0.02)
        assert expected == pytest.approx(model.SESSION_SIZE, rel=0.1)
    first, last = (np.full(groups.session.max() + 1, x) for x in (np.inf, -np.inf))
    np.minimum.at(first, groups.session, start)
    np.maximum.at(last, groups.session, start)
    assert (last - first < 5 * MINUTE_US).all()
    long_kinds = np.zeros((groups.long.max() + 1, 3), bool)
    long_kinds[groups.long[groups.session], kind] = True
    assert (long_kinds.sum(axis=1) == 1).all()


def test_two_level_factors_keep_the_marginal_rate_and_the_pair_probabilities():
    rng = np.random.default_rng(0)
    n_impressions, e = 30_000, (2.5, 1.2, 0.4)
    impression = np.repeat(np.arange(n_impressions), 3)
    start = np.sort(rng.integers(0, 10080 * MINUTE_US, n_impressions))
    groups = model.groupings(start, 5, 60, rng)
    q = rng.uniform(0.02, 0.1, len(impression))
    session, long = groups.session[impression], groups.long[groups.session][impression]
    expected = np.array(pair_counts(q, impression, session, long)) - np.array(
        [(q**2).sum() - q.sum()] * 3
    )
    expected = np.diff(expected, prepend=0) * (1 + np.array(e))
    seen, total = np.zeros(3), 0
    for _ in range(600):
        rows = model.draw(rng, q, impression, groups, e, low=0.5)
        clicks = np.zeros(len(q))
        clicks[rows] = 1
        seen += np.diff(pair_counts(clicks, impression, session, long), prepend=0)
        total += clicks.sum()
    assert total / 600 == pytest.approx(q.sum(), rel=0.01)
    assert seen / 600 == pytest.approx(expected, rel=0.04)


def test_a_two_level_factor_reaches_higher_than_an_on_off_factor():
    e = (2.5, 1.2, 0.4)
    assert model.largest_factor(e) == pytest.approx(3.5)
    assert model.largest_factor(e, low=0.5) == pytest.approx(
        1.8 * (1 + 2 * (2.2 / 1.4 - 1)) * (1 + 2 * (3.5 / 2.2 - 1))
    )
    with pytest.raises(ValueError, match="allow"):
        model.draw(
            np.random.default_rng(0), np.full(3, 0.2), np.zeros(3, int), None, (3, 0, 0), 0.5
        )
