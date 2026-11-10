import numpy as np
from pytest import approx

from obd import estimators as est
from obd import tables
from obd.data import BLOCK_US, WEEK_START_US
from obd.tests.fixtures import campaign, rows
from obd.tests.synthetic import converted, raw_log, uniform


def estimate(t, pi0=None, width=1, eligible=None):
    n_items = t.b_rows.shape[2]
    pi0 = np.full((n_items, 3), 1 / n_items) if pi0 is None else np.asarray(pi0)
    eligible = np.zeros((n_items, 3), bool) if eligible is None else eligible
    return est.estimate(t, pi0, width, eligible)


def block(j, count):
    """Multiplicities of one everywhere except `count` at block j."""
    m = np.ones(1008, int)
    m[j] = count
    return m


def by_block(n_items, entries):
    out = np.zeros((1008, n_items, 3), int)
    for key, n in entries.items():
        out[key] = n
    return out


def by_hour(n_items, entries):
    out = np.zeros((168, n_items, 3))
    for key, n in entries.items():
        out[key] = n
    return out


# Random streams of Section 5


def test_multiplicities_follow_the_registered_call():
    registered = np.random.default_rng([20261110, 0, 7]).multinomial(1008, np.full(1008, 1 / 1008))
    assert est.multiplicities(7).tolist() == registered.tolist()
    assert est.multiplicities(8).tolist() != registered.tolist()


def test_prior_target_follows_the_registered_call():
    alpha, beta = np.array([2.0, 3.0, 4.0]), np.array([5.0, 4.0, 9.0])
    draws = np.random.default_rng([20261110, 1, 2]).beta(alpha, beta, size=(1_000_000, 3))
    pi0 = est.fixed_prior_target(alpha, beta, stream=2)
    for item in range(3):
        assert pi0[item, 0] == approx((draws.argmax(axis=1) == item).mean(), abs=1e-12)
        assert pi0[item, 2] == approx((draws.argmin(axis=1) == item).mean(), abs=1e-12)


def test_prior_target_ranks_separated_items():
    alpha, beta = np.array([900.0, 500.0, 100.0, 1.0]), np.array([100.0, 500.0, 900.0, 999.0])
    pi0 = est.fixed_prior_target(alpha, beta, stream=1)
    assert pi0.tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]


def test_prior_target_of_exchangeable_items_is_uniform():
    pi0 = est.fixed_prior_target(np.full(5, 2.0), np.full(5, 30.0), stream=0)
    assert pi0 == approx(np.full((5, 3), 0.2), abs=0.003)
    assert pi0.sum(axis=0) == approx(1)


# H1


def test_h1_distance_and_noise_floor():
    counts = by_block(2, {(0, 0, 0): 4, (1, 0, 0): 2, (1, 1, 0): 2})
    result = est.h1(counts, np.full((2, 3), 0.5))
    assert result["d"] == 0.25  # hour frequencies (0.75, 0.25) against (0.5, 0.5)
    assert result["d0"] == 0.5  # (1, 0) in the even block against (0.5, 0.5) in the odd
    assert result["left_out"] == 0
    assert result["first_hour"][0] == 0.25


def test_h1_weights_cells_by_their_rows():
    counts = by_block(2, {(0, 0, 0): 4, (1, 0, 0): 2, (1, 1, 0): 2, (6, 0, 1): 1, (7, 0, 1): 1})
    result = est.h1(counts, np.full((2, 3), 0.5))
    assert result["d"] == approx((8 * 0.25 + 2 * 0.5) / 10)
    assert result["d0"] == approx(8 * 0.5 / 10)


def test_h1_leaves_out_cells_with_an_empty_half():
    counts = by_block(2, {(0, 0, 0): 4, (1, 0, 0): 2, (1, 1, 0): 2, (6, 0, 0): 2})
    result = est.h1(counts, np.full((2, 3), 0.5))
    assert (result["d"], result["d0"], result["left_out"]) == (0.25, 0.5, approx(0.2))


def test_h1_halves_are_alternate_blocks():
    counts = by_block(2, {(j, j % 2, 0): 1 for j in range(6)})
    assert est.h1(counts, np.full((2, 3), 0.5))["d0"] == 1


# H2


def test_h2_statistic():
    bts = rows(2, item=0, p=0.5, minute=0) + rows(1, item=1, p=0.2, minute=0)
    t, facts = campaign(rows(1, minute=0), bts)
    eligible = est.eligible_cells(facts["min_propensity"])
    out = estimate(t, eligible=eligible)
    assert out["h2.s.0.1"] == approx(4 / 3)
    assert out["h2.s.1.1"] == approx(5 / 3)
    assert out["h2.m"] == approx(1.5)


