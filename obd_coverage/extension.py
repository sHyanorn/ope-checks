"""The extension of the coverage study (EXTENSION.md): calibration, simulation, reading.

python -m obd_coverage.extension check       # the registered parameters, with the extended code
python -m obd_coverage.extension calibrate   # results/extension/calibration.json; reads the clicks
python -m obd_coverage.extension simulate all women --scenarios F FH
python -m obd_coverage.extension read        # results/extension/coverage.json
python -m obd_coverage.extension posthoc     # results/extension/posthoc.json; not registered
"""

import argparse
import json
from pathlib import Path

import numpy as np

from obd import data
from obd.posthoc import blocks
from obd.posthoc.units import variance_ratio
from obd_coverage import direct, model, moments, reading, run
from obd_coverage.intervals import QUANTITIES, UNITS, Resampler
from obd_coverage.run import LOGS, SEED

RESULTS = run.RESULTS / "extension"
WORK_DIR = run.WORK_DIR / "extension"
# The index of a scenario is part of the random streams.
SCENARIOS = (
    "F",
    "FH",
    "FU",
    "FS",
    "S",
    "M.half-sessions",
    "M.double-sessions",
    "M.two-level",
    "H.half-long",
    "H.double-long",
    "H.two-level",
    "FD",
)
VARIANTS = {"M": SCENARIOS[5:8], "H": SCENARIOS[8:11]}
CONFIRMATORY = ("F", "FH", "FS", "S", *VARIANTS["M"], *VARIANTS["H"])  # 4,000 data sets
N_DESCRIBED = 1000  # data sets of FU and FD, and those with residuals in every scenario
N_MEASURED = 400  # data sets of F with D1 and D2
SIZES = (5.5, 11, 22, 44)  # impressions of a session
PER_LONG = (3, 6, 12, 24)  # sessions of a long group
LOW = 0.5
WIDENING = 180  # minutes: the block length whose published standard deviation is matched
RESIDUALS = (len(blocks.MINUTES), len(direct.SUMS))


def typed_rng(campaign, log):
    return np.random.default_rng([SEED, 10, data.CAMPAIGNS.index(campaign), log])


def drifted(q, t, by_hour, k, rescaled):
    """Click probabilities that follow the drift of scenario D with amplitude `k`."""
    moved = q * (1 + k * (model.drift(t, by_hour) - 1))
    return moved * q.sum() / moved.sum() if rescaled else moved


def spec(logs, long_minutes=None, per_long=PER_LONG[0], typed=True, low=0.0, rescaled=True):
    """A scenario: per log the excesses (e_I, e_S, e_L), the span and size of a session and
    the amplitude of the drift; for both logs the long groups, the factor and the grouping."""
    return {
        "typed": typed,
        "long_minutes": long_minutes,
        "per_long": per_long,
        "low": low,
        "rescaled": rescaled,
        "logs": dict(zip(LOGS, logs, strict=True)),
        "notes": [],
    }


def of_log(excess=(0, 0, 0), minutes=None, size=model.SESSION_SIZE, drift=0.0):
    return {"excess": list(excess), "minutes": minutes, "size": size, "drift": drift}


def registered(calibration, scenario, size=model.SESSION_SIZE, per_long=PER_LONG[0], low=0.0):
    """Scenario M or H of the registration from a calibration of `run.calibrate`."""
    long_minutes = run.LONG.get(scenario)
    e_l = calibration["long"][str(long_minutes)]["e"] if long_minutes else 0
    own = [
        of_log(
            (calibration["e_impression"], calibration["session"][name]["e"], e_l),
            calibration["session"][name]["minutes"],
            size,
        )
        for name in LOGS
    ]
    return spec(own, long_minutes, per_long, typed=False, low=low)


def settings(logs, base, scenario, campaign):
    """Per log: the click probability of each row, the groupings, the excesses."""
    rate, out = np.array(base["rate"]), []
    for i, (log, name) in enumerate(zip(logs, LOGS, strict=True)):
        own, q, groups = scenario["logs"][name], rate[log.cell], None
        if own["drift"]:
            q = drifted(q, log.t, base["drift_by_hour"], own["drift"], scenario["rescaled"])
        if own["minutes"]:
            typed = scenario["typed"]
            groups = model.groupings(
                log.start,
                own["minutes"],
                scenario["long_minutes"],
                typed_rng(campaign, i) if typed else run.grouping_rng(campaign, i),
                own["size"],
                scenario["per_long"],
                log.kind if typed else None,
            )
        out.append((q, groups, tuple(own["excess"])))
    return out


