"""The tables of the README and `results/cells.md`, from the two result files.

    python -m obd_coverage.tables

prints the tables and writes one line per cell to `results/cells.md`.
"""

import json

from obd.posthoc import blocks
from obd_coverage.intervals import QUANTITIES, UNITS
from obd_coverage.run import LOGS, LONG, RESULTS, SCENARIOS

NAMES = {"all": "All", "women": "Women's", "men": "Men's"}
MARK = {"adequate": "", "under-covers": " (-)", "over-covers": " (+)", "unresolved": " (?)"}
HEAD = ["rows", "impressions", *(f"{m} min" for m in blocks.MINUTES)]


def table(head, lines):
    rule = "|" + "---|" * len(head)
    return "\n".join(
        ["| " + " | ".join(head) + " |", rule, *("| " + " | ".join(x) + " |" for x in lines)]
    )


def calibration_table(calibration):
    def cut(solved, used):
        return f"{used:.1f}" if abs(solved - used) < 1e-9 else f"{used:.1f} (solved {solved:.1f})"

    lines = []
    for campaign, name in NAMES.items():
        c = calibration[campaign]
        sessions = []
        for log in LOGS:
            s = c["session"][log]
            solved = next(
                (
                    float(n.split("solved as ")[1].split(",")[0])
                    for n in c["notes"]
                    if n.startswith(f"e_S of the {log} log at {s['minutes']} minutes")
                ),
                s["e"],
            )
            sessions += [str(s["minutes"]), cut(solved, s["e"])]
        long = [
            cut(c["long"][str(span)]["solved"], c["long"][str(span)]["e"]) for span in LONG.values()
        ]
        truth = c["truth"]["A"]["ips_ratio"]
        lines.append([name, f"{c['e_impression']:.1f}", *sessions, *long, f"{truth:.4f}"])
    head = [
        "Campaign",
        "`e_I`",
        "`T` random",
        "`e_S` random",
        "`T` BTS",
        "`e_S` BTS",
        "`e_L` 60 min",
        "`e_L` 24 h",
        "true IPS ratio",
    ]
    return table(head, lines)


def coverage_table(results, campaign, quantity):
    lines = []
    for scenario in SCENARIOS:
        cells = results[campaign][scenario]["cells"][quantity]
        lines.append(
            [scenario]
            + [
                f"{cells[str(u)]['coverage']:.3f}{MARK[cells[str(u)]['label']]} / "
                f"{cells[str(u)]['predicted_coverage']:.3f}"
                for u in UNITS
            ]
        )
    return table(["Scenario", *HEAD], lines)


def widening_table(results):
    lines = []
    for campaign, name in NAMES.items():
        for scenario in ("M", "H", "U"):
            ratios = results[campaign][scenario]["sd_of_ips_ratio"]["over_ten_minutes"]
            at = [ratios[str(m)] for m in (60, 180)]
            cells = [f"{r['median']:.3f} ({r['p2.5']:.3f} to {r['p97.5']:.3f})" for r in at]
            published = [f"{ratios[str(m)]['published']:.3f}" for m in (60, 180)]
            lines.append([name, scenario, cells[0], published[0], cells[1], published[1]])
    head = [
        "Campaign",
        "Scenario",
        "60 min: simulated",
        "published",
        "180 min: simulated",
        "published",
    ]
    return table(head, lines)


def dependence_table(results):
    lines = []
    for campaign, name in NAMES.items():
        for scenario in ("A", "M", "H", "U"):
            r = results[campaign][scenario]
            sd = r["sd_of_ips_ratio"]
            row = [name, scenario]
            for log in LOGS:
                row += [f"{r['variance_ratio'][log][m]['mean']:.2f}" for m in ("1", "10", "60")]
            row += [
                f"{sd['impressions_over_rows']['mean']:.3f}",
                f"{sd['blocks_over_rows']['mean']:.2f}",
            ]
            lines.append(row)
        p = results[campaign]["A"]
        row = [name, "published"]
        for log in LOGS:
            row += [f"{p['variance_ratio'][log][m]['published']:.2f}" for m in ("1", "10", "60")]
        sd = p["sd_of_ips_ratio"]
        row += [
            f"{sd['impressions_over_rows']['published']:.3f}",
            f"{sd['blocks_over_rows']['published']:.2f}",
        ]
        lines.append(row)
    head = [
        "Campaign",
        "",
        "random 1",
        "10",
        "60",
        "BTS 1",
        "10",
        "60",
        "impressions / rows",
        "blocks / rows",
    ]
    return table(head, lines)


