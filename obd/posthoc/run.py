"""Run the post hoc analyses.

    python -m obd.posthoc.run                    all seven
    python -m obd.posthoc.run units features     some of them

Results go to obd/posthoc/results/<analysis>.json. The data directory is that of `obd.run`.
"""

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

from obd import data
from obd import estimators as est
from obd.posthoc import blocks, distances, features, lengths, prior, propensities, units
from obd.run import POOL

HERE = Path(__file__).parent
RESULTS = HERE / "results"
REGISTERED = HERE.parent / "results"


def load(data_dir, policy, campaign, columns=None):
    """A log, converted if needed, without the rows outside the week.

    With `columns`, only those are read.
    """
    path = data.to_parquet(data_dir, policy, campaign)
    log = pq.read_table(path, columns=columns).to_pandas() if columns else data.read_log(path)
    since = log["timestamp"] - data.WEEK_START_US
    return log[(since >= 0) & (since < data.N_BLOCKS * data.BLOCK_US)]


def resampling_units(data_dir):
    out = {}
    for stream, campaign in enumerate(data.CAMPAIGNS):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        pi0 = est.fixed_prior_target(*data.read_prior(data_dir, campaign), stream)
        out[campaign] = {
            "h3": units.h3_by_unit(random, bts, pi0, stream),
            "dependence": {"random": units.dependence(random), "bts": units.dependence(bts)},
        }
    return out


def unmatched_features(data_dir):
    out = {}
    for campaign in ("all", "women"):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        found = features.one_log_values(random, bts)
        pairs = features.same_category(found)
        out[campaign] = found | {"taken_as_one_value": pairs}
        if not pairs:
            continue
        registered = json.loads((REGISTERED / f"{campaign}.json").read_text())["quantities"]
        post_hoc = features.quantities(
            features.rewritten(random, pairs),
            bts,
            *data.read_prior(data_dir, campaign),
            data.CAMPAIGNS.index(campaign),
        )
        moved = differing(registered, post_hoc)
        if moved:  # only H7 reads the user features
            raise SystemExit(f"{campaign}: differs from the registered result: {moved}")
        out[campaign]["h7"] = {
            name: {"registered": registered[name], "post_hoc": post_hoc[name]}
            for name in registered
            if name.startswith("h7.")
        }
    return out


def differing(registered, post_hoc):
    """The quantities outside H7 whose estimate or interval is not the registered one."""
    return [
        name
        for name in registered
        if not name.startswith("h7.")
        and not np.allclose(
            [post_hoc[name]["estimate"], *post_hoc[name]["interval"]],
            [registered[name]["estimate"], *registered[name]["interval"]],
            rtol=1e-9,
            atol=0,
            equal_nan=True,
        )
    ]


def propensity_identity(data_dir):
    return {
        campaign: propensities.analyse(
            load(data_dir, "bts", campaign), len(data.read_prior(data_dir, campaign)[0])
        )
        for campaign in data.CAMPAIGNS
    }


def block_lengths(data_dir):
    by_unit = {}
    for stream, campaign in enumerate(data.CAMPAIGNS):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        pi0 = est.fixed_prior_target(*data.read_prior(data_dir, campaign), stream)
        by_unit[campaign] = blocks.h3_by_length(random, bts, pi0)
    by_unit["pooled"] = blocks.pooled(by_unit, POOL)
    out = {unit: blocks.summarise(by_length) for unit, by_length in by_unit.items()}
    for unit, by_length in out.items():
        registered = json.loads((REGISTERED / f"{unit}.json").read_text())["quantities"]
        at_ten = {f"h3.{name}": by_length[blocks.REGISTERED][name] for name in ("ips", "snips")}
        moved = differing({name: registered[name] for name in at_ten}, at_ten)
        if moved:
            raise SystemExit(f"{unit}: differs from the registered result: {moved}")
    return {"minutes": blocks.MINUTES, "weights": POOL} | out


def registered_quantities(unit, names):
    """Quantities of a registered result file under the names given: {name: registered name}."""
    q = json.loads((REGISTERED / f"{unit}.json").read_text())["quantities"]
    return {name: q[theirs] for name, theirs in names.items()}


