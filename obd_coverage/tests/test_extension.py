import json

import numpy as np
import pytest

from obd.posthoc import blocks
from obd_coverage import direct, extension, model, run
from obd_coverage.intervals import QUANTITIES, UNITS
from obd_coverage.tests import small

TARGET = small.TARGET


def plain(x):
    return json.loads(json.dumps(x, default=lambda v: v.tolist() if hasattr(v, "tolist") else v))


@pytest.fixture(scope="module")
def calibrated():
    """Small logs whose clicks come in pairs within an impression, the registered calibration
    and that of the extension."""
    logs, _, _ = small.logs(0, n_random=30_000, n_bts=150_000)
    rng = np.random.default_rng(5)
    rows = [model.draw(rng, np.full(len(x.t), 0.08), x.impression, None, (3, 0, 0)) for x in logs]
    clicks = [np.bincount(r, minlength=len(x.t)) for r, x in zip(rows, logs, strict=True)]
    base = plain(run.calibrate(logs, clicks, TARGET, "all"))
    return logs, base, plain(extension.calibrate(logs, clicks, base, TARGET, "all"))


def test_a_registered_scenario_keeps_its_settings(calibrated):
    logs, base, _ = calibrated
    for scenario in ("M", "H"):
        mine = extension.settings(logs, base, extension.registered(base, scenario), "all")
        for (q, groups, excess), (q0, groups0, excess0) in zip(
            mine, run.settings(logs, base, scenario, "all"), strict=True
        ):
            assert (q == q0).all() and excess == pytest.approx(excess0)
            assert (groups.session == groups0.session).all()
            assert (groups.long is None) == (groups0.long is None)
            assert groups.long is None or (groups.long == groups0.long).all()


def test_the_fitted_scenario_takes_the_measured_excess_of_each_log(calibrated):
    logs, base, ext = calibrated
    for name in run.LOGS:
        measured = ext["direct"]["double_clicks"][name]
        assert measured["excess"] == pytest.approx(3, abs=0.5)
        assert measured["interval"][0] < measured["excess"] < measured["interval"][1]
        own = ext["scenarios"]["F"]["logs"][name]
        assert own["excess"][0] == measured["excess"]
        assert 0 <= own["excess"][1] <= own["excess"][0] and own["excess"][2] == 0
        assert own["size"] in extension.SIZES and own["minutes"] in model.SPANS
    groups = extension.settings(logs, base, ext["scenarios"]["F"], "all")[0][1]
    kinds = np.zeros((groups.session.max() + 1, logs[0].kind.max() + 1), bool)
    kinds[groups.session, logs[0].kind] = True
    assert (kinds.sum(axis=1) == 1).all()


def test_the_grid_of_sessions_holds_the_fitted_one_and_the_sessions_it_forms(calibrated):
    logs, base, calibration = calibrated
    grid = extension.session_grid(logs, base, calibration["direct"], TARGET, "all")
    for log, name in zip(logs, run.LOGS, strict=True):
        fitted = calibration["direct"]["double_clicks"][name]["sessions"]
        at = grid[name][f"{fitted['size']:g}"][str(fitted["minutes"])]
        assert {key: at[key] for key in ("e", "solved", "variance_ratio_at_1")} == {
            key: fitted[key] for key in ("e", "solved", "variance_ratio_at_1")
        }
        for by_span in grid[name].values():
            for cell in by_span.values():
                impressions = cell["sessions"] * cell["impressions_per_session"]
                assert impressions == pytest.approx(len(log.start))
                assert cell["seen_from_an_impression"] >= cell["impressions_per_session"]


def test_the_measured_variance_ratios_are_the_published_statistic(calibrated):
    _, _, ext = calibrated
    ratios = ext["direct"]["variance_ratio"]["bts"]
    assert list(ratios) == [str(m) for m in direct.RATIO_MINUTES]
    assert ratios["180"]["pairs_of_blocks"] == 28
    for x in ratios.values():
        assert x["interval"][0] < x["ratio"] < x["interval"][1]
    assert set(ext["direct"]["residuals"]) == {str(m) for m in blocks.MINUTES}


def test_dependence_and_drift_are_solved_to_the_same_published_widening(calibrated):
    logs, base, ext = calibrated
    for name in ("FH", "FS", "S"):
        scenario = ext["scenarios"][name]
        if not scenario["notes"]:
            setting = extension.settings(logs, base, scenario, "all")
            assert extension.widening(logs, setting) == pytest.approx(1.04, abs=1e-6)
    assert not ext["scenarios"]["FS"]["notes"] and not ext["scenarios"]["S"]["notes"]
    assert ext["scenarios"]["FS"]["logs"]["bts"]["drift"] > 0
    assert ext["scenarios"]["FS"]["logs"]["random"]["drift"] == 0
    assert ext["scenarios"]["S"]["logs"]["bts"]["excess"] == [0, 0, 0]
    assert ext["scenarios"]["FH"]["long_minutes"] == 60
    assert ext["scenarios"]["FU"]["long_minutes"] == 1440


