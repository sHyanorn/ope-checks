import numpy as np
from pytest import approx

from obd import estimators as est
from obd.posthoc import distances
from obd.tests.fixtures import log

P = np.array([[0.6, 0.5, 0.2], [0.4, 0.5, 0.8]])  # [item, position]
Q = np.array([[0.2, 0.5, 0.4], [0.8, 0.5, 0.6]])
TV_PQ = np.array([0.4, 0.0, 0.2])  # by position


def week(*blocks_of_an_hour, rows=(100, 100, 200)):
    """rows[block, item, position] of a week in which the hours repeat the given cycle.

    Each hour of the cycle is a list of six distributions [item, position], one per block.
    """
    hours = [blocks_of_an_hour[h % len(blocks_of_an_hour)] for h in range(168)]
    return np.array([p * np.array(rows) for hour in hours for p in hour])


def test_rows_by_block_counts_items_and_positions_on_the_clock():
    rows = [
        {"minute": 0, "item": 1, "position": 3},
        {"minute": 9.99, "item": 1, "position": 3},
        {"minute": 10, "item": 0, "position": 1},
        {"minute": 10079.9, "item": 0, "position": 2},
    ]
    got = distances.rows_by_block(log(rows)[distances.COLUMNS], 2)
    assert got.shape == (1008, 2, 3)
    assert got[0, 1, 2] == 2 and got[1, 0, 0] == 1 and got[1007, 0, 1] == 1
    assert got.sum() == 4


def test_one_distribution_all_week_is_at_its_distance_from_the_target_and_nowhere_else():
    got = distances.analyse(week([P] * 6), Q)
    by_position = np.array([100, 100, 200]) / 400
    assert got["d"] == approx((by_position * TV_PQ).sum())
    assert got["prior_to_week"] == approx(got["d"])
    assert got["hours_to_week"] == approx(0)
    assert got["d0"] == approx(0) and got["prior_to_week_reference"] == approx(0)
    assert got["first_hour"]["distance"] == approx(TV_PQ)
    assert got["first_hour"]["floor"] == approx([0, 0, 0])
    assert got["first_hour"]["rows"] == [600, 600, 1200]


def test_hours_that_alternate_around_the_target_are_far_from_it_while_the_week_is_not():
    middle = (P + Q) / 2
    got = distances.analyse(week([P] * 6, [Q] * 6), middle)
    by_position = np.array([100, 100, 200]) / 400
    assert got["prior_to_week"] == approx(0)
    assert got["hours_to_week"] == approx((by_position * TV_PQ / 2).sum())
    assert got["d"] == approx(got["hours_to_week"])
    assert got["d0"] == approx(0)


def test_the_two_relations_between_the_distances_hold():
    rng = np.random.default_rng(6)
    rows = rng.multinomial(50, rng.dirichlet(np.ones(5), 1008 * 3)).reshape(1008, 3, 5)
    rows = rows.transpose(0, 2, 1).astype(float)
    got = distances.analyse(rows, rng.dirichlet(np.ones(5), 3).T)
    assert got["left_out"] == 0
    assert got["prior_to_week"] <= got["d"] <= got["prior_to_week"] + got["hours_to_week"]


def test_blocks_that_alternate_within_every_hour_show_in_the_floors_only():
    got = distances.analyse(week([P, Q] * 3), (P + Q) / 2)
    by_position = np.array([100, 100, 200]) / 400
    assert got["d"] == approx(0) and got["hours_to_week"] == approx(0)
    assert got["d0"] == approx((by_position * TV_PQ).sum())
    assert got["prior_to_week_reference"] == approx(got["d0"])
    assert got["first_hour"]["floor"] == approx(TV_PQ)


def test_the_registered_quantities_come_from_the_registered_function():
    rng = np.random.default_rng(7)
    rows = rng.poisson(3.0, (1008, 4, 3)).astype(float)
    target = rng.dirichlet(np.ones(4), 3).T
    got, registered = distances.analyse(rows, target), est.h1(rows, target)
    assert (got["d"], got["d0"], got["left_out"]) == (
        registered["d"],
        registered["d0"],
        registered["left_out"],
    )
    assert got["first_hour"]["distance"] == registered["first_hour"]


def test_a_fixed_distribution_drawn_with_noise_stays_under_its_floor():
    rng = np.random.default_rng(8)
    policy = rng.dirichlet(np.full(20, 0.5), 3)  # [position, item]
    rows = np.stack(
        [rng.multinomial(40, p, 1008) for p in policy], axis=2
    )  # [block, item, position]
    got = distances.analyse(rows.astype(float), policy.T)
    assert 0.4 * got["d0"] < got["d"] < 0.7 * got["d0"]
    assert 0.4 * got["d0"] < got["hours_to_week"] < 0.7 * got["d0"]
    assert got["prior_to_week"] < 0.1 * got["d0"]
    assert got["prior_to_week"] == approx(got["prior_to_week_reference"] / 2, rel=0.5)
    for distance, floor in zip(
        got["first_hour"]["distance"], got["first_hour"]["floor"], strict=True
    ):
        assert distance < floor
