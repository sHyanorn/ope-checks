"""The tables of the extension, from its two result files.

    python -m obd_coverage.extension_tables

prints the tables and writes `results/extension/cells.md` (one line per cell) and
`results/extension/residuals.md` (D3 by block length, real and simulated).
"""

import json

from obd.posthoc import blocks
from obd_coverage import run
from obd_coverage.direct import RATIO_MINUTES
from obd_coverage.extension import CONFIRMATORY, RESULTS, SCENARIOS, VARIANTS, registered
from obd_coverage.run import LOGS
from obd_coverage.tables import HEAD, MARK, NAMES, every_cell, prediction_table, table

FITTED = ("F", "FH", "FU", "FS", "S", "FD")
# D3: the key of a statistic in the results and its name in a table.
SHARES = {
    "g": "G",
    "v_over_ten": "V(L) / V(10)",
    "w_over_ten": "W(L) / W(10)",
    "between": "between the logs",
    "g_random": "G within the random log",
    "v_random_over_ten": "V(L) / V(10) within the random log",
    "w_random_over_ten": "W(L) / W(10) within the random log",
    "g_bts": "G within the BTS log",
    "v_bts_over_ten": "V(L) / V(10) within the BTS log",
    "w_bts_over_ten": "W(L) / W(10) within the BTS log",
}


def ranged(x, digits=2):
    """A value with its 2.5th to 97.5th percentile, or a median with them."""
    centre, low, high = x if isinstance(x, tuple) else (x["median"], x["p2.5"], x["p97.5"])
    return f"{centre:.{digits}f} ({low:.{digits}f} to {high:.{digits}f})"


def cut(solved, used):
    return f"{used:.1f}" if abs(solved - used) < 1e-9 else f"{used:.1f} (solved {solved:.1f})"


def double_click_table(calibration, base):
    lines = [
        [
            name,
            log,
            f"{d['pairs']:.0f}",
            f"{d['expected']:.1f}",
            ranged((d["excess"], *d["interval"]), 1),
            f"{base[campaign]['e_impression']:.1f}",
        ]
        for campaign, name in NAMES.items()
        for log, d in calibration[campaign]["direct"]["double_clicks"].items()
    ]
    head = ["Campaign", "Log", "`N2`", "`E0`", "`e_I^` (95% interval)", "registered `e_I`"]
    return table(head, lines)


def variance_ratio_table(calibration):
    lines = [
        [name, log, *(ranged((r["ratio"], *r["interval"])) for r in ratios.values())]
        for campaign, name in NAMES.items()
        for log, ratios in calibration[campaign]["direct"]["variance_ratio"].items()
    ]
    return table(["Campaign", "Log", *(f"{m} min" for m in RATIO_MINUTES)], lines)


def real_shares(calibration, campaign):
    """D3 on the real clicks, by block length, under the keys of the simulated summaries."""
    real = calibration[campaign]["direct"]["residuals"]
    out = {}
    for minutes, r in real.items():
        out[minutes] = {key: r[key] for key in ("g", "g_random", "g_bts", "between")}
        for s in ("", "_random", "_bts"):
            for key in "vw":
                out[minutes][f"{key}{s}_over_ten"] = r[key + s] / real["10"][key + s]
    return out


def real_share_table(calibration):
    keys = ("v_over_ten", "w_over_ten", "g", "g_random", "g_bts", "between")
    lines = [
        [name, minutes, *(f"{r[key]:.3f}" for key in keys)]
        for campaign, name in NAMES.items()
        for minutes, r in real_shares(calibration, campaign).items()
    ]
    return table(["Campaign", "Block, minutes", *(SHARES[key] for key in keys)], lines)