def layouts(logs, setting):
    return [moments.layout(log, groups) for log, (_, groups, _) in zip(logs, setting, strict=True)]


def parts(logs, setting, lays=None):
    """The parts of each quantity and their true values; `lays` if already at hand."""
    lays = lays or layouts(logs, setting)
    return moments.quantity_parts(
        *logs, setting[0][0], setting[1][0], *lays, setting[0][2], setting[1][2]
    )


def widening(logs, setting, lays=None):
    """The expected standard deviation of the replicates of the IPS ratio at 180 minutes over
    the one at ten."""
    ratio = parts(logs, setting, lays)[0]["ips_ratio"]
    return (
        moments.bootstrap_variance(ratio, WIDENING) / moments.bootstrap_variance(ratio, 10)
    ) ** 0.5


def measure(logs, clicked, q, campaign):
    """D1 to D3 on the clicks of a campaign, with the intervals of D1 and D2."""
    c = data.CAMPAIGNS.index(campaign)
    out = {"double_clicks": {}, "variance_ratio": {}}
    for i, (log, rows, name) in enumerate(zip(logs, clicked, LOGS, strict=True)):
        ten = log.start // data.BLOCK_US
        pairs, expected = (
            np.bincount(ten, x, data.N_BLOCKS)
            for x in (direct.double_clicks(log, rows), direct.expected_pairs(log, q[i]))
        )
        rng = np.random.default_rng([SEED, 13, c, i, 1])
        out["double_clicks"][name] = {
            "pairs": float(pairs.sum()),
            "expected": float(expected.sum()),
            "excess": float(pairs.sum() / expected.sum() - 1),
            "interval": (direct.resampled_ratio(pairs, expected, rng) - 1).tolist(),
        }
        rng = np.random.default_rng([SEED, 13, c, i, 2])
        clicks = direct.clicks_by_impression(log, rows)
        out["variance_ratio"][name] = {}
        for minutes in direct.RATIO_MINUTES:
            terms = direct.variance_ratio_terms(log.start, clicks, log.size, minutes)
            out["variance_ratio"][name][str(minutes)] = {
                "pairs_of_blocks": len(terms[0]),
                "ratio": float(terms[0].sum() / terms[1].sum()),
                "interval": direct.resampled_ratio(*terms, rng).tolist(),
            }
    of = [direct.typed(log, p) for log, p in zip(logs, q, strict=True)]
    out["residuals"] = residual_table(direct.all_block_sums(of, clicked))
    return out


def residual_table(sums):
    """D3 by block length from `direct.all_block_sums`, with G for the ratio and by log."""
    out = {}
    for row, minutes in zip(sums, blocks.MINUTES, strict=True):
        named = dict(zip(direct.SUMS, row.tolist(), strict=True))
        named |= {"g": 1 - named["w"] / named["v"]}
        named |= {f"g_{log}": 1 - named[f"w_{log}"] / named[f"v_{log}"] for log in LOGS}
        out[str(minutes)] = named
    return out


def solve_sessions(log, q, e_i, ratios, campaign, i, size, minutes):
    """`e_S` of one log at a session size and span within user types, and the sessions."""
    session = model.groupings(
        log.start, minutes, None, typed_rng(campaign, i), size, kind=log.kind
    ).session
    solved = moments.solve(ratios[10], *moments.variance_ratio_moments(log, q, session, e_i, 10))
    e_s = min(max(solved, 0), e_i)
    (n0, n1), (d0, d1) = moments.variance_ratio_moments(log, q, session, e_i, 1)
    at_one = (n0 + e_s * (n1 - n0)) / (d0 + e_s * (d1 - d0))
    return {"e": e_s, "solved": solved, "variance_ratio_at_1": at_one}, session


def fit_sessions(log, q, e_i, ratios, campaign, i):
    """Span, strength and size of the sessions of one log within user types (Section 3)."""
    for size in SIZES:
        tried = {
            minutes: solve_sessions(log, q, e_i, ratios, campaign, i, size, minutes)[0]
            for minutes in model.SPANS
        }
        best = min(tried, key=lambda m: abs(tried[m]["variance_ratio_at_1"] - ratios[1]))
        if tried[best]["solved"] <= e_i or size == SIZES[-1]:
            return {"minutes": best, "size": size} | tried[best]


