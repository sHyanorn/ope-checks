import numpy as np

from obd.posthoc import prior


def test_shared_pairs_are_counted_with_their_order():
    a = (np.array([1.0, 2.0, 3.0, 4.0]), np.array([9.0, 8.0, 7.0, 6.0]))
    b = (np.array([2.0, 4.0]), np.array([8.0, 6.0]))  # the second and fourth pair of a, in order
    c = (np.array([4.0, 2.0, 5.0]), np.array([6.0, 8.0, 1.0]))  # two pairs of a, reversed
    got = prior.shared_pairs({"a": a, "b": b, "c": c})
    assert got["pairs"] == {"a": 4, "b": 2, "c": 3}
    assert got["distinct"] == {"a": True, "b": True, "c": True}
    assert got["shared"]["b"]["a"] == {"pairs": 2, "same_order": True}
    assert got["shared"]["a"]["b"] == {"pairs": 2, "same_order": True}
    assert got["shared"]["c"]["a"] == {"pairs": 2, "same_order": False}
    assert got["shared"]["c"]["b"] == {"pairs": 2, "same_order": False}


def test_a_pair_is_shared_only_if_both_parameters_are_equal():
    a = (np.array([1.0, 2.0]), np.array([5.0, 6.0]))
    b = (np.array([1.0, 2.0]), np.array([6.0, 5.0]))
    got = prior.shared_pairs({"a": a, "b": b})
    assert got["shared"]["a"]["b"] == {"pairs": 0, "same_order": True}


def test_a_repeated_pair_is_reported_as_not_distinct():
    a = (np.array([1.0, 1.0, 2.0]), np.array([5.0, 5.0, 6.0]))
    b = (np.array([1.0]), np.array([5.0]))
    got = prior.shared_pairs({"a": a, "b": b})
    assert got["distinct"] == {"a": False, "b": True}
    assert got["shared"]["a"]["b"]["pairs"] == 2 and got["shared"]["b"]["a"]["pairs"] == 1