def every_cell(results):
    """One line per cell, and the cells whose prediction lies outside the Wilson interval."""
    lines, outside = [], []
    for campaign, name in NAMES.items():
        for scenario in SCENARIOS:
            for quantity in QUANTITIES:
                for unit, head in zip(UNITS, HEAD, strict=True):
                    c = results[campaign][scenario]["cells"][quantity][str(unit)]
                    inside = c["wilson"][0] <= c["predicted_coverage"] <= c["wilson"][1]
                    line = [
                        name,
                        scenario,
                        quantity,
                        head,
                        f"{c['coverage']:.3f}",
                        f"{c['wilson'][0]:.3f} to {c['wilson'][1]:.3f}",
                        c["label"],
                        "yes" if c["contains_nominal"] else "no",
                        f"{c['predicted_coverage']:.3f}",
                        "yes" if inside else "no",
                        f"{c['interval_below_truth']:.3f}",
                        f"{c['interval_above_truth']:.3f}",
                        f"{c['mean_width']:.3g}",
                        f"{c['median_width']:.3g}",
                        f"{c['sd_of_replicates_over_sd_of_estimate']:.3f}",
                        f"{c['coverage_of_mean_estimate']:.3f}",
                    ]
                    lines.append(line)
                    if not inside:
                        outside.append((abs(c["coverage"] - c["predicted_coverage"]), line))
    head = [
        "Campaign",
        "Scenario",
        "Quantity",
        "Unit",
        "Coverage",
        "Wilson 95%",
        "Label",
        "Interval contains 0.95",
        "Predicted",
        "Prediction inside",
        "Interval below",
        "Interval above",
        "Mean width",
        "Median width",
        "sd of replicates / sd of estimate",
        "Coverage of mean estimate",
    ]
    return table(head, lines), outside, len(lines)


def prediction_table(results):
    """Simulated minus predicted coverage, summarised by quantity over all other factors."""
    lines = []
    for quantity in (*QUANTITIES, None):
        gaps, outside = [], 0
        for campaign in NAMES:
            for scenario in SCENARIOS:
                for q in QUANTITIES if quantity is None else (quantity,):
                    for c in results[campaign][scenario]["cells"][q].values():
                        gaps.append(c["coverage"] - c["predicted_coverage"])
                        outside += not c["wilson"][0] <= c["predicted_coverage"] <= c["wilson"][1]
        lines.append(
            [
                quantity or "all",
                str(len(gaps)),
                str(outside),
                f"{sum(gaps) / len(gaps):+.3f}",
                f"{min(gaps):+.3f}",
                f"{max(gaps):+.3f}",
                str(sum(abs(g) > 0.01 for g in gaps)),
            ]
        )
    head = [
        "Quantity",
        "Cells",
        "Prediction outside the Wilson interval",
        "Mean of simulated minus predicted",
        "Smallest",
        "Largest",
        "Cells more than 0.01 apart",
    ]
    return table(head, lines)


def main():
    calibration = json.loads((RESULTS / "calibration.json").read_text())
    results = json.loads((RESULTS / "coverage.json").read_text())
    cells, outside, n = every_cell(results)
    (RESULTS / "cells.md").write_text(
        "# Every cell of the coverage study\n\nWritten by `python -m obd_coverage.tables` from "
        '`coverage.json`. "Interval below" is the share of intervals that lie below the true '
        "value.\n\n" + cells + "\n"
    )
    print("## Calibration\n\n" + calibration_table(calibration))
    for campaign, name in NAMES.items():
        print(
            f"\n## IPS ratio, {name}: simulated / predicted\n\n"
            + coverage_table(results, campaign, "ips_ratio")
        )
    for campaign, name in NAMES.items():
        print(
            f"\n## Click rate of the BTS log, {name}\n\n"
            + coverage_table(results, campaign, "v_on")
        )
    print("\n## Widening\n\n" + widening_table(results))
    print("\n## Dependence\n\n" + dependence_table(results))
    print("\n## Predictions\n\n" + prediction_table(results))
    print("\n## Reading\n\n" + json.dumps(results["reading"], indent=1))


if __name__ == "__main__":
    main()