def fitted_table(calibration):
    """The scenarios built on the direct measurements: sessions by log, long groups, drift."""
    lines = []
    for campaign, name in NAMES.items():
        c = calibration[campaign]
        sessions = c["direct"]["double_clicks"]
        for scenario in FITTED:
            s = c["scenarios"][scenario]
            line = [name, scenario]
            for log in LOGS:
                own = s["logs"][log]
                if own["minutes"] is None:
                    line += ["", "", "", ""]
                    continue
                fit = sessions[log]["sessions"]
                e_i, e_s = own["excess"][:2]
                line += [f"{own['size']:g}", str(own["minutes"]), f"{e_i:.1f}"]
                line += [cut(fit["solved"], e_s)]
            long, drift = s.get("long"), s.get("drift")
            line += [f"{long['per_long']:g}", cut(long["solved"], long["e"])] if long else ["", ""]
            if drift:
                line += [f"{drift['k']:.2f} of {drift['k_max']:.2f}"]
            else:
                line += ["as D" if s["logs"]["bts"]["drift"] else ""]
            line += [f"{s['truth']['ips_ratio']:.4f}", f"{s['largest_probability']:.3f}"]
            lines.append(line)
    head = ["Campaign", "Scenario"]
    for log in LOGS:
        head += [f"{log}: nominal size", "`T`", "`e_I`", "`e_S`"]
    head += ["sessions per long group", "`e_L`", "`k` of `k_max`", "true IPS ratio"]
    return table([*head, "largest probability"], lines)


def session_table(grid, calibration):
    """The sessions of F by log: the nominal size and span that were fitted, the sessions that
    the grouping forms, and the smallest `e_S` that any size and span of the grid solves to."""
    lines = []
    for campaign, name in NAMES.items():
        measured = calibration[campaign]["direct"]
        for log in LOGS:
            fitted = measured["double_clicks"][log]["sessions"]
            cells = {
                (size, minutes): cell
                for size, by_span in grid[campaign]["sessions"][log].items()
                for minutes, cell in by_span.items()
            }
            at = cells[f"{fitted['size']:g}", str(fitted["minutes"])]
            (size, minutes), least = min(cells.items(), key=lambda x: x[1]["solved"])
            lines.append(
                [
                    name,
                    log,
                    f"{fitted['size']:g}",
                    str(fitted["minutes"]),
                    f"{at['impressions_per_session']:.2f}",
                    f"{at['seen_from_an_impression']:.1f}",
                    f"{max(0.0, measured['double_clicks'][log]['excess']):.1f}",
                    f"{at['solved']:.1f}",
                    f"{at['variance_ratio_at_1']:.2f}",
                    f"{measured['variance_ratio'][log]['1']['ratio']:.2f}",
                    f"{least['solved']:.1f} (size {size}, {minutes} min, "
                    f"{least['variance_ratio_at_1']:.2f})",
                ]
            )
    head = ["Campaign", "Log", "nominal size", "`T`", "impressions per session"]
    head += ["as seen from an impression", "`e_I`", "solved `e_S`", "one-minute ratio: fitted"]
    return table([*head, "real", "smallest solved `e_S` (where, its one-minute ratio)"], lines)


def largest_impression_table(grid, calibration):
    """Per log, the impression with the most pairs of clicked rows, and D1 without it."""
    lines = [
        [
            name,
            log,
            str(found["rows"]),
            str(found["clicks"]),
            f"{found['pairs']:.0f}",
            f"{found['share_of_pairs']:.1%}",
            f"{calibration[campaign]['direct']['double_clicks'][log]['excess']:.1f}",
            f"{found['excess_without']:.1f}",
        ]
        for campaign, name in NAMES.items()
        for log, found in grid[campaign]["largest_impression"].items()
    ]
    head = ["Campaign", "Log", "rows", "clicks", "pairs", "share of `N2`", "`e_I^`", "without it"]
    return table(head, lines)


def variant_table(calibration, base):
    """The variants of Section 5 beside the registered M and H."""

    def solved(notes, start, used):
        found = (float(n.split("solved as ")[1].split(",")[0]) for n in notes if start in n)
        return cut(next(found, used), used)

    lines = []
    for campaign, name in NAMES.items():
        for scenario in ("M", *VARIANTS["M"], "H", *VARIANTS["H"]):
            if scenario in VARIANTS[scenario[0]]:
                s = calibration[campaign]["scenarios"][scenario]
            else:
                s = registered(base[campaign], scenario)
            # The two-level variants keep the strengths of the registration and its notes.
            as_registered = "." not in scenario or scenario.endswith("two-level")
            notes = base[campaign]["notes"] if as_registered else s["notes"]
            line = [name, scenario]
            for log in LOGS:
                own = s["logs"][log]
                start = f"e_S of the {log} log at {own['minutes']} minutes"
                line += [str(own["minutes"]), solved(notes, start, own["excess"][1])]
            if s["long_minutes"]:
                e_l = s["logs"]["random"]["excess"][2]
                line += [solved(notes, f"e_L at {s['long_minutes']} minutes", e_l)]
            else:
                line += [""]
            line += [f"{s['largest_probability']:.3f}" if "largest_probability" in s else ""]
            lines.append(line)
    head = ["Campaign", "Scenario", "`T` random", "`e_S` random", "`T` BTS", "`e_S` BTS", "`e_L`"]
    return table([*head, "largest probability"], lines)


