"""Calibration, simulation and reading of the coverage study.

python -m obd_coverage.run check       # the block code against the published intervals
python -m obd_coverage.run calibrate   # writes results/calibration.json; generates no click
python -m obd_coverage.run simulate all men women
python -m obd_coverage.run read        # writes results/coverage.json
"""

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

from obd import data
from obd import estimators as est
from obd.posthoc import blocks
from obd.posthoc.run import load
from obd.posthoc.units import variance_ratio
from obd_coverage import model, moments, reading
from obd_coverage.intervals import N_REPLICATES, QUANTITIES, UNITS, Resampler

HERE = Path(__file__).parent
RESULTS = HERE / "results"
POSTHOC = HERE.parent / "obd" / "posthoc" / "results"
WORK_DIR = Path.home() / ".cache" / "ope-checks" / "coverage"
SEED = 20261111
LOGS = ("random", "bts")
SCENARIOS = ("A", "I", "M", "D", "H", "U")  # the index is part of the random streams
LONG = {"H": 60, "U": 1440}  # minutes
N_DATA_SETS = 4000
N_DESCRIBED = 200  # data sets on which the variance ratios are computed
RATIO_MINUTES = (1, 10, 60)
PRIMARY = ("all", "women")


def published():
    """The published numbers that the calibration and the reading use, by campaign."""
    units, lengths = (json.loads((POSTHOC / f).read_text()) for f in ("units.json", "blocks.json"))
    out = {}
    for campaign in data.CAMPAIGNS:
        h3, dependence = units[campaign]["h3"], units[campaign]["dependence"]
        rows = h3["rows"]["ips"]["sd"]
        out[campaign] = {
            "impressions_over_rows": h3["impressions"]["ips"]["sd"] / rows,
            "blocks_over_rows": h3["blocks"]["ips"]["sd"] / rows,
            "variance_ratio": {
                log: {m: dependence[log]["variance_ratio"][str(m)]["clicks"] for m in RATIO_MINUTES}
                for log in LOGS
            },
            "sd_over_ten_minutes": {
                m: lengths[campaign][str(m)]["ips"]["sd_over_ten_minutes"] for m in blocks.MINUTES
            },
        }
    return out


def rows(data_dir, campaign):
    """The kept logs of a campaign (random, BTS) and their real clicks."""
    stream = data.CAMPAIGNS.index(campaign)
    pi0 = est.fixed_prior_target(*data.read_prior(data_dir, campaign), stream)
    logs, clicks = [], []
    for policy in LOGS:
        frame = load(data_dir, policy, campaign)
        logs.append(model.kept(frame, pi0 if policy == "random" else None))
        clicks.append(frame["click"].to_numpy())
    return logs, clicks


def grouping_rng(campaign, log):
    return np.random.default_rng([SEED, 0, data.CAMPAIGNS.index(campaign), log])


def settings(logs, calibration, scenario, campaign):
    """Per log: the marginal click probability of each row, the groupings, the excesses."""
    rate, e_i = np.array(calibration["rate"]), calibration["e_impression"]
    out = []
    for i, (log, name) in enumerate(zip(logs, LOGS, strict=True)):
        q, groups, session = rate[log.cell], None, calibration["session"][name]
        if scenario == "D":
            q = q * model.drift(log.t, calibration["drift_by_hour"])
        if scenario in ("M", "H", "U"):
            groups = model.groupings(
                log.start, session["minutes"], LONG.get(scenario), grouping_rng(campaign, i)
            )
        excess = {
            "A": (0, 0, 0),
            "D": (0, 0, 0),
            "I": (e_i, 0, 0),
            "M": (e_i, session["e"], 0),
            "H": (e_i, session["e"], calibration["long"]["60"]["e"]),
            "U": (e_i, session["e"], calibration["long"]["1440"]["e"]),
        }[scenario]
        out.append((q, groups, excess))
    return out


def scenario_parts(logs, calibration, scenario, campaign):
    setting = settings(logs, calibration, scenario, campaign)
    lays = [moments.layout(log, groups) for log, (_, groups, _) in zip(logs, setting, strict=True)]
    return moments.quantity_parts(
        *logs, setting[0][0], setting[1][0], *lays, setting[0][2], setting[1][2]
    )


