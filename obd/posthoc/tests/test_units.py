import numpy as np
import pytest
from pytest import approx

from obd import estimators as est
from obd import tables
from obd.posthoc import units
from obd.tests.fixtures import log
from obd.tests.synthetic import converted, raw_log, uniform


def at(second, **row):
    return {"minute": second / 60, **row}


def test_impressions_are_runs_in_time_order():
    rows = [at(2.5), at(0), at(1.3, user="b"), at(1.2), at(0.6), at(1.4)]
    assert units.impressions(log(rows)).tolist() == [3, 0, 1, 0, 0, 2]


def test_an_impression_ends_after_a_full_second_or_a_change_in_any_user_feature():
    rows = [at(0), at(0.5), at(1.5), at(1.6, user=("a", "-", "-", "x")), at(1.7)]
    assert units.impressions(log(rows)).tolist() == [0, 0, 1, 2, 3]


def test_rows_with_one_timestamp_keep_their_file_order():
    rows = [at(0), at(0, user="b"), at(0)]
    assert units.impressions(log(rows)).tolist() == [0, 1, 2]


def test_resamples_draw_each_distinct_row_in_proportion_to_its_count():
    kinds = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    sums = units.resampled(kinds, np.random.default_rng(0), 20_000)
    assert (sums.sum(axis=1) == 4).all()
    assert sums[:, 0].mean() == approx(1, abs=0.03)
    assert sums[:, 0].var() == approx(4 * 0.25 * 0.75, abs=0.03)


def test_resampled_sums_spread_like_sums_of_drawn_units():
    values = np.random.default_rng(1).normal(size=(50, 1))
    sums = units.resampled(values, np.random.default_rng(2), 20_000)
    assert sums.shape == (20_000, 1)
    assert sums.mean() == approx(values.sum(), abs=0.2)
    assert sums.std() == approx(50**0.5 * values.std(), rel=0.03)


def test_ratios():
    got = units.ratios(np.array([6.0, 12.0, 10.0]), np.array([3.0, 5.0]))
    assert got == {"ips": approx(1.0), "snips": approx(0.5 / 0.6)}


def test_blocks_are_the_registered_bootstrap():
    rng = np.random.default_rng(3)
    click_rate = np.array([0.2, 0.3, 0.4, 0.5])
    random = converted(raw_log(rng, 3000, uniform(4), click_rate))
    bts = converted(raw_log(rng, 6000, rng.dirichlet(np.full(4, 5.0), 3), click_rate))
    pi0 = rng.dirichlet(np.full(4, 5.0), 3).T
    t, _ = tables.build(random, bts, np.full(4, 0.5))
    registered = [
        est.estimate(t.resample(est.multiplicities(i)), pi0, 1, np.zeros(pi0.shape, bool))
        for i in range(30)
    ]
    got = units.h3_by_unit(random, bts, pi0, 0, n_replicates=30)["blocks"]
    for name in ("ips", "snips"):
        replicates = [r[f"h3.{name}"] for r in registered]
        assert got[name]["interval"] == approx(np.percentile(replicates, [2.5, 97.5]))
        assert got[name]["sd"] == approx(np.std(replicates, ddof=1))
        full = est.estimate(t, pi0, 1, np.zeros(pi0.shape, bool))
        assert got[name]["estimate"] == approx(full[f"h3.{name}"])


def test_rows_that_click_together_widen_the_interval_of_larger_units():
    clicked = np.random.default_rng(4).random(2000) < 0.3
    random = [
        at(300 * i, position=k, click=click) for i, click in enumerate(clicked) for k in (1, 2, 3)
    ]
    bts = [at(600 * block, click=1) for block in range(1008)]  # on-policy value 1 in any resample
    got = units.h3_by_unit(log(random), log(bts), np.full((2, 3), 0.5), 0, n_replicates=2000)
    assert got["rows"]["units"] == {"random": 6000, "bts": 1008}
    assert got["impressions"]["units"]["random"] == 2000
    assert got["impressions"]["ips"]["sd"] / got["rows"]["ips"]["sd"] == approx(3**0.5, rel=0.1)
    assert got["sd_of_blocks_over"]["rows"]["ips"] == approx(3**0.5, rel=0.1)
    assert got["sd_of_blocks_over"]["impressions"]["ips"] == approx(1, rel=0.1)


