"""Run the registered analysis.

    python -m obd.run men            the development campaign
    python -m obd.run all women      the confirmatory campaigns and the pooled unit
    python -m obd.run --check all    only the stop checks of Section 2

Results go to obd/results/<campaign>.json and pooled.json.
"""

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

from obd import data, tables, verdicts
from obd import estimators as est

PREREGISTRATION = "08ab8da8301409b0ffd2eda8b646293c14d74af3"
RESULTS = Path(__file__).parent / "results"
POOL = {"all": 0.54, "women": 0.46}  # Section 4


def bootstrap(t, pi0, width, eligible, n_replicates):
    """The estimates on the full data and their replicates, both by quantity."""
    point = est.estimate(t, pi0, width, eligible)
    replicates = np.array(
        [
            list(est.estimate(t.resample(est.multiplicities(i)), pi0, width, eligible).values())
            for i in range(n_replicates)
        ]
    )
    return point, dict(zip(point, replicates.T, strict=False))


def summarise(estimate, replicates):
    """A quantity with its percentile interval over the replicates in which it is defined."""
    defined = replicates[np.isfinite(replicates)]
    low, high = np.percentile(defined, [2.5, 97.5]) if len(defined) else (np.nan, np.nan)
    return {
        "estimate": float(estimate),
        "interval": [float(low), float(high)],
        "undefined_replicates": len(replicates) - len(defined),
    }


def labelled(quantities, n_replicates, names, rule):
    """`rule` applied to the intervals of the named quantities.

    A quantity undefined in more than 1% of the replicates gets no label.
    """
    undefined = [n for n in names if quantities[n]["undefined_replicates"] > n_replicates / 100]
    if undefined:
        return f"not evaluable: {', '.join(undefined)} undefined in over 1% of replicates"
    return rule(*(quantities[name]["interval"] for name in names))


def h2_label(quantities, n_replicates):
    cells = [name for name in quantities if name.startswith("h2.s.")]
    if len(cells) < 5:  # the first clause of the rule; without cells M is undefined
        return "undetermined"
    m = quantities["h2.m"]["estimate"]
    return labelled(
        quantities,
        n_replicates,
        ["h2.m", *cells],
        lambda m_interval, *intervals: verdicts.h2(m, m_interval, intervals),
    )


def reading(h3_ips, alignment, level):
    """The reading of the gap by H4; none if a label behind it could not be given."""
    if any(label.startswith("not evaluable") for label in (h3_ips, alignment, level)):
        return None
    return verdicts.h4_reading(h3_ips, alignment, level)


def analyse(data_dir, campaign, n_replicates=est.N_REPLICATES):
    """Every proposition on one campaign: the result and the replicates by quantity."""
    alpha, beta = data.read_prior(data_dir, campaign)
    n_items = len(alpha)
    pi0 = est.fixed_prior_target(alpha, beta, data.CAMPAIGNS.index(campaign))
    random, bts = (
        data.read_log(data.to_parquet(data_dir, policy, campaign)) for policy in ("random", "bts")
    )
    t, facts = tables.build(random, bts, alpha / (alpha + beta))
    del random, bts

    width, coverage = est.choose_width(est.hours(t.b_rows), est.hours(t.r_rows))
    eligible = est.eligible_cells(facts["min_propensity"])
    point, replicates = bootstrap(t, pi0, width, eligible, n_replicates)
    q = {name: summarise(point[name], replicates[name]) for name in point}
    for name, summary in q.items():
        if name.startswith("h4.rho."):
            summary["replicate_median"] = float(np.nanmedian(replicates[name]))
        if name.startswith("h4.share."):
            summary["replicate_mean"] = float(np.nanmean(replicates[name]))

    def label(rule, *names):
        return labelled(q, n_replicates, names, rule)

    b_rows, r_rows = t.b_rows.sum(axis=1), t.r_rows.sum(axis=1)  # [block, item, position]
    h1 = est.h1(b_rows, pi0)
    cells = [name for name in q if name.startswith("h2.s.")]
    h3 = {name: label(verdicts.h3, f"h3.{name}") for name in ("ips", "snips")}
    h4 = {"alignment": None, "level": None, "reading": None}
    if q[f"h4.share.{width}.dropped"]["estimate"] <= 0.001:
        h4["alignment"] = label(verdicts.h4_alignment, f"h4.d.{width}")
        h4["level"] = label(verdicts.h4_level, f"h4.rho.{width}")
        h4["reading"] = reading(h3["ips"], h4["alignment"], h4["level"])
    inv_p = t.b_inv_p.sum()
    written, hourly = facts["users_as_written"], np.ones(tables.HOURS)
    result = {
        "campaign": campaign,
        "items": n_items,
        "rows": {"random": r_rows.sum(), "bts": b_rows.sum()},
        "rows_outside_week": facts["rows_outside_week"],
        "h1": h1
        | {
            "label": verdicts.h1(h1["d"], h1["d0"]),
            "random_log_against_uniform": est.h1(r_rows, np.full(pi0.shape, 1 / n_items)),
        },
        "h2": {
            "label": h2_label(q, n_replicates),
            "eligible_cells": len(cells),
            "eligible_share_of_rows": b_rows.sum(axis=0)[eligible].sum() / b_rows.sum(),
            "cells_with_1_in_interval": sum(
                q[c]["interval"][0] <= 1 <= q[c]["interval"][1] for c in cells
            ),
            "mean_inverse_propensity_by_position": (
                t.b_inv_p.sum(axis=(0, 1)) / b_rows.sum(axis=(0, 1))
            ).tolist(),
            "rows_below_1e-5": facts["rows_below_1e-5"],
            "rows_off_grid": facts["rows_off_grid"],
        },
        "h3": h3,
        "h4": {"width": width, "coverage": coverage, "evaluable": h4["level"] is not None} | h4,
        "h5": {"label": label(verdicts.h5, "h5.after_minus_before")},
        "h6": {
            "ips": label(verdicts.h6, "h6.ips"),
            "snips": label(verdicts.h6, "h6.snips"),
            "effective_sample_size": inv_p**2 / facts["sum_inv_p_squared"],
            "largest_weight": 1 / (n_items * facts["min_propensity"].min()),
            "share_of_weights_below_0.001": facts["low_inv_p"] / inv_p,
            "share_of_weighted_clicks_below_0.001": facts["low_inv_p_clicks"]
            / t.b_inv_p_clicks.sum(),
        },
        "h7": {
            "values_matched": facts["user_values_matched"],
            "as_written": {
                name: distance
                for name, distance in est.user_distances(
                    written["bts"], written["random"], hourly, hourly, written["features"]
                ).items()
                if name != "hours"
            },
            "between_alternate_blocks": {
                "bts": est.between_alternate_blocks(
                    t.b_users, b_rows.sum(axis=(1, 2)), t.user_features
                ),
                "random": est.between_alternate_blocks(
                    t.r_users, r_rows.sum(axis=(1, 2)), t.user_features
                ),
            },
        },
        "exploratory": {
            "impressions": facts["impressions"],
            "complete_impressions": facts["complete_impressions"],
        },
        "quantities": q,
    }
    return result, replicates