def beside(results, published, scenarios, variants=()):
    """(name in a table, where its cells are) for a registered scenario, its variants and the
    scenarios of the extension that are read with it."""
    return [
        (f"{scenarios[0]} (registered)", published, scenarios[0]),
        *((name, results, name) for name in (*variants, *scenarios[1:])),
    ]


def coverage_table(results, published, campaign, quantity="ips_ratio"):
    """Simulated coverage, its label, and the predicted coverage; M and H as registered."""
    rows = beside(results, published, ("M", "F"), VARIANTS["M"])
    rows += beside(results, published, ("H", "FH", "FS", "S"), VARIANTS["H"])
    lines = [
        [name]
        + [
            f"{c['coverage']:.3f}{MARK[c['label']]} / {c['predicted_coverage']:.3f}"
            for c in source[campaign][scenario]["cells"][quantity].values()
        ]
        for name, source, scenario in rows
        if "cells" in source[campaign].get(scenario, {})
    ]
    return table(["Scenario", *HEAD], lines)


def fit_table(results):
    """Section 3: every statistic of the real logs beside its range over the data sets of F."""
    fits = [results[campaign]["F"]["fit"] for campaign in NAMES]
    lines = []
    for rows in zip(*(f["statistics"] for f in fits), strict=True):
        line = [rows[0]["statistic"], "yes" if rows[0]["solved_from"] else ""]
        for r in rows:
            mark = "" if r["reproduced"] else " **no**"
            line.append(f"{r['real']:.3f} ({r['p2.5']:.3f} to {r['p97.5']:.3f}){mark}")
        lines.append(line)
    lines.append(["reproduced", "", *(f"{f['reproduced']} of {f['of']}" for f in fits)])
    return table(["Statistic", "Solved from", *NAMES.values()], lines)


def explanation_table(reading):
    lines = [
        [
            NAMES[campaign],
            f"{e['g_180']:.3f}",
            "{:.3f} to {:.3f}".format(*e["within_types"]),
            "{:.3f} to {:.3f}".format(*e["drift"]),
            "yes" if e["separated"] else "no",
            e["label"] + (f", {e['position']}" if "position" in e else ""),
        ]
        for campaign, e in reading["explanation"].items()
    ]
    head = ["Campaign", "real `G(180)`", "within types", "drift", "ranges apart", "label"]
    return table(head, lines)


def share_table(results, calibration, key, campaigns=NAMES):
    """One statistic of D3 by block length: the real value, then its median and range over
    the data sets of every scenario."""
    lines = []
    for campaign in campaigns:
        real = real_shares(calibration, campaign)
        lines.append([NAMES[campaign], "real", *(f"{r[key]:.3f}" for r in real.values())])
        for scenario in SCENARIOS:
            if scenario in results[campaign]:
                by_length = results[campaign][scenario]["residuals"]
                lines.append(
                    [NAMES[campaign], scenario, *(ranged(r[key]) for r in by_length.values())]
                )
    return table(["Campaign", "", *(f"{m} min" for m in blocks.MINUTES)], lines)


def widening_table(results):
    """The standard deviation of the replicates of the IPS ratio over the one at ten minutes."""
    lengths = [str(m) for m in blocks.MINUTES if m > 10]
    lines = []
    for campaign, name in NAMES.items():
        for scenario in SCENARIOS:
            ratios = results[campaign].get(scenario, {}).get("sd_of_ips_ratio")
            if ratios:
                by_length = ratios["over_ten_minutes"]
                lines.append([name, scenario, *(ranged(by_length[m], 3) for m in lengths)])
        by_length = results[campaign]["F"]["sd_of_ips_ratio"]["over_ten_minutes"]
        lines.append([name, "published", *(f"{by_length[m]['published']:.3f}" for m in lengths)])
    return table(["Campaign", "", *(f"{m} min" for m in lengths)], lines)