def test_h2_eligibility_bound():
    bts = [
        {"minute": 0, "item": 0, "p": 0.001},
        {"minute": 0, "item": 1, "p": 0.5},
        {"minute": 9, "item": 1, "p": 0.000995},
    ]
    _, facts = campaign(rows(1, minute=0), bts)
    assert est.eligible_cells(facts["min_propensity"]).tolist() == [
        [True, False, False],
        [False, False, False],
    ]


def test_h2_cells_stay_as_chosen_while_sums_are_recomputed():
    bts = rows(2, item=0, p=0.5, minute=0) + rows(1, item=1, p=0.2, minute=10)
    t, facts = campaign(rows(1, minute=0), bts)
    eligible = est.eligible_cells(facts["min_propensity"])
    tripled = estimate(t.resample(block(1, 3)), eligible=eligible)
    assert (tripled["h2.s.0.1"], tripled["h2.s.1.1"]) == (approx(4 / 5), approx(15 / 5))
    absent = estimate(t.resample(block(1, 0)), eligible=eligible)
    assert (absent["h2.s.0.1"], absent["h2.s.1.1"], absent["h2.m"]) == (2, 0, 1)


# H3

H3_RANDOM = rows(6, clicks=3, item=0, minute=0) + rows(2, clicks=1, item=1, minute=0)
H3_TARGET = [[0.8, 0.5, 0.5], [0.2, 0.5, 0.5]]


def test_h3_estimators():
    t, _ = campaign(H3_RANDOM, rows(4, clicks=1, minute=0))
    out = estimate(t, pi0=H3_TARGET)
    assert out["v_on"] == 0.25
    assert out["h3.ips"] == approx((1.6 * 3 + 0.4 * 1) / 8 / 0.25)
    assert out["h3.snips"] == approx((1.6 * 3 + 0.4 * 1) / (1.6 * 6 + 0.4 * 2) / 0.25)
    assert out["h3.mean_weight"] == approx(1.3)


def test_h3_ratio_uses_the_on_policy_value_of_the_same_replicate():
    t, _ = campaign(H3_RANDOM, rows(4, clicks=1, minute=0) + rows(4, clicks=3, minute=10))
    assert estimate(t, pi0=H3_TARGET)["h3.ips"] == approx(0.65 / 0.5)
    assert estimate(t.resample(block(1, 3)), pi0=H3_TARGET)["h3.ips"] == approx(0.65 / 0.625)


# H4

H4_B = {(0, 0, 0): 10, (1, 0, 0): 10, (30, 0, 0): 20}
H4_R = {(0, 0, 0): 5, (1, 0, 0): 4, (30, 0, 0): 2, (40, 0, 0): 2}
H4_CLICKS = {(0, 0, 0): 3, (1, 0, 0): 1, (30, 0, 0): 2}


def test_matched_takes_the_narrowest_level_with_enough_rows():
    v_m, shares = est.matched(by_hour(1, H4_B), by_hour(1, H4_R), by_hour(1, H4_CLICKS), 1)
    # hour 0 is covered; hour 1 resolves at three hours; hour 30 only at the week
    assert v_m == approx((10 * 3 / 5 + 10 * 4 / 9 + 20 * 6 / 13) / 40)
    assert shares == {1: 0.25, 3: 0.25, 6: 0, 24: 0, 168: 0.5, "dropped": 0}


def test_matched_starts_the_fallback_from_the_width_given():
    v_m, shares = est.matched(by_hour(1, H4_B), by_hour(1, H4_R), by_hour(1, H4_CLICKS), 3)
    assert v_m == approx((20 * 4 / 9 + 20 * 6 / 13) / 40)
    assert shares == {3: 0.5, 6: 0, 24: 0, 168: 0.5, "dropped": 0}


def test_matched_drops_cells_short_of_rows_in_the_week_and_renormalises():
    b = by_hour(2, {(0, 0, 0): 30, (0, 1, 0): 10})
    r = by_hour(2, {(0, 0, 0): 5, (0, 1, 0): 2, (100, 1, 0): 2})
    clicks = by_hour(2, {(0, 0, 0): 1, (0, 1, 0): 2})
    v_m, shares = est.matched(b, r, clicks, 1)
    assert v_m == approx(0.2)
    assert (shares[1], shares["dropped"]) == (0.75, 0.25)