def session_grid(logs, base, measured, target, campaign):
    """Every size and span that `fit_sessions` chooses among, per log, with the sessions that
    the grouping forms. Descriptive; no part of the registration."""
    rate, out = np.array(base["rate"]), {}
    for i, (log, name) in enumerate(zip(logs, LOGS, strict=True)):
        e_i = max(0.0, measured["double_clicks"][name]["excess"])
        out[name] = {}
        for size in SIZES:
            out[name][f"{size:g}"] = {}
            for minutes in model.SPANS:
                tried, session = solve_sessions(
                    log,
                    rate[log.cell],
                    e_i,
                    target["variance_ratio"][name],
                    campaign,
                    i,
                    size,
                    minutes,
                )
                held = np.bincount(session)
                held = held[held > 0]  # impressions of each session
                out[name][f"{size:g}"][str(minutes)] = tried | {
                    "sessions": len(held),
                    "impressions_per_session": float(held.mean()),
                    "seen_from_an_impression": float((held**2).sum() / held.sum()),
                }
    return out


def fit_long(logs, base, scenario, campaign, target, long_minutes):
    """`scenario` with long groups whose strength matches the published widening."""

    def at(e_l, per_long):
        own = [x | {"excess": [*x["excess"][:2], e_l]} for x in scenario["logs"].values()]
        return spec(own, long_minutes, per_long)

    def ratio(e_l, per_long):
        setting = settings(logs, base, at(e_l, per_long), campaign)
        return parts(logs, setting)[0]["ips_ratio"]

    cap = min(x["excess"][1] for x in scenario["logs"].values())
    for per_long in PER_LONG:
        ends = [ratio(e_l, per_long) for e_l in (0, 1)]
        solved = moments.solve(
            target**2,
            [moments.bootstrap_variance(p, WIDENING) for p in ends],
            [moments.bootstrap_variance(p, 10) for p in ends],
        )
        if solved <= cap or per_long == PER_LONG[-1]:
            e_l = min(max(solved, 0), cap)
            out = at(e_l, per_long)
            out["long"] = {"e": e_l, "solved": solved, "per_long": per_long}
            if e_l != solved:
                out["notes"].append(f"e_L solved as {solved:.4g}, set to {e_l:.4g}")
            return out


def fit_drift(logs, base, scenario, campaign, target):
    """`scenario` with a drift in the BTS log whose amplitude matches the published widening."""

    def at(k):
        own = [scenario["logs"]["random"], scenario["logs"]["bts"] | {"drift": k}]
        return spec(own, scenario["long_minutes"], scenario["per_long"], scenario["typed"])

    still = settings(logs, base, scenario, campaign)
    lays = layouts(logs, still)  # the groupings do not move with the drift

    def widened(k):
        q = drifted(still[1][0], logs[1].t, base["drift_by_hour"], k, rescaled=True)
        return widening(logs, [still[0], (q, *still[1][1:])], lays)

    low, k_max = 0.0, 1 / (1 - model.drift(logs[1].t, base["drift_by_hour"]).min())
    high = k_max
    reached = [widened(k) for k in (low, high)]
    out_of_reach = reached[0] >= target or reached[1] < target
    if out_of_reach:
        k = low if reached[0] >= target else high
    else:
        for _ in range(30):
            k = (low + high) / 2
            low, high = (k, high) if widened(k) < target else (low, k)
        k = (low + high) / 2
    out = at(k)
    out["drift"] = {"k": k, "k_max": k_max, "widening_without": reached[0]}
    if out_of_reach:
        out["notes"].append(
            f"the drift cannot match {target:.4g}: the widening is {reached[0]:.4g} without it "
            f"and {reached[1]:.4g} at k_max; k set to {k:.4g}"
        )
    return out


