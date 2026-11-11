import json

import pytest

from obd_coverage import extension_tables as tables
from obd_coverage import run
from obd_coverage.extension import RESULTS


def load(name):
    return json.loads((RESULTS / name).read_text())


def test_the_written_tables_are_those_of_the_result_files():
    results, calibration = load("coverage.json"), load("calibration.json")
    cells, _, _ = tables.cells_md(results)
    assert (RESULTS / "cells.md").read_text() == cells
    assert (RESULTS / "residuals.md").read_text() == tables.residuals_md(results, calibration)


def rows(text):
    """The rows of a table in Markdown, without its head."""
    return [line.strip("| ").split(" | ") for line in text.split("\n") if line[:2] == "| "][1:]


def test_every_cell_is_listed_once_and_the_missed_predictions_apart():
    cells, apart, n = tables.cells_md(load("coverage.json"))
    every, missed = map(rows, cells.split("## Cells whose prediction lies outside"))
    assert n == len(every) == len({tuple(r[:4]) for r in every}) == (10 * 2 + 1) * 4 * 8
    outside = [r for r in every if r[9] == "no"]  # the column "Prediction inside"
    assert apart == len(missed) and sorted(missed) == sorted(outside)
    gaps = [abs(float(r[4]) - float(r[8])) for r in missed]
    assert gaps[0] == max(gaps)


def test_the_real_residuals_are_set_over_those_at_ten_minutes():
    calibration = load("calibration.json")
    real = tables.real_shares(calibration, "women")
    raw = calibration["women"]["direct"]["residuals"]
    assert real["10"]["v_over_ten"] == real["10"]["w_bts_over_ten"] == 1
    assert real["180"]["v_over_ten"] == raw["180"]["v"] / raw["10"]["v"]
    assert real["180"]["g"] == raw["180"]["g"]


def test_a_registered_scenario_stands_beside_its_variants():
    published = json.loads((run.RESULTS / "coverage.json").read_text())
    lines = tables.coverage_table(load("coverage.json"), published, "men").split("\n")[2:]
    assert [line.split(" | ")[0] for line in lines] == [
        "| M (registered)",
        "| F",
        "| H (registered)",
    ]
    cell = published["men"]["M"]["cells"]["ips_ratio"]["rows"]
    assert f"{cell['coverage']:.3f} (-) / {cell['predicted_coverage']:.3f}" in lines[0]


def test_the_sessions_described_afterwards_are_those_of_the_calibration():
    calibration, described = load("calibration.json"), load("posthoc.json")
    for campaign in run.PRIMARY + ("men",):
        for log, measured in calibration[campaign]["direct"]["double_clicks"].items():
            fitted = measured["sessions"]
            at = described[campaign]["sessions"][log][f"{fitted['size']:g}"]
            assert at[str(fitted["minutes"])]["solved"] == pytest.approx(
                fitted["solved"], rel=1e-12
            )
            largest = described[campaign]["largest_impression"][log]
            assert largest["pairs"] / largest["share_of_pairs"] == pytest.approx(measured["pairs"])
    lines = rows(tables.session_table(described, calibration))
    assert [line[2] for line in lines] == ["44", "22", "44", "22", "44", "11"]  # nominal sizes