def impression(second, items, positions=(1, 2, 3)):
    return [at(second, item=item, position=k) for item, k in zip(items, positions, strict=True)]


def test_list_reuse_compares_consecutive_complete_impressions():
    rows = (
        impression(0, (1, 2, 3))
        + impression(10, (1, 2, 3), positions=(1, 1, 2))  # not complete, passed over
        + impression(20, (1, 2, 3))
        + impression(30, (3, 2, 1))
        + impression(40, (3, 2, 1))
    )
    frame = log(rows)
    assert units.list_reuse(frame, units.impressions(frame)) == {
        "impressions": 5,
        "complete_impressions": 4,
        "same_list_as_previous": approx(2 / 3),
    }


def test_variance_ratio_of_one_pair_of_blocks():
    start = np.array([0, 1, 60, 61, 120, 121, 300]) * 1_000_000
    clicks, rows = np.array([1.0, 0, 0, 0, 1, 1, 1]), np.ones(7)
    # First pair: rates 0.5 and 0; variances 2 x (0.25 + 0.25) / 4 and 0. The third
    # block faces an empty one and the sixth holds one impression: both pairs are left out.
    assert units.variance_ratio(start, clicks, rows, 1) == approx(0.25 / 0.25)
    assert units.variance_ratio(start[:6], clicks[:6], rows[:6], 1, False) == approx(0.25 / 0.125)


def independent(rng, n):
    start = rng.integers(0, 7 * 24 * 3600 * 1_000_000, n)
    return start, (rng.random(n) < 0.3).astype(float), np.ones(n)


def test_variance_ratio_is_one_for_independent_rows_and_larger_when_blocks_differ():
    rng = np.random.default_rng(5)
    start, clicks, rows = independent(rng, 200_000)
    by_block = 0.2 + 0.2 * (start // 600_000_000 % 2)
    assert units.variance_ratio(start, clicks, rows, 10) == approx(1, abs=0.2)
    assert units.variance_ratio(start, (rng.random(200_000) < by_block) * 1.0, rows, 10) > 5


def test_variance_ratio_is_one_for_independent_rows_in_sparse_blocks():
    start, clicks, rows = independent(np.random.default_rng(6), 5000)  # five to a block
    assert units.variance_ratio(start, clicks, rows, 10) == approx(1, abs=0.2)
    assert units.variance_ratio(start, clicks, rows, 10, False) > 1.4


@pytest.mark.filterwarnings("ignore::RuntimeWarning")  # no complete impression, empty blocks
def test_dependence_also_measures_clicks_net_of_their_item_and_position():
    clicks = {0: [(0, 1), (0, 0), (1, 0)], 60: [(0, 1), (1, 0), (1, 0)]}
    rows = [
        at(second + 2 * i, item=item, click=click)
        for second, block in clicks.items()
        for i, (item, click) in enumerate(block)
    ]
    # Both blocks have a click rate of 1/3; item 0 has 2/3 and item 1 has 0. Net of
    # these the rates are -1/9 and 1/9 and the variances 3/2 x 42/729 and 3/2 x 6/729.
    assert units.dependence(log(rows))["variance_ratio"][1] == {
        "clicks": approx(0),
        "residuals": approx(0.5),
        "clicks_without_factor": approx(0),
    }


@pytest.mark.filterwarnings("ignore::RuntimeWarning")  # no complete impression, empty blocks
def test_an_impression_belongs_to_the_block_of_its_first_row():
    rows = [at(10), at(59.8, click=1), at(60.3), at(70), at(80)]
    # First minute: impressions of (1 click, 2 rows) and (0, 1), rate 1/3, variance
    # 2 x (1/9 + 1/9) / 9. Second minute: two impressions without a click.
    assert units.dependence(log(rows))["variance_ratio"][1]["clicks"] == approx(2.25)
