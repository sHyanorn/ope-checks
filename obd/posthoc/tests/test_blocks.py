import numpy as np
from pytest import approx

from obd import estimators as est
from obd import tables
from obd.posthoc import blocks
from obd.tests.fixtures import log
from obd.tests.synthetic import converted, raw_log, uniform


def test_multiplicities_draw_as_many_blocks_as_the_week_holds():
    for minutes, n in zip(blocks.MINUTES, (2016, 1008, 504, 336, 168, 56), strict=True):
        drawn = blocks.multiplicities(minutes, 7)
        assert drawn.shape == (n,)
        assert drawn.sum() == n


def test_multiplicities_at_ten_minutes_are_the_registered_ones():
    assert (blocks.multiplicities(10, 3) == est.multiplicities(3)).all()


def test_multiplicities_depend_on_the_length_and_on_the_replicate():
    assert (blocks.multiplicities(20, 0) == blocks.multiplicities(20, 0)).all()
    assert (blocks.multiplicities(20, 0) != blocks.multiplicities(20, 1)).any()
    # a stream that ignored the length would repeat the first 168 draws of a longer one
    first = np.random.default_rng([20261110, 3, 60, 0]).multinomial(168, np.full(168, 1 / 168))
    assert (blocks.multiplicities(60, 0) == first).all()
    other = np.random.default_rng([20261110, 3, 30, 0]).multinomial(168, np.full(168, 1 / 168))
    assert (first != other).any()


def test_block_sums_follow_the_clock_from_the_start_of_the_week():
    random = [
        {"minute": 0, "item": 0, "click": 1},
        {"minute": 4.99, "item": 1, "click": 1},
        {"minute": 5, "item": 1},
        {"minute": 185, "item": 0, "click": 1},
    ]
    bts = [{"minute": 19.9, "click": 1}, {"minute": 20}, {"minute": 10079.9, "click": 1}]
    pi0 = np.array([[0.25, 0.5, 0.5], [0.75, 0.5, 0.5]])  # weights 0.5 and 1.5 at position 1
    r, b = blocks.block_sums(log(random), log(bts), pi0, 5)
    assert r.shape == (2016, 3) and b.shape == (2016, 2)
    assert r[0].tolist() == [2.0, 2.0, 2.0]
    assert r[1].tolist() == [0.0, 1.5, 1.0]
    assert r[37].tolist() == [0.5, 0.5, 1.0]
    assert b[3].tolist() == [1.0, 1.0] and b[4].tolist() == [0.0, 1.0]
    assert b[2015].tolist() == [1.0, 1.0]
    r, b = blocks.block_sums(log(random), log(bts), pi0, 180)
    assert r.shape == (56, 3)
    assert r[0].tolist() == [2.0, 3.5, 3.0] and r[1].tolist() == [0.5, 0.5, 1.0]
    assert b[0].tolist() == [1.0, 2.0] and b[55].tolist() == [1.0, 1.0]


def test_ten_minutes_is_the_registered_bootstrap():
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
    full = est.estimate(t, pi0, 1, np.zeros(pi0.shape, bool))
    got = blocks.summarise(blocks.h3_by_length(random, bts, pi0, n_replicates=30))
    for minutes in blocks.MINUTES:
        assert got[minutes]["blocks"] == 10080 // minutes
        for name in ("ips", "snips"):
            assert got[minutes][name]["estimate"] == approx(full[f"h3.{name}"])
    for name in ("ips", "snips"):
        replicates = [r[f"h3.{name}"] for r in registered]
        assert got[10][name]["interval"] == approx(np.percentile(replicates, [2.5, 97.5]))
        assert got[10][name]["sd"] == approx(np.std(replicates, ddof=1))
        assert got[10][name]["sd_over_ten_minutes"] == 1


def sd_over_ten_minutes(clicks):
    """Of the IPS ratio, for a random log of one row a minute and an on-policy value of 1."""
    random = [{"minute": i, "click": int(click)} for i, click in enumerate(clicks)]
    bts = [{"minute": 5 * block, "click": 1} for block in range(2016)]
    by_length = blocks.h3_by_length(log(random), log(bts), np.full((2, 3), 0.5), n_replicates=2000)
    return {m: x["ips"]["sd_over_ten_minutes"] for m, x in blocks.summarise(by_length).items()}


def test_independent_rows_give_one_width_at_every_length():
    got = sd_over_ten_minutes(np.random.default_rng(4).random(10080) < 0.3)
    for minutes in (5, 20, 30, 60):
        assert got[minutes] == approx(1, rel=0.15)
    assert got[180] == approx(1, rel=0.3)  # 56 blocks


def test_clicks_that_come_by_the_hour_widen_the_interval_up_to_the_hour():
    got = sd_over_ten_minutes(np.repeat(np.random.default_rng(5).random(168) < 0.3, 60))
    assert got[5] == approx(0.5**0.5, rel=0.1)
    assert got[30] == approx(3**0.5, rel=0.1)
    assert got[60] == approx(6**0.5, rel=0.15)
    assert got[180] == approx(6**0.5, rel=0.3)


def test_the_pooled_unit_is_combined_replicate_by_replicate():
    def campaign(value):
        return {
            m: ({"ips": value, "snips": 2 * value}, {"ips": value + np.arange(3.0), "snips": None})
            for m in blocks.MINUTES
        }

    by_campaign = {"all": campaign(1.0), "women": campaign(3.0)}
    for c in by_campaign:
        for m in blocks.MINUTES:
            by_campaign[c][m][1]["snips"] = by_campaign[c][m][1]["ips"] * (1 if c == "all" else -1)
    got = blocks.pooled(by_campaign, {"all": 0.25, "women": 0.75})
    assert set(got) == set(blocks.MINUTES)
    estimate, replicates = got[60]
    assert estimate == {"ips": approx(2.5), "snips": approx(5.0)}
    assert replicates["ips"].tolist() == approx([2.5, 3.5, 4.5])
    # opposite movements partly cancel within a replicate
    assert replicates["snips"].tolist() == approx([-2.0, -2.5, -3.0])