def test_blocks_are_expected_to_over_cover_under_a_drift_the_logs_do_not_share(calibrated):
    _, _, ext = calibrated

    def expected(name, unit):
        return ext["scenarios"][name]["predicted"]["ips_ratio"]["coverage"][str(unit)]

    assert expected("S", 180) > expected("S", 10) > 0.95
    assert expected("FS", 180) > expected("F", 180)
    assert expected("FD", 180) == pytest.approx(expected("F", 180), abs=0.01)
    assert ext["scenarios"]["FD"]["truth"]["v_on"] != ext["scenarios"]["F"]["truth"]["v_on"]
    assert ext["scenarios"]["FS"]["truth"]["v_on"] == pytest.approx(
        ext["scenarios"]["F"]["truth"]["v_on"]
    )


def test_the_variants_change_one_choice_of_the_registered_scenarios(calibrated):
    _, base, ext = calibrated
    s = ext["scenarios"]
    assert s["M.half-sessions"]["logs"]["bts"]["size"] == model.SESSION_SIZE / 2
    assert s["M.double-sessions"]["logs"]["bts"]["size"] == model.SESSION_SIZE * 2
    assert s["H.half-long"]["per_long"] == 1.5 and s["H.double-long"]["per_long"] == 6
    assert s["H.half-long"]["logs"]["bts"]["size"] == model.SESSION_SIZE
    for registered in ("M", "H"):
        variant = s[f"{registered}.two-level"]
        assert variant["low"] == 0.5 and not variant["typed"]
        assert variant["predicted"] == base["predicted"][registered]
        assert variant["truth"] == base["truth"][registered]
        assert variant["largest_probability"] <= 1
    assert all(not s[name]["typed"] for name in extension.SCENARIOS[5:11])
    assert all(s[name]["typed"] for name in ("F", "FH", "FU", "FS", "FD"))


def test_a_simulation_is_reproducible_and_keeps_its_progress(calibrated, tmp_path):
    logs, base, ext = calibrated
    scenario = ext["scenarios"]["F"]

    def run_to(n, path):
        extension.simulate(logs, base, scenario, "all", "F", path, n, True)
        with np.load(path) as state:
            return {key: state[key].copy() for key in state}

    whole = run_to(4, tmp_path / "a.npz")
    assert whole["done"] == 4
    assert whole["low"].shape == (4, len(UNITS), len(QUANTITIES))
    assert whole["residuals"].shape == (4, len(blocks.MINUTES), len(direct.SUMS))
    assert (whole["low"] < whole["estimate"][:, None] + 1e-12).all()
    assert np.isfinite(whole["excess"][:4]).all() and (whole["variance_ratio"][:4] > 0).all()
    extension.simulate(logs, base, scenario, "all", "F", tmp_path / "b.npz", 2, True)
    (tmp_path / "b.npz").rename(tmp_path / "c.npz")
    again = run_to(4, tmp_path / "a.npz")
    assert all((whole[key] == again[key]).all() for key in ("estimate", "low", "residuals"))


def test_which_scenarios_are_simulated_where():
    assert extension.data_sets("men", "F") == (4000, True)
    assert extension.data_sets("men", "FH") is None
    assert extension.data_sets("all", "H.two-level") == (4000, True)
    assert extension.data_sets("women", "FU") == (1000, True)
    assert extension.data_sets("women", "FD") == (1000, False)
    assert extension.data_sets("men", "FD") is None


def results(g, labels):
    """Results with G(180) ranges by scenario and one label for every cell of a scenario."""
    by_scenario = {}
    for name in extension.SCENARIOS:
        low, high = g.get(name, (0, 0))
        by_scenario[name] = {
            "residuals": {"180": {"g": {"p2.5": low, "p97.5": high}}},
            "cells": {"ips_ratio": {str(u): {"label": labels(name, u)} for u in UNITS}},
        }
    return {campaign: by_scenario for campaign in run.PRIMARY}