def calibrate(logs, clicks, target, campaign):
    """The parameters of Section 5 for one campaign, and the coverage they predict."""
    rate = model.cell_rates(logs, clicks, int(max(log.cell.max() for log in logs)) + 1)
    by_hour = model.fitted_drift(logs, clicks, rate)
    q = [rate[log.cell] for log in logs]
    drifted = sum((x * model.drift(log.t, by_hour)).sum() for x, log in zip(q, logs, strict=True))
    out = {"rate": rate, "drift_by_hour": by_hour * sum(x.sum() for x in q) / drifted, "notes": []}

    def ips_ratio(excess, groups=(None, None)):
        lays = [moments.layout(log, g) for log, g in zip(logs, groups, strict=True)]
        return moments.quantity_parts(*logs, *q, *lays, *excess)[0]["ips_ratio"]

    def clipped(name, e, low, high):
        if not low <= e <= high:
            out["notes"].append(f"{name} solved as {e:.4g}, set to {min(max(e, low), high):.4g}")
        return min(max(e, low), high)

    none, one = ips_ratio([(0, 0, 0)] * 2), ips_ratio([(1, 0, 0)] * 2)
    by_rows = moments.bootstrap_variance(none, "rows")
    e_i = moments.solve(
        target["impressions_over_rows"] ** 2,
        [moments.bootstrap_variance(p, "impressions") for p in (none, one)],
        (by_rows, by_rows),
    )
    e_i = out["e_impression"] = clipped("e_I", e_i, 0, np.inf)

    out["session"] = {}
    for i, (log, name) in enumerate(zip(logs, LOGS, strict=True)):
        ratios, tried = target["variance_ratio"][name], {}
        for minutes in model.SPANS:
            session = model.groupings(log.start, minutes, None, grouping_rng(campaign, i)).session
            at_ten = moments.variance_ratio_moments(log, q[i], session, e_i, 10)
            e_s = clipped(
                f"e_S of the {name} log at {minutes} minutes",
                moments.solve(ratios[10], *at_ten),
                0,
                e_i,
            )
            (n0, n1), (d0, d1) = moments.variance_ratio_moments(log, q[i], session, e_i, 1)
            at_one = (n0 + e_s * (n1 - n0)) / (d0 + e_s * (d1 - d0))
            tried[minutes] = {"e": e_s, "variance_ratio_at_1": at_one}
        best = min(tried, key=lambda m: abs(tried[m]["variance_ratio_at_1"] - ratios[1]))
        out["session"][name] = {"minutes": best, "e": tried[best]["e"], "tried": tried}

    e_s = [out["session"][name]["e"] for name in LOGS]
    out["long"] = {}
    for span in LONG.values():
        groups = [
            model.groupings(
                log.start, out["session"][name]["minutes"], span, grouping_rng(campaign, i)
            )
            for i, (log, name) in enumerate(zip(logs, LOGS, strict=True))
        ]
        at = [ips_ratio([(e_i, e, e_l) for e in e_s], groups) for e_l in (0, 1)]
        e_l = moments.solve(
            target["sd_over_ten_minutes"][180] ** 2,
            [moments.bootstrap_variance(p, 180) for p in at],
            [moments.bootstrap_variance(p, 10) for p in at],
        )
        out["long"][str(span)] = {
            "e": clipped(f"e_L at {span} minutes", e_l, 0, min(e_s)),
            "solved": e_l,
        }

    if (1 + e_i) * rate.max() > 1:
        raise SystemExit(f"{campaign}: (1 + e_I) max q = {(1 + e_i) * rate.max():.3f} exceeds 1")
    out["truth"], out["predicted"] = {}, {}
    for scenario in SCENARIOS:
        parts, out["truth"][scenario] = scenario_parts(logs, out, scenario, campaign)
        out["predicted"][scenario] = {}
        for quantity in QUANTITIES:
            true = moments.true_variance(parts[quantity])
            expected = {unit: moments.bootstrap_variance(parts[quantity], unit) for unit in UNITS}
            out["predicted"][scenario][quantity] = {
                "true_variance": true,
                "bootstrap_variance": {str(unit): v for unit, v in expected.items()},
                "coverage": {str(unit): moments.coverage(v / true) for unit, v in expected.items()},
            }
    return out