def other_intervals(data_dir):
    by_unit, names = {}, {}
    for stream, campaign in enumerate(data.CAMPAIGNS):
        random, bts = (load(data_dir, policy, campaign) for policy in ("random", "bts"))
        pi0 = est.fixed_prior_target(*data.read_prior(data_dir, campaign), stream)
        width = json.loads((REGISTERED / f"{campaign}.json").read_text())["h4"]["width"]
        by_unit[campaign] = lengths.by_length(random, bts, pi0, width)
        names[campaign] = {
            name: f"{name}.{width}" if name in ("h4.rho", "h4.d") else name
            for name in by_unit[campaign][blocks.REGISTERED][0]
        }
    by_unit["pooled"] = lengths.pooled(by_unit, POOL)
    names["pooled"] = {name: name for name in lengths.POOLED}
    out = {unit: lengths.summarise(by_length) for unit, by_length in by_unit.items()}
    h3 = json.loads((RESULTS / "blocks.json").read_text())
    for unit, by_length in out.items():
        moved = differing(registered_quantities(unit, names[unit]), by_length[blocks.REGISTERED])
        moved += [
            f"h3.ips at {minutes} minutes"
            for minutes, q in by_length.items()
            if not np.allclose(
                q["h3.ips"]["interval"], h3[unit][str(minutes)]["ips"]["interval"], rtol=1e-9
            )
        ]
        if moved:
            raise SystemExit(f"{unit}: differs from an earlier result: {moved}")
    return {"minutes": blocks.MINUTES, "weights": POOL} | out


def prior_distances(data_dir):
    out = {}
    for stream, campaign in enumerate(data.CAMPAIGNS):
        alpha, beta = data.read_prior(data_dir, campaign)
        registered = json.loads((REGISTERED / f"{campaign}.json").read_text())["h1"]
        targets = {
            "bts": (est.fixed_prior_target(alpha, beta, stream), registered),
            "random": (
                np.full((len(alpha), 3), 1 / len(alpha)),
                registered["random_log_against_uniform"],
            ),
        }
        out[campaign] = {}
        for policy, (target, want) in targets.items():
            log = load(data_dir, policy, campaign, distances.COLUMNS)
            got = distances.analyse(distances.rows_by_block(log, len(alpha)), target)
            if not np.allclose(
                [got["d"], got["d0"], got["left_out"], *got["first_hour"]["distance"]],
                [want["d"], want["d0"], want["left_out"], *want["first_hour"]],
                rtol=1e-9,
            ):
                raise SystemExit(f"{campaign}, {policy}: H1 differs from the registered result")
            out[campaign][policy] = got
    return out


def prior_file(data_dir):
    return prior.shared_pairs({c: data.read_prior(data_dir, c) for c in data.CAMPAIGNS})


ANALYSES = {
    "units": resampling_units,
    "features": unmatched_features,
    "propensities": propensity_identity,
    "blocks": block_lengths,
    "lengths": other_intervals,
    "distances": prior_distances,
    "prior": prior_file,
}


def _code_commit():
    """The commit of the code, marked if the code differs from it."""

    def git(*args):
        done = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, check=True)
        return done.stdout.strip()

    changed = git("status", "--porcelain", "--", ":(glob)../**/*.py")
    return git("rev-parse", "HEAD") + ("-dirty" if changed else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("analyses", nargs="*", choices=list(ANALYSES))
    parser.add_argument("--data-dir", type=Path, default=data.DEFAULT_DIR)
    args = parser.parse_args()
    data.fetch(args.data_dir)
    provenance = {
        "post_hoc": True,
        "code_commit": _code_commit(),
        "numpy": np.__version__,
        "replicates": est.N_REPLICATES,
        "command": " ".join(["python -m obd.posthoc.run", *args.analyses]),
    }
    RESULTS.mkdir(exist_ok=True)
    for name in args.analyses or ANALYSES:
        result = provenance | ANALYSES[name](args.data_dir)
        text = json.dumps(result, indent=1, default=lambda x: x.item())
        (RESULTS / f"{name}.json").write_text(text + "\n")
        print(f"wrote {RESULTS / name}.json")


if __name__ == "__main__":
    main()
