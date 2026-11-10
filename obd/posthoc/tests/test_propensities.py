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
    + rows(1, minute=DAY, item=1, p=0.0004, position=2)
)


def test_cell_sums():
    sums = propensities.cell_sums(log(BTS), 2)
    assert sums["rows"].shape == sums["inv_p"].shape == (1008, 2, 3)
    assert sums["rows"][0, :, 0].tolist() == [2, 1]
    assert sums["inv_p"][144, 1].tolist() == [4, 2500, 0]
    assert sums["min_p"][:, :2].tolist() == [[0.5, np.inf], [0.25, 0.0004]]
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


def test_absent_is_the_share_of_the_position_in_hours_without_the_cell():
    bts = rows(1, minute=0, item=0) + rows(1, minute=0, item=1) + rows(2, minute=HOUR, item=1)
    gone = propensities.absent(propensities.cell_sums(log(bts), 2)["rows"])
    assert gone[:, 0].tolist() == [0.5, 0]


def test_analysis_by_bound_and_cell():
    out = propensities.analyse(log(BTS), 2, n_replicates=5)
    assert [out["by_bound"][bound]["cells"] for bound in propensities.BOUNDS] == [2, 2, 3]
    assert out["by_bound"][0.001]["share_of_rows"] == approx(4 / 5)
    assert out["by_bound"][0.001]["m"]["estimate"] == approx((4 / 4 + 8 / 4) / 2)
    assert len(out["by_bound"][0.001]["m_by_day"]) == 7
    assert out["by_bound"][0.001]["m_by_day"][1]["estimate"] == approx((0 + 4) / 2)
    assert out["by_bound"][0.001]["grid_bias"] == approx(
        (2 * 0.5 / 0.25 + 2 * 0.75 / 0.0625) / 200_000 / 4 / 2
    )
    assert out["by_bound"][0.001]["absent"] == approx((1 / 4 + 0) / 2)
    assert [(c["item"], c["position"]) for c in out["cells"]] == [(0, 1), (1, 1), (1, 2)]
    assert out["cells"][2] == {
        "item": 1,
        "position": 2,
        "rows": 1,
        "min_propensity": 0.0004,
        "s": approx(2500),
        "grid_bias": approx(0.9996 / (200_000 * 0.0004**2)),
        "absent": 0,
    }
