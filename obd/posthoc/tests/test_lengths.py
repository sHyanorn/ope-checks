import numpy as np
from pytest import approx

from obd import estimators as est
from obd import tables
from obd.posthoc import blocks, lengths
from obd.tests.fixtures import log
from obd.tests.synthetic import converted, raw_log, uniform

REGISTERED = {  # the name here, the name in `est.estimate` at a width of one hour
    "h3.ips": "h3.ips",
    "h4.rho": "h4.rho.1",
    "h4.d": "h4.d.1",
    "h5.after_minus_before": "h5.after_minus_before",
    "h6.ips": "h6.ips",
    "h6.snips": "h6.snips",
}


def campaign(seed, n_random=3000, n_bts=6000):
    rng = np.random.default_rng(seed)
    click_rate = np.array([0.2, 0.3, 0.4, 0.5])
    random = converted(raw_log(rng, n_random, uniform(4), click_rate))
    bts = converted(raw_log(rng, n_bts, rng.dirichlet(np.full(4, 5.0), 3), click_rate))
    return random, bts, rng.dirichlet(np.full(4, 5.0), 3).T


def registered(random, bts, pi0, drawn=None):
    """The registered estimate, on tables in which ten-minute block j counts drawn[j] times."""
    t, _ = tables.build(random, bts, np.full(len(pi0), 0.5))
    if drawn is not None:
        t = t.resample(drawn)
    got = est.estimate(t, pi0, 1, np.zeros(pi0.shape, bool))
    return {name: got[theirs] for name, theirs in REGISTERED.items()}


def test_sums_follow_the_clock_in_steps_of_five_minutes():
    random = [
        {"minute": 0, "item": 0, "click": 1},
        {"minute": 4.99, "item": 1, "position": 2, "click": 1},
        {"minute": 5, "item": 1},
    ]
    bts = [
        {"minute": 9.9, "item": 1, "position": 3, "click": 1, "p": 0.25},
        {"minute": 10, "p": 0.5},
        {"minute": 10079.9, "click": 1, "p": 0.1},
    ]
    s = lengths.sums(log(random), log(bts), 2)
    assert s["r_rows"].shape == s["r_clicks"].shape == s["b_rows"].shape == (2016, 2, 3)
    assert s["r_rows"][0].tolist() == [[1, 0, 0], [0, 1, 0]]
    assert s["r_clicks"][0].tolist() == [[1, 0, 0], [0, 1, 0]]
    assert s["r_rows"][1].tolist() == [[0, 0, 0], [1, 0, 0]] and s["r_clicks"][1].sum() == 0
    assert s["b_rows"][1, 1, 2] == 1 and s["b_rows"].sum() == 3
    assert s["b_clicks"][[1, 2, 2015]].tolist() == [1, 0, 1]
    assert s["b_inv_p"][[1, 2, 2015]].tolist() == approx([4, 2, 10])
    assert s["b_inv_p_clicks"][[1, 2, 2015]].tolist() == approx([4, 0, 10])


def test_quantities_on_the_full_data_are_the_registered_ones():
    random, bts, pi0 = campaign(11)
    got = lengths.quantities(lengths.sums(random, bts, 4), pi0, 1)
    assert got == approx(registered(random, bts, pi0), rel=1e-12)


def test_ten_minutes_is_the_registered_bootstrap():
    random, bts, pi0 = campaign(12)
    got = lengths.by_length(random, bts, pi0, 1, n_replicates=8)[10][1]
    for i in range(8):
        want = registered(random, bts, pi0, est.multiplicities(i))
        assert {name: x[i] for name, x in got.items()} == approx(want, rel=1e-12)


def test_a_longer_block_carries_all_its_ten_minute_blocks():
    random, bts, pi0 = campaign(13)
    got = lengths.by_length(random, bts, pi0, 1, n_replicates=4)
    for minutes in (20, 30, 60, 180):
        for i in range(4):
            drawn = np.repeat(blocks.multiplicities(minutes, i), minutes // 10)
            want = registered(random, bts, pi0, drawn)
            assert {name: x[i] for name, x in got[minutes][1].items()} == approx(want, rel=1e-12)


def test_five_minute_blocks_are_drawn_one_by_one():
    random, bts, pi0 = campaign(14)
    # rows in the second half of a ten-minute block are dropped, so that a
    # five-minute block is the whole of its ten-minute block
    random, bts = (x[x["timestamp"] % 600_000_000 < 300_000_000] for x in (random, bts))
    got = lengths.by_length(random, bts, pi0, 1, n_replicates=4)[5][1]
    for i in range(4):
        want = registered(random, bts, pi0, blocks.multiplicities(5, i)[0::2])
        assert {name: x[i] for name, x in got.items()} == approx(want, rel=1e-12)


def test_the_estimate_is_the_same_at_every_length():
    random, bts, pi0 = campaign(15)
    got = lengths.by_length(random, bts, pi0, 1, n_replicates=2)
    assert set(got) == set(blocks.MINUTES)
    for estimate, _ in got.values():
        assert estimate == approx(registered(random, bts, pi0), rel=1e-12)


def test_summary_gives_interval_and_spread_and_counts_undefined_replicates():
    replicates = {"h4.d": np.r_[np.arange(101.0), np.nan], "h6.ips": np.arange(102.0)}
    by_length = {
        10: ({"h4.d": 0.5, "h6.ips": 1.0}, replicates),
        60: ({"h4.d": 0.5, "h6.ips": 1.0}, {name: 2 * x for name, x in replicates.items()}),
    }
    got = lengths.summarise(by_length)
    assert got[10]["h4.d"] == {
        "estimate": 0.5,
        "interval": approx([2.5, 97.5]),
        "sd": approx(np.arange(101.0).std(ddof=1)),
        "sd_over_ten_minutes": 1,
        "undefined_replicates": 1,
    }
    assert got[60]["h4.d"]["interval"] == approx([5, 195])
    assert got[60]["h6.ips"]["sd_over_ten_minutes"] == approx(2)
    assert got[60]["h6.ips"]["undefined_replicates"] == 0


def test_the_pooled_unit_weights_the_campaigns_replicate_by_replicate():
    def one(value):
        return {
            m: (
                {"h3.ips": 1.0, "h4.rho": value, "h4.d": value / 2, "h6.ips": 9.0},
                {
                    "h3.ips": np.ones(3),
                    "h4.rho": value + np.arange(3.0),
                    "h4.d": value - np.arange(3.0),
                    "h6.ips": None,
                },
            )
            for m in blocks.MINUTES
        }

    got = lengths.pooled({"all": one(1.0), "women": one(3.0)}, {"all": 0.25, "women": 0.75})
    estimate, replicates = got[180]
    # H5 and H6 are not pooled
    assert estimate == {"h3.ips": approx(1), "h4.rho": approx(2.5), "h4.d": approx(1.25)}
    assert replicates["h4.rho"].tolist() == approx([2.5, 3.5, 4.5])
    assert replicates["h4.d"].tolist() == approx([2.5, 1.5, 0.5])