def test_matched_is_undefined_when_every_cell_is_dropped():
    b, r = by_hour(1, {(0, 0, 0): 10}), by_hour(1, {(0, 0, 0): 4})
    v_m, shares = est.matched(b, r, r, 1)
    assert np.isnan(v_m)
    assert shares["dropped"] == 1


def test_matched_identity_when_every_cell_is_covered():
    rng = np.random.default_rng(1)
    policy = np.array([[0.5, 0.3, 0.2], [0.2, 0.2, 0.6], [0.1, 0.8, 0.1]])
    random = converted(raw_log(rng, 30_000, uniform(3), np.array([0.2, 0.4, 0.6])))
    bts = converted(raw_log(rng, 60_000, policy, np.array([0.3, 0.3, 0.5])))
    t, _ = tables.build(random, bts, np.full(3, 0.5))
    out = estimate(t, width=24)
    assert out["h4.share.24.24"] == 1

    def cells(log):
        day = (log["timestamp"] - WEEK_START_US) // (144 * BLOCK_US)
        return log.groupby([day, "item_id", "position"])["click"].agg(["size", "mean"])

    b, r = cells(bts), cells(random)
    gap = (b["size"] / len(bts) * (b["mean"] - r["mean"])).sum()
    assert out["v_on"] * (1 - out["h4.rho.24"]) == approx(gap)
    assert out["h4.d.24"] == approx(out["h4.rho.24"] - out["h3.ips"])


def test_multiplicities_count_towards_the_minimum_cell_count():
    random = rows(3, clicks=3, minute=0) + rows(6, minute=70)
    t, _ = campaign(random, rows(10, clicks=5, minute=0))
    full = estimate(t)  # three rows in the hour: resolved at three hours, 3 clicks in 9
    assert (full["h4.share.1.1"], full["h4.share.1.3"]) == (0, 1)
    assert full["h4.rho.1"] == approx(1 / 3 / 0.5)
    doubled = estimate(t.resample(block(0, 2)))  # six rows in the hour: covered
    assert doubled["h4.share.1.1"] == 1
    assert doubled["h4.rho.1"] == approx(1 / 0.5)


def test_bts_shares_and_on_policy_value_follow_the_replicate():
    random = rows(5, clicks=1, minute=0) + rows(5, clicks=4, minute=60)
    bts = rows(4, clicks=1, minute=0) + rows(4, clicks=3, minute=60)
    t, _ = campaign(random, bts)
    assert estimate(t)["h4.rho.1"] == approx((0.5 * 0.2 + 0.5 * 0.8) / 0.5)
    tripled = estimate(t.resample(block(6, 3)))  # hour 1 of both logs three times
    assert tripled["v_on"] == approx(10 / 16)
    assert tripled["h4.rho.1"] == approx((4 * 0.2 + 12 * 0.8) / 16 / (10 / 16))
    gone = estimate(t.resample(block(6, 0)))  # a cell without BTS rows has no weight
    assert gone["h4.rho.1"] == approx(0.2 / 0.25)


def test_width_is_the_narrowest_that_reaches_tau():
    r = by_hour(1, {(0, 0, 0): 5, (1, 0, 0): 4})
    width, coverage = est.choose_width(by_hour(1, {(0, 0, 0): 99, (1, 0, 0): 1}), r)
    assert (width, coverage[1]) == (1, 0.99)  # exactly tau is enough
    width, coverage = est.choose_width(by_hour(1, {(0, 0, 0): 98, (1, 0, 0): 2}), r)
    assert (width, coverage[1], coverage[3]) == (3, 0.98, 1)


def test_width_is_a_day_when_no_width_reaches_tau():
    b, r = by_hour(1, {(0, 0, 0): 10}), by_hour(1, {(0, 0, 0): 4})
    assert est.choose_width(b, r) == (24, {1: 0, 3: 0, 6: 0, 24: 0})


def test_h4_in_ips_form_and_with_whole_week_frequencies():
    bts = (
        rows(3, clicks=2, item=0, minute=0)
        + rows(1, item=1, minute=0)
        + rows(1, item=0, minute=60)
        + rows(3, item=1, minute=60)
        + rows(4, item=0, position=2, minute=300)  # no random rows there: left out
    )
    random = (
        rows(4, clicks=2, item=0, minute=0)
        + rows(4, clicks=4, item=1, minute=0)
        + rows(2, item=0, minute=60)
        + rows(2, clicks=1, item=1, minute=60)
    )
    t, _ = campaign(random, bts)
    out = estimate(t)
    hour_0 = 2 * (0.75 * 2 + 0.25 * 4) / 8
    hour_1 = 2 * (0.25 * 0 + 0.75 * 1) / 4
    assert out["h4.ips_form"] == approx((4 * hour_0 + 4 * hour_1) / 8 / out["v_on"])
    assert out["h4.ips_week"] == approx(2 * 0.5 * 7 / 12 / out["v_on"])