def calibrate(logs, clicks, base, target, campaign):
    """The direct measurements and every scenario of the extension for one campaign."""
    rate = np.array(base["rate"])
    q = [rate[log.cell] for log in logs]
    out = {"direct": measure(logs, [np.flatnonzero(c) for c in clicks], q, campaign)}

    sessions, notes = [], []
    for i, (log, name) in enumerate(zip(logs, LOGS, strict=True)):
        e_i = max(0.0, out["direct"]["double_clicks"][name]["excess"])
        session = fit_sessions(log, q[i], e_i, target["variance_ratio"][name], campaign, i)
        if session["e"] != session["solved"]:
            notes.append(
                f"e_S of the {name} log solved as {session['solved']:.4g}, "
                f"set to {session['e']:.4g}"
            )
        sessions.append(of_log((e_i, session["e"], 0), session["minutes"], session["size"]))
        out["direct"]["double_clicks"][name]["sessions"] = session
    f = spec(sessions)
    f["notes"] = notes
    widened = target["sd_over_ten_minutes"][WIDENING]
    scenarios = {
        "F": f,
        "FH": fit_long(logs, base, f, campaign, widened, 60),
        "FU": fit_long(logs, base, f, campaign, widened, 1440),
        "FS": fit_drift(logs, base, f, campaign, widened),
        "S": fit_drift(logs, base, spec([of_log(), of_log()]), campaign, widened),
        "FD": spec([x | {"drift": 1.0} for x in sessions], rescaled=False),
        "M.two-level": registered(base, "M", low=LOW),
        "H.two-level": registered(base, "H", low=LOW),
    }
    for name, size, per_long in (
        ("M.half-sessions", model.SESSION_SIZE / 2, PER_LONG[0]),
        ("M.double-sessions", model.SESSION_SIZE * 2, PER_LONG[0]),
        ("H.half-long", model.SESSION_SIZE, PER_LONG[0] / 2),
        ("H.double-long", model.SESSION_SIZE, PER_LONG[0] * 2),
    ):
        solved = run.calibrate(logs, clicks, target, campaign, size, per_long, scenarios=())
        scenarios[name] = registered(solved, name[0], size, per_long)
        scenarios[name]["notes"] = solved["notes"]
    out["scenarios"] = {}
    for name in SCENARIOS:
        scenario = scenarios[name]
        setting = settings(logs, base, scenario, campaign)
        scenario["largest_probability"] = max(
            p.max() * model.largest_factor(excess, scenario["low"]) for p, _, excess in setting
        )
        if scenario["largest_probability"] > 1:
            raise SystemExit(f"{campaign} {name}: a click probability exceeds 1")
        scenario_parts, scenario["truth"] = parts(logs, setting)
        scenario["predicted"] = run.predicted(scenario_parts)
        out["scenarios"][name] = scenario
        print(f"calibrated {campaign} {name}", flush=True)
    return out


def simulate(logs, base, scenario, campaign, name, path, n_data_sets, intervals):
    """Data sets of a scenario: with `intervals`, estimates and interval ends as in
    `run.simulate`; the sums of D3 on the first data sets; in F also D1 and D2."""
    c, x = data.CAMPAIGNS.index(campaign), SCENARIOS.index(name)
    shape = (n_data_sets, len(UNITS), len(QUANTITIES))
    state = {
        "done": np.array(0),
        "estimate": np.empty((n_data_sets, len(QUANTITIES))),
        "low": np.empty(shape),
        "high": np.empty(shape),
        "sd": np.empty(shape),
        "residuals": np.empty((min(n_data_sets, N_DESCRIBED), *RESIDUALS)),
        "excess": np.empty((N_MEASURED, len(LOGS))),
        "variance_ratio": np.empty((N_MEASURED, len(LOGS), len(direct.RATIO_MINUTES))),
    }
    if path.exists():
        with np.load(path) as saved:
            if saved["low"].shape == shape:
                state = {key: saved[key].copy() for key in state}
    setting = settings(logs, base, scenario, campaign)
    rate = np.array(base["rate"])
    q = [rate[log.cell] for log in logs]
    of = [direct.typed(log, p) for log, p in zip(logs, q, strict=True)]
    expected = [direct.expected_pairs(log, p).sum() for log, p in zip(logs, q, strict=True)]
    resampler = Resampler(*logs, np.random.default_rng([SEED, 3, c])) if intervals else None
    for s in range(int(state["done"]), n_data_sets):
        rng = np.random.default_rng([SEED, 11, c, x, s])
        clicked = [
            model.draw(rng, p, log.impression, groups, excess, scenario["low"])
            for log, (p, groups, excess) in zip(logs, setting, strict=True)
        ]
        if intervals:
            estimate, replicates = resampler.replicates(
                *clicked, np.random.default_rng([SEED, 12, c, x, s])
            )
            state["estimate"][s] = estimate
            state["low"][s], state["high"][s] = np.percentile(replicates, [2.5, 97.5], axis=1)
            state["sd"][s] = replicates.std(axis=1, ddof=1)
        if s < len(state["residuals"]):
            state["residuals"][s] = direct.all_block_sums(of, clicked)
        if name == "F" and s < N_MEASURED:
            for i, (log, rows) in enumerate(zip(logs, clicked, strict=True)):
                state["excess"][s, i] = direct.double_clicks(log, rows).sum() / expected[i] - 1
                clicks = direct.clicks_by_impression(log, rows)
                state["variance_ratio"][s, i] = [
                    variance_ratio(log.start, clicks, log.size, m) for m in direct.RATIO_MINUTES
                ]
        if (s + 1) % 250 == 0 or s + 1 == n_data_sets:
            state["done"] = np.array(s + 1)
            np.savez(path.with_suffix(".tmp.npz"), **state)
            path.with_suffix(".tmp.npz").replace(path)
            print(f"{campaign} {name}: {s + 1} data sets", flush=True)