def pool(results, replicates, n_replicates=est.N_REPLICATES):
    """The pooled unit of Section 4, combined replicate by replicate."""
    q = {}
    for name in ("h3.ips", "h3.snips", "h4.rho", "h4.d"):
        own = {
            c: name if name.startswith("h3") else f"{name}.{results[c]['h4']['width']}"
            for c in POOL
        }
        estimate = {c: results[c]["quantities"][own[c]]["estimate"] for c in POOL}
        draws = {c: replicates[c][own[c]] for c in POOL}
        q[name] = summarise(
            sum(POOL[c] * estimate[c] for c in POOL), sum(POOL[c] * draws[c] for c in POOL)
        )
        q[name + ".all_minus_women"] = summarise(
            estimate["all"] - estimate["women"], draws["all"] - draws["women"]
        )

    def label(rule, name):
        return {
            "label": labelled(q, n_replicates, [name], rule),
            "campaigns_differ": labelled(
                q, n_replicates, [name + ".all_minus_women"], verdicts.campaigns_differ
            ),
        }

    result = {
        "weights": POOL,
        "h3": {"ips": label(verdicts.h3, "h3.ips"), "snips": label(verdicts.h3, "h3.snips")},
        "h4": None,
        "quantities": q,
    }
    if all(results[c]["h4"]["evaluable"] for c in POOL):
        alignment = label(verdicts.h4_alignment, "h4.d")
        level = label(verdicts.h4_level, "h4.rho")
        result["h4"] = {
            "widths": {c: results[c]["h4"]["width"] for c in POOL},
            "alignment": alignment,
            "level": level,
            "reading": reading(result["h3"]["ips"]["label"], alignment["label"], level["label"]),
        }
    return result


def run(data_dir, campaigns):
    """Section 2 checks of every campaign, then the analysis: results by unit.

    Nothing but the checks is computed if a campaign stops. Both confirmatory
    campaigns are checked before either is analysed (Section 9).
    """
    to_check = {*campaigns, *POOL} if set(campaigns) & set(POOL) else campaigns
    checks = data.check(data_dir, [c for c in data.CAMPAIGNS if c in to_check])
    stops = {name: report["stops"] for name, report in checks.items() if report["stops"]}
    if stops:
        raise SystemExit(f"stopped by the checks of Section 2: {json.dumps(stops, indent=1)}")
    results, replicates = {}, {}
    for campaign in campaigns:
        results[campaign], replicates[campaign] = analyse(data_dir, campaign)
        results[campaign]["checks"] = {
            name: report for name, report in checks.items() if name.endswith("/" + campaign)
        }
    if set(POOL) <= set(campaigns):
        results["pooled"] = pool(results, replicates)
    return results


def _code_commit():
    """The commit of the code, marked if the code differs from it."""

    def git(*args):
        done = subprocess.run(
            ["git", *args], cwd=RESULTS.parent, capture_output=True, text=True, check=True
        )
        return done.stdout.strip()

    changed = git("status", "--porcelain", "--", ".", ":(exclude)results")
    return git("rev-parse", "HEAD") + ("-dirty" if changed else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("campaigns", nargs="+", choices=data.CAMPAIGNS)
    parser.add_argument("--check", action="store_true", help="only the checks of Section 2")
    parser.add_argument("--data-dir", type=Path, default=data.DEFAULT_DIR)
    args = parser.parse_args()
    data.fetch(args.data_dir)
    if args.check:
        print(json.dumps(data.check(args.data_dir, args.campaigns), indent=1))
        return
    provenance = {
        "preregistration_commit": PREREGISTRATION,
        "code_commit": _code_commit(),
        "numpy": np.__version__,
        "replicates": est.N_REPLICATES,
        "command": "python -m obd.run " + " ".join(args.campaigns),
    }
    RESULTS.mkdir(exist_ok=True)
    for unit, result in run(args.data_dir, args.campaigns).items():
        text = json.dumps(provenance | result, indent=1, default=lambda x: x.item())
        (RESULTS / f"{unit}.json").write_text(text + "\n")
        print(f"wrote {RESULTS / unit}.json")


if __name__ == "__main__":
    main()