def reading_table(results, published):
    """Cells of the confirmatory reading: coverage, Wilson interval and label."""

    def cell(c):
        return "{:.3f} ({:.3f} to {:.3f}){}".format(c["coverage"], *c["wilson"], MARK[c["label"]])

    lines = []
    for units, rows in (
        (("rows", "impressions", "10"), beside(results, published, ("M", "F"), VARIANTS["M"])),
        (("10",), beside(results, published, ("H", "FH"), VARIANTS["H"])),
    ):
        for name, source, scenario in rows:
            for campaign in run.PRIMARY:
                cells = source[campaign][scenario]["cells"]["ips_ratio"]
                found = [cell(cells[unit]) for unit in units]
                lines.append([name, NAMES[campaign], *[""] * (3 - len(found)), *found])
    return table(["Scenario", "Campaign", "rows", "impressions", "10 min"], lines)


def cells_md(results):
    """`cells.md`, and how many of its cells have a prediction outside the Wilson interval."""
    cells, outside, n = every_cell(results, CONFIRMATORY)
    apart = [line for _, line in sorted(outside, key=lambda x: -x[0])]
    head = cells.split("\n", 1)[0].strip("| ").split(" | ")
    text = (
        "# Every cell of the extension\n\nWritten by `python -m obd_coverage.extension_tables` "
        'from `coverage.json`. "Interval below" is the share of intervals that lie below the '
        f"true value.\n\n{cells}\n\n## Cells whose prediction lies outside the Wilson interval"
        f"\n\n{len(apart)} of {n} cells, the widest gap first.\n\n{table(head, apart)}\n"
    )
    return text, len(apart), n


def residuals_md(results, calibration):
    tables = (
        f"## {name}\n\n{share_table(results, calibration, key)}" for key, name in SHARES.items()
    )
    return (
        "# Block residuals by log and user type (D3)\n\nWritten by `python -m "
        "obd_coverage.extension_tables` from `calibration.json` (the real clicks) and "
        "`coverage.json` (median and 2.5th to 97.5th percentile over the first 1,000 data sets "
        "of a scenario).\n\n" + "\n\n".join(tables) + "\n"
    )


def main():
    base = json.loads((run.RESULTS / "calibration.json").read_text())
    published = json.loads((run.RESULTS / "coverage.json").read_text())
    calibration = json.loads((RESULTS / "calibration.json").read_text())
    results = json.loads((RESULTS / "coverage.json").read_text())
    cells, apart, n = cells_md(results)
    (RESULTS / "cells.md").write_text(cells)
    (RESULTS / "residuals.md").write_text(residuals_md(results, calibration))

    print("## D1\n\n" + double_click_table(calibration, base))
    print("\n## D2\n\n" + variance_ratio_table(calibration))
    print("\n## D3 on the real clicks\n\n" + real_share_table(calibration))
    print("\n## Fitted scenarios\n\n" + fitted_table(calibration))
    grid = json.loads((RESULTS / "posthoc.json").read_text())  # written after the reading
    print("\n## Sessions of F\n\n" + session_table(grid, calibration))
    print("\n## Largest impression\n\n" + largest_impression_table(grid, calibration))
    print("\n## Variants\n\n" + variant_table(calibration, base))
    for campaign, name in NAMES.items():
        print(
            f"\n## IPS ratio, {name}: simulated / predicted\n\n"
            + coverage_table(results, published, campaign)
        )
    print("\n## Cells of the confirmatory reading\n\n" + reading_table(results, published))
    print("\n## Fit of F\n\n" + fit_table(results))
    print("\n## Explanation\n\n" + explanation_table(results["reading"]))
    print(f"\n## G by block length\n\n{share_table(results, calibration, 'g', run.PRIMARY)}")
    print("\n## Widening\n\n" + widening_table(results))
    print("\n## Predictions\n\n" + prediction_table(results, CONFIRMATORY))
    print(f"\n{apart} of {n} cells have a prediction outside the Wilson interval.")
    print("\n## Reading\n\n" + json.dumps(results["reading"], indent=1))


if __name__ == "__main__":
    main()