def simulate(logs, calibration, campaign, scenario, path, n_data_sets):
    """Estimates, interval ends and standard deviations of replicates over the data sets.

    Progress is kept in `path`, so an interrupted run continues where it stopped.
    """
    c, x = data.CAMPAIGNS.index(campaign), SCENARIOS.index(scenario)
    shape = (n_data_sets, len(UNITS), len(QUANTITIES))
    state = {
        "done": np.array(0),
        "estimate": np.empty((n_data_sets, len(QUANTITIES))),
        "low": np.empty(shape),
        "high": np.empty(shape),
        "sd": np.empty(shape),
        "variance_ratio": np.empty((N_DESCRIBED, len(LOGS), len(RATIO_MINUTES))),
    }
    if path.exists():
        with np.load(path) as saved:
            if saved["low"].shape == shape:
                state = {name: saved[name].copy() for name in state}
    setting = settings(logs, calibration, scenario, campaign)
    resampler = Resampler(*logs, np.random.default_rng([SEED, 3, c]))
    for s in range(int(state["done"]), n_data_sets):
        rng = np.random.default_rng([SEED, 1, c, x, s])
        clicked = [
            model.draw(rng, q, log.impression, groups, excess)
            for log, (q, groups, excess) in zip(logs, setting, strict=True)
        ]
        estimate, replicates = resampler.replicates(
            *clicked, np.random.default_rng([SEED, 2, c, x, s])
        )
        state["estimate"][s] = estimate
        state["low"][s], state["high"][s] = np.percentile(replicates, [2.5, 97.5], axis=1)
        state["sd"][s] = replicates.std(axis=1, ddof=1)
        if s < N_DESCRIBED:
            for i, (log, rows_clicked) in enumerate(zip(logs, clicked, strict=True)):
                clicks = np.bincount(log.impression[rows_clicked], minlength=len(log.size))
                state["variance_ratio"][s, i] = [
                    variance_ratio(log.start, clicks, log.size, m) for m in RATIO_MINUTES
                ]
        if (s + 1) % 250 == 0 or s + 1 == n_data_sets:
            state["done"] = np.array(s + 1)
            np.savez(path.with_suffix(".tmp.npz"), **state)
            path.with_suffix(".tmp.npz").replace(path)
            print(f"{campaign} {scenario}: {s + 1} data sets", flush=True)


def summarise(state, calibration, scenario, target):
    """Section 8 for one scenario and campaign."""
    truth, predicted = calibration["truth"][scenario], calibration["predicted"][scenario]
    out = {"data_sets": int(state["done"]), "cells": {}}
    for j, quantity in enumerate(QUANTITIES):
        out["cells"][quantity] = {}
        for u, unit in enumerate(UNITS):
            cell = reading.cell(
                state["estimate"][:, j],
                state["low"][:, u, j],
                state["high"][:, u, j],
                state["sd"][:, u, j],
                truth[quantity],
            )
            cell["predicted_coverage"] = predicted[quantity]["coverage"][str(unit)]
            out["cells"][quantity][str(unit)] = cell
    sd = state["sd"][:, :, 0]
    ten, by_rows = sd[:, UNITS.index(10)], sd[:, UNITS.index("rows")]
    out["sd_of_ips_ratio"] = {
        "over_ten_minutes": {
            str(m): reading.spread(sd[:, UNITS.index(m)] / ten) | {"published": published_m}
            for m, published_m in target["sd_over_ten_minutes"].items()
        },
        "impressions_over_rows": reading.spread(sd[:, UNITS.index("impressions")] / by_rows)
        | {"published": target["impressions_over_rows"]},
        "blocks_over_rows": reading.spread(ten / by_rows)
        | {"published": target["blocks_over_rows"]},
    }
    out["variance_ratio"] = {
        log: {
            str(m): {
                "mean": float(state["variance_ratio"][:, i, k].mean()),
                "published": target["variance_ratio"][log][m],
            }
            for k, m in enumerate(RATIO_MINUTES)
        }
        for i, log in enumerate(LOGS)
    }
    return out


def confirmatory(results):
    """The readings of Section 9 on the primary cells."""

    def labels(campaign, scenario):
        cells = results[campaign][scenario]["cells"]["ips_ratio"]
        return {unit: cells[str(unit)]["label"] for unit in UNITS}

    out = {"by_campaign": {}}
    for campaign in PRIMARY:
        m = labels(campaign, "M")
        widening = results[campaign]["M"]["sd_of_ips_ratio"]["over_ten_minutes"]
        flagged = {
            str(k): widening[str(k)]["published"] > widening[str(k)]["p97.5"] for k in (60, 180)
        }
        shortest = {}
        for scenario in SCENARIOS:
            by_length = {k: v for k, v in labels(campaign, scenario).items() if k in blocks.MINUTES}
            minutes, longer_too = reading.shortest_adequate(by_length)
            shortest[scenario] = {"minutes": minutes, "every_longer_adequate": longer_too}
        out["by_campaign"][campaign] = {
            "1_rows_in_A": labels(campaign, "A")["rows"],
            "2_M": {str(unit): m[unit] for unit in ("rows", "impressions", 10)},
            "3_shortest_adequate_block": shortest,
            "4_long": {s: {str(k): labels(campaign, s)[k] for k in (10, 180)} for s in LONG},
            "5_published_widening_above_M": flagged,
        }
    by = out["by_campaign"]
    out["implementation_check_passed"] = all(by[c]["1_rows_in_A"] == "adequate" for c in PRIMARY)
    out["against_ten_minute_intervals"] = {
        "ten_minutes_under_covers_in_M": [
            c for c in PRIMARY if by[c]["2_M"]["10"] == "under-covers"
        ],
        "widening_above_M": [
            c for c in PRIMARY if any(by[c]["5_published_widening_above_M"].values())
        ],
        "no_length_adequate_in_U": [
            c for c in PRIMARY if by[c]["3_shortest_adequate_block"]["U"]["minutes"] is None
        ],
    }
    return out