def test_the_real_share_is_read_against_the_two_ranges():
    g = {"FH": (-0.3, 0.2), "FU": (-0.2, 0.3), "FD": (-0.25, 0.25), "FS": (0.1, 0.6)}
    measured = {"residuals": {"180": {"g": 0.45}}}
    out = extension.apart(results(g, lambda *_: "adequate"), measured, "women")
    assert out["within_types"] == [-0.3, 0.3] and out["drift"] == [0.1, 0.6]
    assert out["label"] == "more like a drift" and not out["separated"]
    measured["residuals"]["180"]["g"] = 0.2
    out = extension.apart(results(g, lambda *_: "adequate"), measured, "women")
    assert out["label"] == "not separated" and out["position"] == "inside both ranges"
    g["FS"] = (0.5, 0.9)
    measured["residuals"]["180"]["g"] = 0.4
    out = extension.apart(results(g, lambda *_: "adequate"), measured, "women")
    assert out["separated"] and out["position"] == "outside both ranges"
    measured["residuals"]["180"]["g"] = -0.4
    out = extension.apart(results(g, lambda *_: "adequate"), measured, "women")
    assert out["label"] == "more like dependence"


def test_the_residuals_are_summarised_for_the_ratio_and_within_each_log():
    long = blocks.MINUTES.index(180)
    sums = np.ones((3, *extension.RESIDUALS))  # [data set, length, sum]
    for key, values in (("v", [2, 4, 6]), ("v_random", [4, 4, 4]), ("w_bts", [1, 2, 3])):
        sums[:, long, direct.SUMS.index(key)] = values
    out = extension.over(sums)
    assert out["180"]["g"]["median"] == 0.75 and out["10"]["g"]["median"] == 0
    assert out["180"]["v_over_ten"]["median"] == 4 and out["180"]["w_over_ten"]["median"] == 1
    assert out["180"]["g_random"]["median"] == 0.75 and out["180"]["g_bts"]["median"] == -1
    assert out["180"]["v_random_over_ten"]["median"] == 4
    assert out["180"]["w_bts_over_ten"]["median"] == 2
    assert out["180"]["w_random_over_ten"]["median"] == out["180"]["v_bts_over_ten"]["median"] == 1


REGISTERED = json.loads((run.RESULTS / "coverage.json").read_text())["reading"]


def as_registered(name, unit):
    if name[0] == "M" or name == "F":
        return "under-covers" if unit in ("rows", "impressions") else "adequate"
    return "under-covers"


def test_results_with_the_registered_labels_are_robust():
    out = extension.confirmatory(results({}, as_registered), REGISTERED)
    assert out["robust"] == {"R1": True, "R2": True, "R3": True} and not out["changed"]
    assert out["same_labels_in_F"] == {"R1": True, "R2": True} and out["same_label_in_FH"]


def test_one_changed_label_makes_a_result_not_robust():
    def labels(name, unit):
        if (name, unit) == ("M.double-sessions", 180):
            return "unresolved"
        if (name, unit) == ("FH", 10):
            return "unresolved"
        return as_registered(name, unit)

    out = extension.confirmatory(results({}, labels), REGISTERED)
    assert out["robust"] == {"R1": True, "R2": False, "R3": True}
    assert {(c["result"], c["variant"], c["unit"], c["label"]) for c in out["changed"]} == {
        ("R2", "M.double-sessions", "180", "unresolved")
    }
    assert len(out["changed"]) == 2  # once per campaign
    assert not out["same_label_in_FH"]


def test_the_fit_says_which_statistics_the_fitted_scenario_reproduces():
    rng = np.random.default_rng(0)
    state = {
        "excess": rng.normal(3, 0.1, (400, 2)),
        "variance_ratio": rng.normal(1.5, 0.05, (400, 2, len(direct.RATIO_MINUTES))),
    }
    spread = {"p2.5": 0.9, "p97.5": 1.1}
    summary = {
        "sd_of_ips_ratio": {
            "impressions_over_rows": spread,
            "blocks_over_rows": spread,
            "over_ten_minutes": {str(m): spread | {"published": 1.0} for m in blocks.MINUTES},
        }
    }
    measured = {
        "double_clicks": {log: {"excess": 3.05} for log in run.LOGS},
        "variance_ratio": {
            log: {str(m): {"ratio": 1.5 if m < 60 else 2.5} for m in direct.RATIO_MINUTES}
            for log in run.LOGS
        },
    }
    out = extension.fit(state, summary, measured, TARGET)
    assert out["of"] == 2 + 2 * len(direct.RATIO_MINUTES) + 2 + 5
    missed = [r["statistic"] for r in out["statistics"] if not r["reproduced"]]
    assert missed == [
        "variance ratio at 60 minutes, random",
        "variance ratio at 180 minutes, random",
        "variance ratio at 60 minutes, bts",
        "variance ratio at 180 minutes, bts",
        "blocks over rows",
    ]
    assert sum(r["solved_from"] for r in out["statistics"]) == 6
    assert out["reproduced"] == out["of"] - 5
