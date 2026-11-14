import json

import numpy as np
import pytest

from obd_coverage import run
from obd_coverage.intervals import QUANTITIES, UNITS
from obd_coverage.tests import small

TARGET = small.TARGET


@pytest.fixture(scope="module")
def calibrated():
    logs, clicks, _ = small.logs(0, n_random=60_000, n_bts=300_000)
    calibration = run.calibrate(logs, clicks, TARGET, "all")
    return logs, json.loads(json.dumps(calibration, default=lambda x: x.tolist()))


def test_the_calibrated_model_expects_the_published_numbers(calibrated):
    _, calibration = calibrated
    expected = calibration["predicted"]["M"]["ips_ratio"]["bootstrap_variance"]
    assert (expected["impressions"] / expected["rows"]) ** 0.5 == pytest.approx(1.05)
    expected = calibration["predicted"]["H"]["ips_ratio"]["bootstrap_variance"]
    assert (expected["180"] / expected["10"]) ** 0.5 == pytest.approx(1.04)
    assert calibration["session"]["bts"]["minutes"] in run.model.SPANS


def test_a_strength_that_would_break_the_nesting_is_cut_back_and_noted(calibrated):
    _, calibration = calibrated
    e_s = min(calibration["session"][log]["e"] for log in run.LOGS)
    day = calibration["long"]["1440"]
    assert 0 < calibration["long"]["60"]["e"] < e_s
    assert day["solved"] > e_s and day["e"] == e_s
    assert calibration["notes"] == [
        f"e_L at 1440 minutes solved as {day['solved']:.4g}, set to {e_s:.4g}"
    ]


def test_scenarios_share_their_true_values_unless_the_click_rate_drifts(calibrated):
    _, calibration = calibrated
    truth = calibration["truth"]
    assert truth["A"] == truth["I"] == truth["M"] == truth["H"] == truth["U"]
    assert truth["D"]["v_on"] == pytest.approx(truth["A"]["v_on"], rel=0.05)
    assert truth["D"] != truth["A"]
    assert np.mean(calibration["drift_by_hour"]) == pytest.approx(1, abs=0.05)


def test_predictions_follow_the_structure_of_each_scenario(calibrated):
    _, calibration = calibrated

    def coverage(scenario, unit, quantity="ips_ratio"):
        return calibration["predicted"][scenario][quantity]["coverage"][str(unit)]

    assert coverage("A", "rows") == pytest.approx(0.95, abs=0.005)
    assert coverage("I", "rows") < coverage("I", "impressions") == pytest.approx(0.95, abs=0.005)
    assert coverage("M", "impressions") < coverage("M", 10) < coverage("M", 60) < 0.96
    assert coverage("U", 180) < coverage("H", 180)
    assert coverage("D", 60, "v_on") > coverage("D", "rows", "v_on") > 0.94


def test_settings_of_a_scenario(calibrated):
    logs, calibration = calibrated
    (q, groups, excess), _ = run.settings(logs, calibration, "A", "all")
    assert groups is None and excess == (0, 0, 0)
    assert q == pytest.approx(np.array(calibration["rate"])[logs[0].cell])
    (drifted, _, _), _ = run.settings(logs, calibration, "D", "all")
    assert not np.allclose(drifted, q)
    (_, groups, excess), _ = run.settings(logs, calibration, "I", "all")
    assert groups is None and excess == (calibration["e_impression"], 0, 0)
    (_, groups, excess), (_, _, bts_excess) = run.settings(logs, calibration, "M", "all")
    assert groups.long is None and excess[2] == bts_excess[2] == 0
    assert excess[1] == calibration["session"]["random"]["e"]
    assert bts_excess[1] == calibration["session"]["bts"]["e"]
    (_, groups, excess), (_, _, bts_excess) = run.settings(logs, calibration, "U", "all")
    assert groups.long is not None
    assert excess[0] == bts_excess[0] == calibration["e_impression"]
    assert excess[2] == bts_excess[2] == calibration["long"]["1440"]["e"]
    (_, h_groups, _), _ = run.settings(logs, calibration, "H", "all")
    assert (h_groups.session == groups.session).all()