# H5

H5_BTS = (
    rows(3, clicks=2, item=0, minute=0)
    + rows(1, item=1, minute=0)
    + rows(1, item=0, minute=60)
    + rows(1, item=1, minute=60)
    + rows(1, item=0, minute=120)
    + rows(3, item=1, minute=120)
)
H5_RANDOM = (
    rows(4, clicks=4, item=0, minute=0)
    + rows(2, clicks=1, item=0, minute=60)
    + rows(2, clicks=2, item=1, minute=60)
)


def test_h5_hour_before_and_after():
    t, _ = campaign(H5_RANDOM, H5_BTS)
    out = estimate(t)
    before = 2 * (0.75 * 1 + 0.25 * 2) / 4  # hour 1 only: hour 0 has no hour before it
    after_0, after_1 = 2 * 0.5 * 4 / 4, 2 * (0.25 * 1 + 0.75 * 2) / 4
    assert out["h5.before"] == approx(before / 0.2)
    assert out["h5.left_out.before"] == 0.5
    assert out["h5.after"] == approx((4 * after_0 + 2 * after_1) / 6 / 0.2)
    assert out["h5.left_out.after"] == 0
    assert out["h5.after_minus_before"] == approx((after_1 - before) / 0.2)
    assert out["h5.left_out.after_minus_before"] == 0.5


def test_h5_window_emptied_by_a_replicate_leaves_its_rows_out():
    t, _ = campaign(H5_RANDOM, H5_BTS)
    out = estimate(t.resample(block(0, 0)))
    assert np.isnan(out["h5.before"])
    assert np.isnan(out["h5.after_minus_before"])
    assert out["h5.left_out.before"] == 1


def test_h5_fifteen_minutes_before():
    bts = rows(1, clicks=1, item=0, minute=5) + rows(1, item=1, minute=40)
    random = (
        rows(2, clicks=1, item=0, minute=20)  # window 0:00 to 0:15 holds item 0
        + rows(3, clicks=3, item=1, minute=50)  # window 0:30 to 0:45 holds item 1
        + rows(1, clicks=1, minute=35)  # window 0:15 to 0:30 is empty
    )
    t, _ = campaign(random, bts)
    out = estimate(t)
    assert out["h5.before_15"] == approx((2 * 1 + 2 * 3) / 5 / 0.5)
    assert out["h5.left_out.before_15"] == approx(1 / 6)


# H6


def test_h6_estimators():
    bts = [
        {"minute": 0, "p": 0.5, "click": 1},
        {"minute": 0, "p": 0.25},
        {"minute": 0, "p": 0.25, "click": 1},
        {"minute": 0, "p": 1.0},
    ]
    t, _ = campaign(rows(4, clicks=2, minute=0), bts)
    out = estimate(t)
    assert out["h6.ips"] == approx((1 + 2) / 4 / 0.5)
    assert out["h6.snips"] == approx((1 + 2) / (1 + 2 + 2 + 0.5) / 0.5)


# H7


def test_h7_distances():
    random = [
        {"minute": minute, "user": (a, b, "-", "-")}
        for (a, b), minute in zip(["ax", "ay", "bx", "by"], [0, 0, 60, 60], strict=False)
    ]
    bts = rows(3, clicks=1, minute=0, user=("a", "x", "-", "-")) + rows(
        1, minute=0, user=("b", "y", "-", "-")
    )
    t, _ = campaign(random, bts)
    out = estimate(t)
    assert out["h7.tv.feature_0"] == 0.25
    assert out["h7.tv.feature_1"] == 0.25
    assert out["h7.tv.feature_2"] == 0
    assert out["h7.tv.joint"] == 0.5
    assert out["h7.tv.hours"] == 0.5
    assert out["h7.absent"] == 0


H7_RANDOM = rows(3, clicks=3, user="a", minute=0) + rows(3, user="b", minute=0)


