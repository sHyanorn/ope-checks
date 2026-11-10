import numpy as np
from pytest import approx

from obd import tables
from obd.posthoc import features
from obd.tests.fixtures import log


def users(*names):
    return log([{"minute": 0, "user": (a, b, "-", "-")} for a, b in names])


RANDOM = users("xp", "xp", "ac")


def test_one_log_values_and_the_rows_they_mark():
    found = features.one_log_values(RANDOM, users("yq", "yq", "ac", "ar"))
    assert found["matched_features"] == ["user_feature_0"]
    assert found["rows_marked"] == {"random": 2, "bts": 2}
    assert found["values"]["user_feature_1"] == [
        {
            "log": "random",
            "value": "p",
            "rows": 2,
            "share_of_rows": approx(2 / 3),
            "rows_marked": 2,
        },
        {"log": "bts", "value": "q", "rows": 2, "share_of_rows": 0.5, "rows_marked": 2},
        {"log": "bts", "value": "r", "rows": 1, "share_of_rows": 0.25, "rows_marked": 0},
    ]
    assert found["values"]["user_feature_2"] == []


def test_values_that_hold_exactly_the_marked_rows_are_paired():
    found = features.one_log_values(RANDOM, users("yq", "yq", "ac", "ar"))
    assert features.same_category(found) == {"user_feature_1": {"random": "p", "bts": "q"}}


def test_no_pair_when_two_values_share_the_marked_rows():
    found = features.one_log_values(RANDOM, users("yq", "ys", "ac"))
    assert features.same_category(found) == {}


def test_no_pair_when_a_value_holds_only_part_of_the_marked_rows():
    found = features.one_log_values(RANDOM, users("yq", "yc", "ac"))
    assert features.same_category(found) == {}


def test_no_pair_when_a_value_also_holds_unmarked_rows():
    found = features.one_log_values(RANDOM, users("yq", "yq", "aq"))
    assert features.same_category(found) == {}


def test_the_registered_code_takes_a_rewritten_pair_as_one_value():
    bts = users("yq", "yq", "ac", "ar")
    alpha = beta = np.ones(3)

    def distance(random):
        return features.quantities(random, bts, alpha, beta, 0, 3)["h7.tv.feature_1"]["estimate"]

    pairs = {"user_feature_1": {"random": "p", "bts": "q"}}
    assert distance(RANDOM) == approx(0.75)  # p, q and r each in one log only
    assert distance(features.rewritten(RANDOM, pairs)) == approx(0.25)
    assert (
        tables.build(features.rewritten(RANDOM, pairs), bts, alpha)[1]["user_values_matched"][1]
        is None
    )