def test_a_simulation_is_reproducible_and_keeps_its_progress(calibrated, tmp_path):
    logs, calibration = calibrated
    paths = [tmp_path / name for name in ("first.npz", "second.npz")]
    for path in paths:
        run.simulate(logs, calibration, "all", "M", path, 3)
    first, second = (dict(np.load(path)) for path in paths)
    assert int(first["done"]) == 3
    assert first["low"].shape == (3, len(UNITS), len(QUANTITIES))
    for name in ("estimate", "low", "high", "sd", "variance_ratio"):
        assert (first[name][:3] == second[name][:3]).all()
    assert (first["low"] < first["estimate"][:, None]).all()
    assert (first["estimate"][:, None] < first["high"]).all()
    assert (first["variance_ratio"][:3] > 0.3).all()
    stamp = paths[0].stat().st_mtime_ns
    run.simulate(logs, calibration, "all", "M", paths[0], 3)
    assert paths[0].stat().st_mtime_ns == stamp
    first["variance_ratio"][3:] = np.nan  # the rows of data sets that were not drawn
    summary = run.summarise(first, calibration, "M", TARGET)
    cell = summary["cells"]["ips_ratio"]["10"]
    assert summary["data_sets"] == 3 and 0 <= cell["coverage"] <= 1
    assert (
        cell["predicted_coverage"] == calibration["predicted"]["M"]["ips_ratio"]["coverage"]["10"]
    )
    assert summary["sd_of_ips_ratio"]["over_ten_minutes"]["180"]["published"] == 1.04
    ratio = summary["variance_ratio"]["bts"]["10"]
    assert ratio["published"] == 1.1
    assert ratio["mean"] == pytest.approx(first["variance_ratio"][:3, 1, 1].mean())


def test_data_sets_drawn_under_other_inputs_are_refused(calibrated, tmp_path):
    logs, calibration = calibrated
    path = tmp_path / "all_M.npz"
    run.simulate(logs, calibration, "all", "M", path, 1)
    other = json.loads(json.dumps(calibration)) | {"e_impression": 0.0}
    with pytest.raises(SystemExit, match="another calibration or scenario"):
        run.simulate(logs, other, "all", "M", path, 1)
    with pytest.raises(SystemExit, match="another calibration or scenario"):
        run.saved(path, run.inputs("all", "M", other))
    assert run.saved(path, run.inputs("all", "M", calibration))["done"] == 1


def results(label_of, widening, at_60=None):
    """Results in which the label of a primary cell is `label_of(scenario, unit)`."""
    cells = {
        s: {
            "cells": {"ips_ratio": {str(u): {"label": label_of(s, u)} for u in UNITS}},
            "sd_of_ips_ratio": {
                "over_ten_minutes": {
                    str(m): {"published": at_60 if at_60 and m == 60 else widening, "p97.5": 1.2}
                    for m in (60, 180)
                }
            },
        }
        for s in run.SCENARIOS
    }
    return dict.fromkeys(run.PRIMARY, cells)


def test_the_confirmatory_reading_when_nothing_counts_against_ten_minutes():
    reading = run.confirmatory(results(lambda s, u: "adequate", 1.1))
    assert reading["implementation_check_passed"]
    assert reading["against_ten_minute_intervals"] == {
        "ten_minutes_under_covers_in_M": [],
        "widening_above_M": [],
        "no_length_adequate_in_U": [],
    }
    assert reading["by_campaign"]["all"]["3_shortest_adequate_block"]["M"] == {
        "minutes": 5,
        "every_longer_adequate": True,
    }


def test_the_confirmatory_reading_when_everything_counts_against_ten_minutes():
    def label_of(scenario, unit):
        return "under-covers" if scenario in "MU" or unit == "rows" else "adequate"

    reading = run.confirmatory(results(label_of, 1.3))
    assert not reading["implementation_check_passed"]
    assert reading["against_ten_minute_intervals"] == {
        "ten_minutes_under_covers_in_M": ["all", "women"],
        "widening_above_M": ["all", "women"],
        "no_length_adequate_in_U": ["all", "women"],
    }
    assert reading["by_campaign"]["women"]["4_long"] == {
        "H": {"10": "adequate", "180": "adequate"},
        "U": {"10": "under-covers", "180": "under-covers"},
    }


def test_one_look_above_the_percentile_flags_a_campaign():
    reading = run.confirmatory(results(lambda s, u: "adequate", 1.3, at_60=1.1))
    assert reading["by_campaign"]["women"]["5_published_widening_above_M"] == {
        "60": False,
        "180": True,
    }
    assert reading["against_ten_minute_intervals"]["widening_above_M"] == ["all", "women"]
