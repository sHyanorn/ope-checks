import numpy as np
from pytest import approx

from obd.tests.fixtures import campaign, rows


def test_rows_outside_the_week_are_counted_and_left_out():
    bts = rows(2, minute=0) + rows(1, minute=-0.001) + rows(1, minute=7 * 24 * 60)
    t, facts = campaign(rows(1, minute=0) + rows(1, minute=-5), bts)
    assert facts["rows_outside_week"] == {"random": 1, "bts": 2}
    assert (t.b_rows.sum(), t.r_rows.sum()) == (2, 1)


def test_rows_land_in_their_block_and_half():
    t, _ = campaign(rows(1, minute=57), rows(1, minute=52, item=1, position=3))
    assert t.r_rows[5, 1, 0, 0] == 1
    assert t.b_rows[5, 0, 1, 2] == 1


def test_resampling_scales_block_j_by_element_j():
    random = rows(2, clicks=1, minute=57) + rows(1, minute=0)
    t, _ = campaign(random, rows(3, clicks=2, p=0.25, minute=57) + rows(1, minute=0))
    m = np.ones(1008, int)
    m[5] = 3
    scaled = t.resample(m)
    assert (scaled.b_rows.sum(), scaled.b_rows[5].sum(), scaled.b_clicks[5]) == (10, 9, 6)
    assert (scaled.b_inv_p[5].sum(), scaled.b_inv_p_clicks[5]) == (36, 24)
    assert (scaled.r_rows.sum(), scaled.r_clicks.sum(), scaled.r_users.sum()) == (7, 3, 7)
    assert (scaled.g_rows.sum(), scaled.g_clicks.sum()) == (7, 3)
    assert (t.b_rows.sum(), t.g_rows.sum()) == (4, 3)


def test_propensity_facts():
    values = [0.000005, 0.00001, 1 / 34, 0.104925, 0.0005]
    bts = [{"minute": 0, "p": p, "click": int(p == 0.0005)} for p in values]
    _, facts = campaign(rows(1, minute=0), bts)
    assert facts["rows_below_1e-5"] == 1
    assert facts["rows_off_grid"] == 1
    assert facts["min_propensity"][0, 0] == 0.000005
    assert np.isinf(facts["min_propensity"][1, 0])
    assert facts["low_inv_p"] == approx(200_000 + 100_000 + 2000)
    assert facts["low_inv_p_clicks"] == approx(2000)
    assert facts["sum_inv_p_squared"] == approx(sum(1 / p**2 for p in values))


def users(*names):
    return [{"minute": 0, "user": (a, b, "-", "-")} for a, b in names]


def test_a_value_written_differently_in_the_two_files_is_matched():
    t, facts = campaign(users("ax", "qx"), users("ax", "zx", "zx"))
    assert facts["user_values_matched"] == [
        {
            "random": "q",
            "bts": "z",
            "share_of_random_rows": 0.5,
            "share_of_bts_rows": approx(2 / 3),
        },
        None,
        None,
        None,
    ]
    assert t.r_users.sum(axis=0).tolist() == [1, 1]
    assert t.b_users.sum(axis=0).tolist() == [1, 2]
    written = facts["users_as_written"]
    assert sorted(zip(written["random"].tolist(), written["bts"].tolist(), strict=True)) == [
        (0, 2),
        (1, 0),
        (1, 1),
    ]


def test_values_are_matched_only_when_each_log_has_exactly_one_of_its_own():
    t, facts = campaign(users("ax", "qx", "px"), users("ax", "zx"))
    assert facts["user_values_matched"] == [None, None, None, None]
    assert t.r_users.shape[1] == 4
    t, facts = campaign(users("ax", "qx"), users("ax", "qx"))
    assert facts["user_values_matched"] == [None, None, None, None]


def test_values_only_in_rows_outside_the_week_do_not_count():
    outside = [{"minute": -5, "user": ("w", "x", "-", "-")}]
    _, facts = campaign(users("ax", "qx") + outside, users("ax", "zx"))
    assert facts["user_values_matched"][0]["random"] == "q"
    _, facts = campaign(users("ax") + outside, users("ax"))
    assert facts["user_values_matched"] == [None, None, None, None]