def test_h7_user_weighted_click_rate():
    t, _ = campaign(H7_RANDOM, rows(9, clicks=3, user="a", minute=0) + rows(3, user="b", minute=0))
    out = estimate(t)  # v is 1.5 for a and 0.5 for b: 0.75 against 0.5 unweighted
    assert out["h7.rho_change"] == approx((0.75 - 0.5) / 0.25)


def test_h7_weights_follow_the_replicate():
    bts = rows(9, clicks=3, user="a", minute=0) + rows(3, user="b", minute=10)
    t, _ = campaign(H7_RANDOM, bts)
    assert estimate(t)["h7.rho_change"] == approx(1)
    assert estimate(t.resample(block(1, 3)))["h7.rho_change"] == approx(0)  # equal shares


def test_h7_cell_without_weight_takes_the_unweighted_rate():
    random = rows(3, clicks=2, user="c", minute=0) + rows(3, clicks=1, user="d", minute=0)
    t, _ = campaign(random, rows(4, clicks=1, user="a", minute=0))  # no user of B is in R
    out = estimate(t)
    assert out["h4.rho.1"] == 2
    assert out["h7.rho_change"] == 0
    assert out["h7.absent"] == 1


# Exploratory item


def impression(minute, items, clicks=(0, 0, 0), user="a"):
    return [
        {"minute": minute + k / 1000, "item": item, "position": k + 1, "click": click, "user": user}
        for k, (item, click) in enumerate(zip(items, clicks, strict=False))
    ]


CONTEXT_RANDOM = (
    impression(0, (0, 1, 2))
    + impression(10, (0, 2, 3), (1, 0, 0))
    + impression(20, (0, 1, 3), (1, 0, 0))
    + impression(30, (0, 1, 2), (1, 0, 0))
)
PRIOR_MEAN = [0.1, 0.2, 0.3, 0.4]


def test_exploratory_difference():
    t, facts = campaign(CONTEXT_RANDOM, rows(1, minute=0), n_items=4, prior_mean=PRIOR_MEAN)
    assert (facts["impressions"], facts["complete_impressions"]) == (4, 4)
    # item 0 at position 1: x is 0.25, 0.35, 0.3, 0.25; clicks 1 and 1 above the
    # median against 0 and 1 below. Two other cells have both sides and no click.
    assert estimate(t)["exploratory"] == approx((4 * 0.5 + 3 * 0 + 2 * 0) / 9 / (3 / 12))


def test_exploratory_rows_keep_their_side_in_a_replicate():
    t, _ = campaign(CONTEXT_RANDOM, rows(1, minute=0), n_items=4, prior_mean=PRIOR_MEAN)
    out = estimate(t.resample(block(1, 0)))  # without the second impression
    assert out["exploratory"] == approx((3 * 0.5 + 3 * 0) / 6 / (2 / 9))


def test_exploratory_x_does_not_depend_on_the_order_of_the_other_two_items():
    # every row of item 2 at position 2 has the same x: none is above the median
    random = impression(0, (1, 2, 0)) + impression(10, (0, 2, 1)) + impression(20, (1, 2, 0))
    t, _ = campaign(random, rows(1, minute=0), n_items=3, prior_mean=[0.000165, 0.008133, 0.009128])
    assert t.x_rows.sum(axis=0)[2, 1].tolist() == [3, 0]


def test_impressions_are_runs_of_adjacent_rows_in_time_order():
    random = (
        [{"minute": m, "position": p} for m, p in [(0, 1), (0.002, 3), (0.001, 2)]]  # complete
        + [{"minute": 5 + k / 1000, "position": k + 1, "user": u} for k, u in enumerate("aba")]
        + [{"minute": m, "position": p} for m, p in [(10, 1), (10.001, 2), (10.02, 3)]]  # 1.1 s gap
        + [{"minute": 20 + k / 1000, "position": p} for k, p in enumerate([1, 2, 3, 1])]
    )
    _, facts = campaign(random, rows(1, minute=0))
    assert (facts["impressions"], facts["complete_impressions"]) == (7, 1)


def test_h7_reference_distance_between_alternate_blocks():
    users = np.zeros((1008, 2), int)
    users[0], users[1], users[6], users[9] = (3, 1), (1, 3), (4, 0), (0, 4)
    features = np.array([[0, 0], [1, 0]])  # two users: they differ in the first feature
    out = est.between_alternate_blocks(users, users.sum(axis=1), features)
    # even blocks hold users (7, 1) in hours (4, 4); odd blocks (1, 7) in hours (4, 4)
    assert out == {"feature_0": 0.75, "feature_1": 0, "joint": 0.75, "hours": 0}
