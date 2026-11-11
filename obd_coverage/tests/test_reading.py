import numpy as np
import pytest

from obd_coverage import reading


def test_wilson_interval():
    assert reading.wilson(95, 100) == pytest.approx((0.8882, 0.9785), abs=2e-4)
    assert reading.wilson(3800, 4000) == pytest.approx((0.9428, 0.9563), abs=2e-4)


@pytest.mark.parametrize(
    "interval, expected",
    [
        ((0.94, 0.96), "adequate"),
        ((0.925, 0.975), "adequate"),
        ((0.90, 0.92), "under-covers"),
        ((0.98, 0.99), "over-covers"),
        ((0.92, 0.94), "unresolved"),
        ((0.96, 0.98), "unresolved"),
    ],
)
def test_labels(interval, expected):
    assert reading.label(interval) == expected


def test_a_cell_counts_the_intervals_that_contain_the_true_value():
    estimate = np.array([1.0, 1.1, 0.9, 1.2])
    low, high = estimate - 0.15, estimate + 0.15
    cell = reading.cell(estimate, low, high, np.full(4, 0.075), truth=1.0)
    assert cell["coverage"] == 0.75
    assert cell["interval_above_truth"] == 0.25 and cell["interval_below_truth"] == 0
    assert cell["mean_width"] == pytest.approx(0.3) and cell["median_width"] == pytest.approx(0.3)
    assert cell["sd_of_replicates_over_sd_of_estimate"] == pytest.approx(
        0.075 / estimate.std(ddof=1)
    )
    assert cell["coverage_of_mean_estimate"] == 1.0  # the mean estimate is 1.05
    assert cell["label"] == "unresolved" and cell["contains_nominal"]


def test_shortest_adequate_block():
    labels = dict(zip((5, 10, 20), ("under-covers", "adequate", "adequate"), strict=True))
    assert reading.shortest_adequate(labels) == (10, True)
    assert reading.shortest_adequate(labels | {20: "unresolved"}) == (10, False)
    assert reading.shortest_adequate(dict.fromkeys((5, 10), "under-covers")) == (None, False)


def test_spread():
    assert reading.spread(np.arange(101.0)) == {
        "mean": 50,
        "p2.5": 2.5,
        "median": 50,
        "p97.5": 97.5,
    }