def check(data_dir):
    """With the real clicks and all registered multiplicities, the block code must give the
    published intervals of the two ratios of H3 at every length."""
    stored = json.loads((POSTHOC / "blocks.json").read_text())
    for campaign in data.CAMPAIGNS:
        logs, clicks = rows(data_dir, campaign)
        resampler = Resampler(*logs, None, est.N_REPLICATES)
        sums = resampler.sums(*(np.flatnonzero(c) for c in clicks))
        for minutes in blocks.MINUTES:
            replicates = resampler.blocks(*sums, minutes)
            for j, name in enumerate(("ips", "snips")):
                interval = np.percentile(replicates[:, j], [2.5, 97.5])
                if not np.allclose(interval, stored[campaign][str(minutes)][name]["interval"]):
                    raise SystemExit(f"{campaign}, {minutes} minutes, {name}: {interval} differs")
        print(f"{campaign}: the published block intervals are reproduced", flush=True)


def _code_commit():
    """The commit of the code, marked if a Python file differs from it."""

    def git(*args):
        done = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, check=True)
        return done.stdout.strip()

    return git("rev-parse", "HEAD") + (
        "-dirty" if git("status", "--porcelain", "--", ":/*.py") else ""
    )


def _write(name, result):
    RESULTS.mkdir(exist_ok=True)

    def plain(x):
        return x.tolist() if isinstance(x, np.ndarray) else x.item()

    (RESULTS / name).write_text(json.dumps(result, indent=1, default=plain) + "\n")
    print(f"wrote {RESULTS / name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("step", choices=["check", "calibrate", "simulate", "read"])
    parser.add_argument("campaigns", nargs="*", choices=data.CAMPAIGNS)
    parser.add_argument("--data-dir", type=Path, default=data.DEFAULT_DIR)
    parser.add_argument("--work-dir", type=Path, default=WORK_DIR)
    parser.add_argument("--data-sets", type=int, default=N_DATA_SETS)
    parser.add_argument("--scenarios", nargs="+", choices=SCENARIOS, default=SCENARIOS)
    args = parser.parse_args()
    provenance = {
        "code_commit": _code_commit(),
        "numpy": np.__version__,
        "command": f"python -m obd_coverage.run {args.step}",
    }
    target = published()
    if args.step == "check":
        return check(args.data_dir)
    if args.step == "calibrate":
        result = provenance | {"reads_real_clicks": "cell rates and the drift of scenario D"}
        result |= {"published": target}
        for campaign in data.CAMPAIGNS:
            logs, clicks = rows(args.data_dir, campaign)
            result[campaign] = calibrate(logs, clicks, target[campaign], campaign)
            print(f"calibrated {campaign}", flush=True)
        return _write("calibration.json", result)
    calibration = json.loads((RESULTS / "calibration.json").read_text())
    args.work_dir.mkdir(parents=True, exist_ok=True)
    if args.step == "simulate":
        for campaign in args.campaigns or data.CAMPAIGNS:
            logs, _ = rows(args.data_dir, campaign)
            for scenario in args.scenarios:
                path = args.work_dir / f"{campaign}_{scenario}.npz"
                simulate(logs, calibration[campaign], campaign, scenario, path, args.data_sets)
        return None
    results = provenance | {
        "replicates": N_REPLICATES,
        "calibration_commit": calibration["code_commit"],
    }
    for campaign in data.CAMPAIGNS:
        results[campaign] = {}
        for scenario in SCENARIOS:
            with np.load(args.work_dir / f"{campaign}_{scenario}.npz") as state:
                if int(state["done"]) != args.data_sets:
                    raise SystemExit(f"{campaign} {scenario}: {int(state['done'])} data sets done")
                results[campaign][scenario] = summarise(
                    state, calibration[campaign], scenario, target[campaign]
                )
    results["reading"] = confirmatory(results)
    return _write("coverage.json", results)


if __name__ == "__main__":
    main()