def data_sets(campaign, name):
    """How many data sets a scenario gets on a campaign and whether they get intervals;
    `None` where it is not simulated."""
    if name in CONFIRMATORY and (campaign in run.PRIMARY or name == "F"):
        return run.N_DATA_SETS, True
    if name in ("FU", "FD") and campaign in run.PRIMARY:
        return N_DESCRIBED, name == "FU"  # FU gets replicates for their standard deviations
    return None


def over(sums):
    """D3 over the data sets, by block length, for the ratio and within each log: G, and V and
    W over those at ten minutes."""
    ten = blocks.MINUTES.index(10)
    x = {key: sums[..., i] for i, key in enumerate(direct.SUMS)}  # [data set, length]
    of = ("", *(f"_{log}" for log in LOGS))
    out = {}
    for j, minutes in enumerate(blocks.MINUTES):
        out[str(minutes)] = (
            {"between": reading.spread(x["between"][:, j])}
            | {f"g{s}": reading.spread(1 - x[f"w{s}"][:, j] / x[f"v{s}"][:, j]) for s in of}
            | {
                f"{key}{s}_over_ten": reading.spread(x[key + s][:, j] / x[key + s][:, ten])
                for s in of
                for key in "vw"
            }
        )
    return out


def fit(state, summary, measured, target):
    """Section 3: the statistics of the real logs beside those of the data sets of F."""

    def row(name, real, low, high, solved_from=False):
        return {
            "statistic": name,
            "real": real,
            "p2.5": float(low),
            "p97.5": float(high),
            "reproduced": bool(low <= real <= high),
            "solved_from": solved_from,
        }

    rows, drawn = [], int(state["done"])
    for i, log in enumerate(LOGS):
        low, high = np.percentile(state["excess"][:drawn, i], [2.5, 97.5])
        real = measured["double_clicks"][log]["excess"]
        rows.append(row(f"excess within an impression, {log}", real, low, high, True))
        for k, minutes in enumerate(direct.RATIO_MINUTES):
            low, high = np.percentile(state["variance_ratio"][:drawn, i, k], [2.5, 97.5])
            real = measured["variance_ratio"][log][str(minutes)]["ratio"]
            name = f"variance ratio at {minutes} minutes, {log}"
            rows.append(row(name, real, low, high, minutes in (1, 10)))
    widths = summary["sd_of_ips_ratio"]
    for key in ("impressions_over_rows", "blocks_over_rows"):
        x = widths[key]
        rows.append(row(key.replace("_", " "), target[key], x["p2.5"], x["p97.5"]))
    for minutes in blocks.MINUTES:
        if minutes != 10:
            x = widths["over_ten_minutes"][str(minutes)]
            name = f"{minutes} minutes over ten"
            rows.append(row(name, x["published"], x["p2.5"], x["p97.5"]))
    return {"statistics": rows, "reproduced": sum(r["reproduced"] for r in rows), "of": len(rows)}


