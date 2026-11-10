import numpy as np
from pytest import approx

from obd import estimators as est
from obd.posthoc import propensities
from obd.tests.fixtures import campaign, log, rows

HOUR, DAY = 60, 24 * 60
BTS = (
    rows(2, minute=0, item=0, p=0.5)
    + rows(1, minute=0, item=1, p=0.25)
    + rows(1, minute=DAY, item=1, p=0.25)
    + rows(1, minute=DAY, item=1, p=0.0005, position=2)
)


def test_cell_sums():
    sums = propensities.cell_sums(log(BTS), 2)
    assert sums["rows"].shape == sums["inv_p"].shape == (1008, 2, 3)
    assert sums["rows"][0, :, 0].tolist() == [2, 1]
    assert sums["inv_p"][144, 1].tolist() == [4, 2000, 0]
    assert sums["min_p"][:, :2].tolist() == [[0.5, np.inf], [0.25, 0.0005]]
    # two rows at 0.5 among the four rows of position 1
    assert sums["grid_bias"][0, 0] == approx(2 * 0.5 / (200_000 * 0.25) / 4)


def test_statistic_follows_the_multiplicities():
    sums = propensities.cell_sums(log(BTS), 2)
    m = np.ones((2, 1008))
    m[1, 0] = 3
    s = propensities.statistic(sums["inv_p"], sums["rows"], m)
    assert s[0, :, 0].tolist() == [approx(4 / 4), approx(8 / 4)]
    assert s[1, :, 0].tolist() == [approx(12 / 10), approx(16 / 10)]


def test_mean_s_is_the_registered_m_with_the_registered_interval():
    bts = BTS + rows(3, minute=7, item=1, p=0.3) + rows(2, minute=5000, item=0, p=0.7)
    t, facts = campaign(rows(1, minute=0), bts)
    eligible = est.eligible_cells(facts["min_propensity"])
    multiplicities = np.array([est.multiplicities(i) for i in range(40)])
    registered = [
        est.estimate(t.resample(m), np.full((2, 3), 0.5), 1, eligible)["h2.m"]
        for m in multiplicities
    ]
    sums = propensities.cell_sums(log(bts), 2)
    got = propensities.mean_s(sums["inv_p"], sums["rows"], eligible, multiplicities)
    assert eligible.sum() == 2
    assert got["estimate"] == approx(est.estimate(t, np.full((2, 3), 0.5), 1, eligible)["h2.m"])
    assert got["interval"] == approx(np.nanpercentile(registered, [2.5, 97.5]))
    assert got["undefined_replicates"] == np.isnan(registered).sum() > 0


def test_mean_s_of_a_day_uses_the_blocks_of_that_day():
    sums = propensities.cell_sums(log(BTS), 2)
    cells = np.array([[True, False, False], [True, False, False]])
    ones = np.ones((1, 1008))
    day = [
        propensities.mean_s(sums["inv_p"], sums["rows"], cells, ones, slice(144 * d, 144 * d + 144))
        for d in (0, 1)
    ]
    assert day[0]["estimate"] == approx((4 / 3 + 4 / 3) / 2)
    assert day[1]["estimate"] == approx((0 + 4) / 2)


def test_low_hours_and_the_part_of_the_shortfall_they_account_for():
    # Position 1 has 4 rows in the first hour and 12 in the second. Item 0 takes half
    # of the first hour as its propensity says, and 1 row of the second at 0.5.
    bts = (
        rows(2, minute=0, item=0, p=0.5)
        + rows(2, minute=5, item=1, p=0.5)
        + rows(1, minute=HOUR, item=0, p=0.5)
        + rows(11, minute=HOUR + 15, item=1, p=0.5)
    )
    sums = propensities.cell_sums(log(bts), 2)
    inv_p, n = propensities.hourly(sums["inv_p"]), propensities.hourly(sums["rows"])
    low, shortfall = propensities.low_hours(inv_p, n, 0.5)
    assert low[:2, 0, 0].tolist() == [False, True]  # hourly S of 1 and of 2/12
    assert shortfall[:2, 0, 0].tolist() == [0, approx(12 / 16 * (1 - 2 / 12))]
    assert not propensities.low_hours(inv_p, n, 0.1)[0].any()
    assert not low[2:].any()  # hours without rows are not low


def test_analysis_by_bound_and_cell():
    bts = BTS + rows(8, minute=HOUR, item=1, p=0.25)  # an hour without item 0
    out = propensities.analyse(log(bts), 2, n_replicates=5)
    at_bound = out["by_bound"][0.001]
    assert [out["by_bound"][bound]["cells"] for bound in propensities.BOUNDS] == [2, 3, 3]
    assert at_bound["share_of_rows"] == approx(12 / 13)
    assert at_bound["m"]["estimate"] == approx((4 / 12 + 40 / 12) / 2)
    assert len(at_bound["m_by_day"]) == 7
    assert at_bound["m_by_day"][1]["estimate"] == approx((0 + 4) / 2)
    assert at_bound["grid_bias"] == approx((2 * 0.5 / 0.25 + 10 * 0.75 / 0.0625) / 200_000 / 12 / 2)
    # item 0 is missing from the second hour (8 rows of 12) and from the second day (1 of 12)
    assert at_bound["shortfall_in_low_hours"][0.1]["mean"] == approx((9 / 12 + 0) / 2)
    assert at_bound["shortfall_in_low_hours"][0.1]["by_day"][:2] == [
        approx(8 / 12 / 2),
        approx(1 / 12 / 2),
    ]
    assert [(c["item"], c["position"]) for c in out["cells"]] == [(0, 1), (1, 1), (1, 2)]
    assert out["cells"][0]["low_hours"][0.1] == {
        "hours": 2,
        "rows": 0,
        "rows_of_position": 9,
        "harmonic_mean_propensity": None,
        "shortfall": approx(9 / 12),
    }
    assert out["cells"][2] == {
        "item": 1,
        "position": 2,
        "rows": 1,
        "min_propensity": 0.0005,
        "s": approx(2000),
        "grid_bias": approx(0.9995 / (200_000 * 0.0005**2)),
        "low_hours": {
            below: {
                "hours": 0,
                "rows": 0,
                "rows_of_position": 0,
                "harmonic_mean_propensity": None,
                "shortfall": 0,
            }
            for below in propensities.LOW
        },
    }


def test_a_low_hour_with_rows_reports_their_recorded_propensity():
    bts = rows(1, minute=0, item=0, p=0.5) + rows(39, minute=0, item=1, p=0.5)
    cell = propensities.analyse(log(bts), 2, n_replicates=2)["cells"][0]
    assert cell["low_hours"][0.1] == {
        "hours": 1,
        "rows": 1,
        "rows_of_position": 40,
        "harmonic_mean_propensity": 0.5,
        "shortfall": approx(1 - 2 / 40),
    }
