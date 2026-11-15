"""T8, the rules: shares, ties, removed runs and labels as Section 8 counts them."""

import numpy as np
import pytest

from obd_rescore import rules


def runs(y_closer, x_closer, ties=0, removed=0):
    """Estimates y and x against a reference 0, in that many runs of each kind."""
    y = [0.1] * y_closer + [0.3] * x_closer + [0.2] * ties + [np.nan] * removed
    x = [0.2] * (y_closer + x_closer + ties + removed)
    return np.array(y), np.array(x)


@pytest.mark.parametrize(
    ("n", "k", "label"),
    [
        (500, 271, "undecided"),
        (500, 272, "holds"),
        (2000, 1043, "undecided"),
        (2000, 1044, "holds"),
    ],
)
def test_a_majority_needs_the_registered_number_of_runs(n, k, label):
    assert rules.compare(*runs(k, n - k), 0)["label"] == label
    assert rules.compare(*reversed(runs(k, n - k)), 0)["label"] == label.replace("holds", "flips")


def test_the_wilson_interval_has_the_registered_z():
    low, high = rules.wilson(0, 10)
    assert low == pytest.approx(0, abs=1e-12)
    assert high == pytest.approx(0.277532, abs=1e-6)
    assert rules.wilson(272, 500)[0] == pytest.approx(0.500174, abs=1e-6)


def test_ties_count_in_both_denominators():
    out = rules.compare(*runs(271, 0, ties=229), 0)
    assert (out["y_closer"], out["x_closer"], out["ties"]) == (271, 0, 229)
    assert (out["p"], out["q"]) == (271 / 500, 0)
    assert out["label"] == "undecided"
    out = rules.compare(*runs(0, 271, ties=229), 0)
    assert (out["q"], out["label"]) == (271 / 500, "undecided")


def test_a_reference_per_run_is_compared_run_by_run():
    y, x = np.array([1.0, 1.0]), np.array([2.0, 2.0])
    out = rules.compare(y, x, np.array([0.0, 3.0]))
    assert (out["y_closer"], out["x_closer"]) == (1, 1)


def test_runs_that_are_not_finite_are_removed_and_counted():
    out = rules.compare(*runs(272, 223, removed=5), 0)
    assert (out["removed"], out["p"], out["label"]) == (5, 272 / 495, "holds")
    assert rules.compare(*runs(270, 225, removed=5), 0)["label"] == "holds"  # p_L over 495
    assert rules.compare(*runs(272, 222, removed=6), 0)["label"] == "not evaluable"
    y, x = runs(300, 200)
    x[:6] = np.nan
    assert (rules.compare(y, x, 0)["removed"], rules.compare(y, x, 0)["label"]) == (
        6,
        "not evaluable",
    )
    y, x = runs(300, 200)
    reference = np.zeros(500)
    reference[:6] = np.inf
    assert rules.compare(y, x, reference)["removed"] == 6
    assert rules.compare(y, x, reference)["label"] == "not evaluable"


def test_labels_across_estimators_and_references():
    assert rules.across_estimators(["holds", "not evaluable", "flips"]) == "flips"
    assert rules.across_estimators(["flips", "holds"]) == "flips"
    assert rules.across_estimators(["holds", "not evaluable", "undecided"]) == "not evaluable"
    assert rules.across_estimators(["not evaluable", "holds"]) == "not evaluable"
    assert rules.across_estimators(["holds", "undecided"]) == "undecided"
    assert rules.across_estimators(["holds"] * 5) == "holds"
    assert rules.across_references("flips", "flips") == "flips"
    assert rules.across_references("not evaluable", "holds") == "not evaluable"
    assert rules.across_references("holds", "not evaluable") == "not evaluable"
    assert rules.across_references("flips", "undecided") == "references differ"


def test_the_interval_of_blue_minus_ips():
    ips = np.zeros(101)
    out = rules.unbiasedness(np.arange(101.0) - 2.5, ips)
    assert (out["interval"], out["label"]) == ([0.0, 95.0], "not contradicted")
    assert rules.unbiasedness(2.5 - np.arange(101.0), ips)["interval"] == [-95.0, 0.0]
    assert rules.unbiasedness(2.5 - np.arange(101.0), ips)["label"] == "not contradicted"
    assert rules.unbiasedness(np.arange(101.0) - 2.4, ips)["label"] == "contradicted"
    blue = np.arange(4.0)
    linear = pytest.approx([0.075, 2.925], rel=1e-12)
    assert rules.unbiasedness(blue, np.zeros(4))["interval"] == linear
    for removed, label in [(20, "not contradicted"), (21, "not evaluable")]:
        ips = np.where(np.arange(2000) < removed, np.nan, 0.0)
        out = rules.unbiasedness(np.linspace(-1, 1, 2000), ips)
        assert (out["removed"], out["label"]) == (removed, label)
    out = rules.unbiasedness(np.r_[np.inf, np.zeros(100)], np.r_[np.inf, np.zeros(100)])
    assert out["removed"] == 1


@pytest.mark.parametrize(
    ("k", "farther", "label"),
    [
        (111, 39, "reproduced"),
        (129, 21, "reproduced"),
        (110, 40, "published share not reproduced"),
        (130, 20, "published share not reproduced"),
        (129, 20, "published share not reproduced"),  # one run removed: p = 129 / 149
        (110, 39, "reproduced"),  # p = 110 / 149, 0.0617 below 0.8
        (120, 28, "not evaluable"),  # two runs removed
    ],
)
def test_the_replication_of_c1(k, farther, label):
    comparison = rules.compare(*runs(k, farther, removed=150 - k - farther), 0)
    assert rules.replication_c1(comparison) == label


@pytest.mark.parametrize(
    ("p", "label"),
    [(0.865, "reproduced"), (0.8651, "published share not reproduced")],
)
def test_the_tolerance_of_the_c1_replication_is_0_065(p, label):
    assert rules.replication_c1({"label": "holds", "p": p}) == label


def test_the_replication_of_c2():
    published = {"BLUE": 0.006687691524532561, "V": 1.0}
    close = {"BLUE": published["BLUE"] * (1 + 0.9e-6), "V": 1 - 0.9999995e-6}
    assert rules.replication_c2(close, published)["label"] == "reproduced"  # relative to printed
    far = close | {"V": 1 - 1.1e-6}
    out = rules.replication_c2(far, published)
    assert out["label"] == "not reproduced"
    assert out["differences"]["V"] == pytest.approx(-1.1e-6)