def apart(results, measured, campaign):
    """Section 4: the real G(180) against its ranges within types and under a drift."""

    def g(name):
        return results[campaign][name]["residuals"][str(WIDENING)]["g"]

    within = (
        min(g(n)["p2.5"] for n in ("FH", "FU", "FD")),
        max(g(n)["p97.5"] for n in ("FH", "FU", "FD")),
    )
    drift = (g("FS")["p2.5"], g("FS")["p97.5"])
    real = measured["residuals"][str(WIDENING)]["g"]
    label = direct.explanation(real, within, drift)
    out = {
        "g_180": real,
        "within_types": list(within),
        "drift": list(drift),
        "separated": bool(within[1] < drift[0] or drift[1] < within[0]),
        "label": label,
    }
    if label == "not separated":
        inside = within[0] <= real <= within[1] and drift[0] <= real <= drift[1]
        out["position"] = "inside both ranges" if inside else "outside both ranges"
    return out


def confirmatory(results, registered_reading):
    """The readings of Section 6 from the cells of the extension and the registered labels."""

    def labels(campaign, name, units):
        cells = results[campaign][name]["cells"]["ips_ratio"]
        return {str(unit): cells[str(unit)]["label"] for unit in units}

    narrow, lengths = ("rows", "impressions"), blocks.MINUTES
    expected = {
        "R1": dict.fromkeys(map(str, narrow), "under-covers"),
        "R2": dict.fromkeys(map(str, lengths), "adequate"),
        "R3": {"10": "under-covers"},
    }
    units = {"R1": narrow, "R2": lengths, "R3": (10,)}
    for campaign in run.PRIMARY:  # the three results are the registered labels
        by = registered_reading["by_campaign"][campaign]
        assert all(by["2_M"][u] == "under-covers" for u in narrow)
        assert by["3_shortest_adequate_block"]["M"] == {"minutes": 5, "every_longer_adequate": True}
        assert by["4_long"]["H"]["10"] == "under-covers"
    out = {"robust": {}, "changed": [], "F": {}, "FH": {}}
    for result, scenario in (("R1", "M"), ("R2", "M"), ("R3", "H")):
        changed = [
            {
                "result": result,
                "campaign": campaign,
                "variant": variant,
                "unit": unit,
                "label": label,
            }
            for variant in VARIANTS[scenario]
            for campaign in run.PRIMARY
            for unit, label in labels(campaign, variant, units[result]).items()
            if label != expected[result][unit]
        ]
        out["robust"][result] = not changed
        out["changed"] += changed
    for campaign in run.PRIMARY:
        out["F"][campaign] = labels(campaign, "F", (*narrow, *lengths))
        out["FH"][campaign] = labels(campaign, "FH", (10,))
    out["same_labels_in_F"] = {
        result: all(
            out["F"][campaign][unit] == label
            for campaign in run.PRIMARY
            for unit, label in expected[result].items()
        )
        for result in ("R1", "R2")
    }
    out["same_label_in_FH"] = all(
        out["FH"][campaign]["10"] == "under-covers" for campaign in run.PRIMARY
    )
    return out


def check(data_dir, baseline, campaigns):
    """With the registered choices the extended code must give the registered parameters and,
    given `baseline` (data sets of A and M on Women's from the code of the coverage study),
    the same estimates and interval ends."""
    stored = json.loads((run.RESULTS / "calibration.json").read_text())
    target = run.published()
    for campaign in campaigns:
        logs, clicks = run.rows(data_dir, campaign)
        again = run.calibrate(logs, clicks, target[campaign], campaign, scenarios=())
        same = np.isclose(again["e_impression"], stored[campaign]["e_impression"], rtol=1e-12)
        for name in LOGS:
            for key in ("minutes", "e"):
                same &= np.isclose(
                    again["session"][name][key], stored[campaign]["session"][name][key], rtol=1e-12
                )
        for span in run.LONG.values():
            same &= np.isclose(
                again["long"][str(span)]["e"], stored[campaign]["long"][str(span)]["e"], rtol=1e-12
            )
        if not same:
            raise SystemExit(f"{campaign}: the registered parameters are not reproduced")
        print(f"{campaign}: the registered parameters are reproduced", flush=True)
        if baseline and campaign == "women":
            for scenario in ("A", "M"):
                with np.load(baseline / f"women_{scenario}.npz") as before:
                    n = int(before["done"])
                    path = baseline / f"again_{scenario}.npz"
                    path.unlink(missing_ok=True)  # `simulate` would continue from it
                    run.simulate(logs, stored[campaign], campaign, scenario, path, n)
                    with np.load(path) as after:
                        apart = max(
                            np.abs(before[key] - after[key]).max()
                            for key in ("estimate", "low", "high")
                        )
                if apart > 1e-12:  # the last digits depend on the threads of the linear algebra
                    raise SystemExit(f"women {scenario}: the data sets differ by {apart:.3g}")
                print(f"women {scenario}: {n} data sets reproduced within {apart:.3g}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("step", choices=["check", "calibrate", "simulate", "read", "posthoc"])
    parser.add_argument("campaigns", nargs="*", choices=data.CAMPAIGNS)
    parser.add_argument("--data-dir", type=Path, default=data.DEFAULT_DIR)
    parser.add_argument("--work-dir", type=Path, default=WORK_DIR)
    parser.add_argument("--scenarios", nargs="+", choices=SCENARIOS, default=SCENARIOS)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    provenance = {
        "code_commit": run._code_commit(),
        "numpy": np.__version__,
        "command": f"python -m obd_coverage.extension {args.step}",
    }
    target = run.published()
    if args.step == "check":
        return check(args.data_dir, args.baseline, args.campaigns or data.CAMPAIGNS)
    base = json.loads((run.RESULTS / "calibration.json").read_text())
    if args.step == "calibrate":
        result = provenance | {
            "reads_real_clicks": "the direct measurements D1 to D3",
            "registered_calibration_commit": base["code_commit"],
        }
        for campaign in data.CAMPAIGNS:
            logs, clicks = run.rows(args.data_dir, campaign)
            result[campaign] = calibrate(logs, clicks, base[campaign], target[campaign], campaign)
        return run._write("extension/calibration.json", result)
    calibration = json.loads((RESULTS / "calibration.json").read_text())
    if args.step == "posthoc":
        result = provenance | {"calibration_commit": calibration["code_commit"]}
        for campaign in data.CAMPAIGNS:
            logs, clicks = run.rows(args.data_dir, campaign)
            rate, measured = np.array(base[campaign]["rate"]), calibration[campaign]["direct"]
            result[campaign] = {
                "sessions": session_grid(
                    logs, base[campaign], measured, target[campaign], campaign
                ),
                "largest_impression": {
                    name: direct.largest_impression(log, np.flatnonzero(c), rate[log.cell])
                    for log, c, name in zip(logs, clicks, LOGS, strict=True)
                },
            }
        return run._write("extension/posthoc.json", result)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    if args.step == "simulate":
        for campaign in args.campaigns or data.CAMPAIGNS:
            logs, _ = run.rows(args.data_dir, campaign)
            for name in args.scenarios:
                if planned := data_sets(campaign, name):
                    scenario = calibration[campaign]["scenarios"][name]
                    path = args.work_dir / f"{campaign}_{name}.npz"
                    simulate(logs, base[campaign], scenario, campaign, name, path, *planned)
        return None
    results = provenance | {"calibration_commit": calibration["code_commit"]}
    for campaign in data.CAMPAIGNS:
        results[campaign] = {}
        for name in SCENARIOS:
            if not (planned := data_sets(campaign, name)):
                continue
            scenario = calibration[campaign]["scenarios"][name]
            with np.load(args.work_dir / f"{campaign}_{name}.npz") as state:
                if int(state["done"]) != planned[0]:
                    raise SystemExit(f"{campaign} {name}: {int(state['done'])} data sets done")
                summary = {"data_sets": planned[0], "residuals": over(state["residuals"])}
                if name in CONFIRMATORY:
                    summary |= run.cells(state, scenario["truth"], scenario["predicted"])
                if planned[1]:
                    summary["sd_of_ips_ratio"] = run.widths(state, target[campaign])
                if name == "F":
                    measured = calibration[campaign]["direct"]
                    summary["fit"] = fit(state, summary, measured, target[campaign])
                results[campaign][name] = summary
    registered_reading = json.loads((run.RESULTS / "coverage.json").read_text())["reading"]
    results["reading"] = confirmatory(results, registered_reading) | {
        "explanation": {
            campaign: apart(results, calibration[campaign]["direct"], campaign)
            for campaign in run.PRIMARY
        }
    }
    return run._write("extension/coverage.json", results)


if __name__ == "__main__":
    main()
