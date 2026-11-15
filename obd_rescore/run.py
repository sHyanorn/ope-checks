"""The registered run (Section 9 of the registration).

    python -m obd_rescore.run [--work-dir DIR]

DIR (default ~/.cache/ope-checks/rescore) holds the environments and the third-party
code that setup.sh writes; the run adds the data and its state there. The same command
resumes a stopped run. Results go to obd_rescore/results/.
"""

import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow

from obd import data
from obd_rescore import envs, logs, references, rules

REGISTRATION = "78c077ab8e7e929e22118a507b57e0720d31e8fe"
COMMITS = {
    "icml2022-mips": "08d65ce04d597d2f7660bfb6da93bf77c86f8b1b",
    "meta-ope-recsys-2025": "f77886a93358a5063656ff073539a03b04d4bb53",
    "recsys2024_optimal_baseline": "137cdbe2488f434f0dbc2997f5bec1194b874a27",
}
RESULTS = Path(__file__).parent / "results"
WORK_DIR = Path.home() / ".cache" / "ope-checks" / "rescore"
COMMAND = "python -m obd_rescore.run"
N_ITEMS = {"all": 80, "men": 34, "women": 46}
ARMS, TARGETS = ("rows", "blocks"), ("published", "own")
C1_ESTIMATORS = ("ips", "mips", "mips_slope")
OTHERS = ("IPS", "SNIPS", "bIPS", "DR", "DM")  # reported with BLUE (Section 2.2)
PUBLISHED = {  # cells 45 and 42 of the notebook, Men's
    "BLUE": 0.006687691524532561,
    "IPS": 0.006010953776252967,
    "SNIPS": 0.00612731824047759,
    "bIPS": 0.006152023858050668,
    "DR": 0.006118951440097642,
    "DM": 0.005127094504168594,
    "V_on": 0.006742727014339116,
}
STOP_DIFFERENCE = 1e-9  # Section 6: R_IPS and R_SNIPS against the IPS and SNIPS of BLUE
SIZES = {"runs": 500, "replication_runs": 150, "replicates": 2000, "sample": logs.SAMPLE}


def now():
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")


def dump(path, value):
    path.write_text(json.dumps(value, indent=1) + "\n")


class Run:
    """The state of a run in DIR/run, and its jobs in the published environments."""

    def __init__(self, work_dir, sizes, slots):
        self.work, self.sizes, self.slots = work_dir, sizes, slots
        self.data, self.state = work_dir / "data", work_dir / "run"
        self.obp_data = self.data / logs.ROOT
        self.src = envs.sources(work_dir)
        for sub in ("tables", "c1", "c2", "logs"):
            (self.state / sub).mkdir(parents=True, exist_ok=True)

    def event(self, **line):
        with open(self.state / "events.jsonl", "a") as f:
            f.write(json.dumps({"time": now()} | line) + "\n")

    def jobs(self, jobs):
        """Run adapter commands, at most `slots` at a time; each resumes from what it wrote."""
        waiting, running = list(jobs), []
        while waiting or running:
            while waiting and len(running) < self.slots:
                name, command = waiting.pop(0)
                log = open(self.state / "logs" / f"{name}.log", "a")
                process = subprocess.Popen(
                    command, stdout=log, stderr=subprocess.STDOUT, env=envs.environ()
                )
                running.append((name, process, log))
            time.sleep(1)
            for job in [job for job in running if job[1].poll() is not None]:
                running.remove(job)
                job[2].close()
                if job[1].returncode:
                    for _, other, _ in running:
                        other.terminate()
                    raise SystemExit(f"{job[0]} failed; see {self.state}/logs/{job[0]}.log")

    def tables(self, policy, campaign):
        path = self.state / "tables" / f"{policy}_{campaign}.npz"
        if not path.exists():
            part = path.with_suffix(".part.npz")
            np.savez(part, **logs.tables(self.data, policy, campaign, N_ITEMS[campaign]))
            part.replace(path)
        with np.load(path) as saved:
            return dict(saved)

    def pi(self, campaign):
        return self.state / "c1" / f"pi_{campaign}.npy"

    def targets(self, campaign):
        args = ["targets", self.src["mips"], campaign, self.pi(campaign)]
        args += ["--runs", self.sizes["runs"]]
        if self.pi(campaign).exists():
            return []
        return [(f"pi_{campaign}", envs.adapter(self.work, "mips", *args))]

    def c1(self, name, campaign, *options):
        blocks = self.state / "c1" / f"blocks_{campaign}.npy"
        if not blocks.exists():
            np.save(
                blocks, [logs.c1_multiplicities(campaign, t) for t in range(self.sizes["runs"])]
            )
        out = self.state / "c1" / f"{name}.jsonl"
        args = [self.src["mips"], self.obp_data, campaign, self.pi(campaign), blocks, out]
        options = [*options, "--sample", self.sizes["sample"]]
        return name, envs.adapter(self.work, "mips", "runs", *args, *options)

    def full(self, campaign):
        out = self.state / "c2" / campaign
        if (out / "full.json").exists():
            return []
        args = [self.src["blue"], self.src["notebook"], self.obp_data, campaign, out]
        return [(f"full_{campaign}", envs.adapter(self.work, "blue", "full", *args))]

    def c2(self, name, campaign, blocks):
        out = self.state / "c2" / f"{name}.jsonl"
        args = [self.src["notebook"], self.state / "c2" / campaign, blocks, out]
        return name, envs.adapter(self.work, "blue", "replicates", *args)

    def read(self, name):
        """The lines of an adapter's record, without its inputs."""
        path = self.state / f"{name}.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()[1:]]

    def inputs(self, name):
        with open(self.state / f"{name}.jsonl") as f:
            return json.loads(f.readline())["inputs"]

    def full_data(self, campaign):
        return json.loads((self.state / "c2" / campaign / "full.json").read_text())


def replication(r):
    """Section 8.5, before any estimate, reference or label other than its own."""
    v_on = {c: logs.on_policy_value(r.tables("bts", c)) for c in ("all", "men")}
    n = r.sizes["replication_runs"]
    halves = [(0, n // 2 - 1), (n // 2, n - 1)]
    r.jobs(r.targets("all") + r.full("men"))
    only = ["--arms", "rows", "--targets", "published", "--estimators", "ips", "mips_slope"]
    r.jobs([r.c1(f"replication_{a}", "all", *only, "--first", a, "--last", b) for a, b in halves])
    lines = sorted(
        (x for a, _ in halves for x in r.read(f"c1/replication_{a}")), key=lambda x: x["t"]
    )
    assert [x["t"] for x in lines] == list(range(n))
    comparison = rules.compare(
        [x["mips_slope"] for x in lines], [x["ips"] for x in lines], v_on["all"]
    )
    values = {name: x[0] for name, x in r.full_data("men")["blue"].items()}
    values["V_on"] = v_on["men"]
    return {
        "c1": {"label": rules.replication_c1(comparison), "comparison": comparison},
        "c2": rules.replication_c2(values, PUBLISHED) | {"values": values, "published": PUBLISHED},
    }


def c1_cell(estimates, refs, v_on, men):
    """Section 8.2 for one campaign, arm and target, with what Section 8.6 reports.

    `estimates` and `refs` map each estimator and reference to its value in each run.
    """
    comparisons = {
        name: rules.compare(estimates["mips_slope"], estimates["ips"], v)
        for name, v in refs.items()
    }
    without_slope = {}
    for name, v in refs.items():
        comparison = rules.compare(estimates["mips"], estimates["ips"], v)
        without_slope[name] = {k: x for k, x in comparison.items() if k != "label"}
    target = comparisons["r_ips"]["label"]
    if men:
        target = rules.across_references(target, comparisons["r_snips"]["label"])
    return {
        "label_v_on": comparisons["v_on"]["label"],
        "label_target": target,
        "comparisons": comparisons,
        "without_slope": without_slope,
        "mean_error_over_v_on": {
            name: {k: float(np.mean((e - v) / v_on)) for k, e in estimates.items()}
            for name, v in refs.items()
        },
    }


def c1_campaign(r, campaign, v_on, random):
    """Every cell of C1 on one campaign, and its lines run by run."""
    n, men = r.sizes["runs"], campaign == "men"
    files = [f"{campaign}_rows", f"{campaign}_blocks"] if campaign == "all" else [campaign]
    read = [x for f in files for x in r.read(f"c1/{f}")]
    lines = {(x["t"], x["arm"], x["target"]): x for x in read}
    assert len(read) == len(lines), f"{campaign}: a run was written twice"
    assert sorted(lines) == sorted((t, a, g) for t in range(n) for a in ARMS for g in TARGETS)
    pis = np.load(r.pi(campaign))[:n]
    out = {"cells": {}, "mean_r_ips_over_v_on": {}}
    for target in TARGETS:
        values = references.values(random, references.applied(pis, target))
        refs = {"v_on": v_on, "r_ips": values["r_ips"]}
        if men:
            refs["r_snips"] = values["r_snips"]
        out["mean_r_ips_over_v_on"][target] = float(np.mean(values["r_ips"] / v_on))
        for arm in ARMS:
            runs = [lines[t, arm, target] for t in range(n)]
            for t, x in enumerate(runs):
                x |= {name: float(v[t]) for name, v in refs.items() if name != "v_on"}
            estimates = {k: np.array([x[k] for x in runs]) for k in C1_ESTIMATORS}
            cell = c1_cell(estimates, refs, v_on, men)
            rows = [x["rows"] for x in runs]
            cell["rows"] = {"min": min(rows), "mean": float(np.mean(rows)), "max": max(rows)}
            out["cells"][f"{arm}/{target}"] = cell
    return out, [lines[key] for key in sorted(lines)]


def c2_labels(draws, refs, men):
    """Section 8.3, secondary, and 8.4: BLUE against each estimator under each reference."""
    out = {}
    for name, v in refs.items():
        comparisons = {x: rules.compare(draws["BLUE"], draws[x], v) for x in OTHERS}
        label = rules.across_estimators([c["label"] for c in comparisons.values()])
        out[name] = {"label": label, "comparisons": comparisons}
    target = out["r_ips"]["label"]
    if men:
        target = rules.across_references(target, out["r_snips"]["label"])
    return {"label_v_on": out["v_on"]["label"], "label_target": target, "by_reference": out}


def c2_campaign(r, campaign, v_on, r_values, bts):
    """Section 8.3 on one campaign, with what Section 8.6 reports, and its replicates."""
    lines = sorted(r.read(f"c2/{campaign}_replicates"), key=lambda x: x["i"])
    assert [x["i"] for x in lines] == list(range(r.sizes["replicates"]))
    draws = {name: np.array([x[name] for x in lines]) for name in ("BLUE", *OTHERS)}
    m = np.load(r.state / "c2" / "blocks.npy")[: len(lines)].astype(float)
    v_on_i = (m @ bts["clicks"].sum(axis=(1, 2))) / (m @ bts["rows"].sum(axis=(1, 2)))
    for x, v in zip(lines, v_on_i, strict=True):
        x["v_on_i"] = float(v)
    refs = {"v_on": v_on, "r_ips": r_values["r_ips"]}
    if campaign == "men":
        refs["r_snips"] = r_values["r_snips"]
    full = r.full_data(campaign)["blue"]
    estimate = {name: x[0] for name, x in full.items()}
    compact = r.read(f"c2/{campaign}_compact")[0]
    closer = {x: bool(abs(estimate["BLUE"] - v_on) < abs(estimate[x] - v_on)) for x in OTHERS}
    differences = draws["BLUE"] - v_on_i
    return {
        "unbiasedness": rules.unbiasedness(draws["BLUE"], draws["IPS"]),
        **c2_labels(draws, refs, campaign == "men"),
        "full_data": full,
        "compact_minus_full": {name: compact[name] - estimate[name] for name in estimate},
        "blue_closer_to_v_on_on_full_data": closer,
        "blue_minus_r_ips": estimate["BLUE"] - refs["r_ips"],
        "blue_minus_v_on": estimate["BLUE"] - v_on,
        "blue_minus_v_on_i": [
            float(x) for x in np.percentile(differences, [2.5, 97.5], method="linear")
        ],
        "replicate_sd": {name: float(np.std(x, ddof=1)) for name, x in draws.items()},
        "replicate_rows": [min(x["rows"] for x in lines), max(x["rows"] for x in lines)],
    }, lines


def labels(c1_results, c2_results):
    """Every label, with the primary labels of Section 8.4 first."""
    c1 = {
        c: {
            cell: {k: x[k] for k in ("label_v_on", "label_target")}
            for cell, x in out["cells"].items()
        }
        for c, out in c1_results.items()
    }
    c2 = {
        c: {
            "unbiasedness": x["unbiasedness"]["label"],
            "label_v_on": x["label_v_on"],
            "label_target": x["label_target"],
        }
        for c, x in c2_results.items()
    }
    primary = {
        "c1_all_blocks_own_against_the_target": c1["all"]["blocks/own"]["label_target"],
        "c2_men_unbiasedness": c2["men"]["unbiasedness"],
    }
    return {"primary": primary, "c1": c1, "c2": c2}


def provenance(r, commit):
    """Versions, commits and the files used; stops if the code or a prior is not registered."""
    out = {
        "registration_commit": REGISTRATION,
        "code_commit": commit,
        "command": COMMAND,
        "archive_sha256": data.ARCHIVE_SHA256,
        "study": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "pyarrow": pyarrow.__version__,
        },
        "third_party_commits": {},
    }
    for name in COMMITS:
        git = ["git", "-C", r.work / "src" / name, "rev-parse", "HEAD"]
        out["third_party_commits"][name] = subprocess.run(
            git, capture_output=True, text=True, check=True
        ).stdout.strip()
    if out["third_party_commits"] != COMMITS:
        raise SystemExit("the third-party code is not at the registered commits")
    for env, args in [("mips", [r.src["mips"]]), ("blue", [r.src["blue"], r.src["notebook"]])]:
        done = subprocess.run(
            envs.adapter(r.work, env, "environment", *args),
            capture_output=True,
            text=True,
            check=True,
            env=envs.environ(),
        )
        out[env] = json.loads(done.stdout)
        priors = [h for path, h in out[env]["files"].items() if path.endswith(data.PRIOR)]
        if priors != [data.PRIOR_SHA256]:
            raise SystemExit(f"the prior of environment {env} is not the registered file")
    return out


def run(work_dir=WORK_DIR, sizes=SIZES, slots=4, commit=None):
    """Section 9: the stop checks, both replications, then everything else."""
    if not np.__version__.startswith("2.5."):
        raise SystemExit("the registered random streams are those of numpy 2.5")
    r = Run(work_dir, sizes, slots)
    r.event(event="start", commit=commit)
    about = provenance(r, commit)

    data.fetch(r.data)
    if not (r.state / "checks.json").exists():
        dump(r.state / "checks.json", data.check(r.data, data.CAMPAIGNS))
    checks = json.loads((r.state / "checks.json").read_text())
    stops = {name: report["stops"] for name, report in checks.items() if report["stops"]}
    if stops:
        raise SystemExit(f"stopped by the checks of Section 3: {json.dumps(stops, indent=1)}")
    logs.extract(r.data, r.data, [("random", c) for c in N_ITEMS] + [("bts", "men")])

    if not (r.state / "replication.json").exists():
        dump(r.state / "replication.json", replication(r))
        r.event(event="replications written")
    RESULTS.mkdir(exist_ok=True)
    dump(RESULTS / "replication.json", json.loads((r.state / "replication.json").read_text()))

    tables = {(p, c): r.tables(p, c) for c in N_ITEMS for p in ("random", "bts")}
    v_on = {c: logs.on_policy_value(tables["bts", c]) for c in N_ITEMS}
    c2_blocks, ones = r.state / "c2" / "blocks.npy", r.state / "c2" / "ones.npy"
    if not c2_blocks.exists():
        np.save(c2_blocks, [logs.c2_multiplicities(i) for i in range(sizes["replicates"])])
    np.save(ones, np.ones((1, data.N_BLOCKS), int))
    on_policy = r.state / "c2" / "on_policy_men.json"
    args = ["on-policy", r.src["blue"], r.obp_data, "men", on_policy]
    on_policy_job = [("on_policy_men", envs.adapter(r.work, "blue", *args))]
    # the full data of All (about 9.8 GB) with the targets only; then the full data of
    # Women's with obp's V_on of Men's (about 3.7 and 6.2 GB)
    r.jobs(r.full("all") + r.targets("men") + r.targets("women"))
    r.jobs(r.full("women") + ([] if on_policy.exists() else on_policy_job))
    last = ["--last", sizes["runs"] - 1]
    r.jobs(
        [
            r.c1("all_rows", "all", "--arms", "rows", *last),
            r.c1("all_blocks", "all", "--arms", "blocks", *last),
            r.c1("women", "women", *last),
            r.c1("men", "men", *last),
        ]
        + [r.c2(f"{c}_compact", c, ones) for c in N_ITEMS]
        + [r.c2(f"{c}_replicates", c, c2_blocks) for c in ("men", "women", "all")]
    )
    r.event(event="jobs done")

    # obp read every row; the run repeats the replication; T7 on OBD before any label
    for campaign in N_ITEMS:
        files = [f"{campaign}_rows", f"{campaign}_blocks"] if campaign == "all" else [campaign]
        read = [r.inputs(f"c1/{f}")["log_rows"] for f in files]
        read += [r.full_data(campaign)["rows"], r.read(f"c2/{campaign}_compact")[0]["rows"]]
        if set(read) != {data.ROWS["random", campaign]}:
            raise SystemExit(f"obp read {read} rows of the random log of {campaign}")
    for campaign in N_ITEMS:  # the adapters drew the blocks this side numbers
        per_block = tables["random", campaign]["rows"].sum(axis=(1, 2))
        c1_blocks = np.load(r.state / "c1" / f"blocks_{campaign}.npy") @ per_block
        file = "all_blocks" if campaign == "all" else campaign
        c1_rows = {x["t"]: x["rows"] for x in r.read(f"c1/{file}") if x["arm"] == "blocks"}
        c2_rows = [
            x["rows"] for x in sorted(r.read(f"c2/{campaign}_replicates"), key=lambda x: x["i"])
        ]
        if c1_rows != dict(enumerate(c1_blocks[: sizes["runs"]])) or c2_rows != list(
            np.load(c2_blocks)[: sizes["replicates"]] @ per_block
        ):
            raise SystemExit(
                f"the adapters and this side assign the rows of {campaign} to other blocks"
            )
    main_rows = {x["t"]: x for x in r.read("c1/all_rows") if x["target"] == "published"}
    halves = (0, sizes["replication_runs"] // 2)
    for x in (x for a in halves for x in r.read(f"c1/replication_{a}")):
        if any(x[k] != main_rows[x["t"]][k] for k in ("rows", "ips", "mips_slope")):
            raise SystemExit(f"run {x['t']} does not repeat the replication")
    r_values, check = {}, {}
    for campaign in N_ITEMS:
        target = np.load(r.state / "c2" / campaign / "target.npy")
        r_values[campaign] = {
            k: float(v) for k, v in references.values(tables["random", campaign], target).items()
        }
        blue = r.full_data(campaign)["blue"]
        check[campaign] = {
            name: abs(r_values[campaign][key] / blue[name][0] - 1)
            for key, name in (("r_ips", "IPS"), ("r_snips", "SNIPS"))
        }
    if not all(d <= STOP_DIFFERENCE for c in check.values() for d in c.values()):
        dump(RESULTS / "stop.json", check)
        raise SystemExit(f"R_IPS or R_SNIPS differs from BLUE's IPS or SNIPS: {check}")

    c1_results, c2_results, lines = {}, {}, {}
    refs = {}
    for campaign in N_ITEMS:
        random, bts = tables["random", campaign], tables["bts", campaign]
        c1_results[campaign], lines["c1", campaign] = c1_campaign(
            r, campaign, v_on[campaign], random
        )
        c2_results[campaign], lines["c2", campaign] = c2_campaign(
            r, campaign, v_on[campaign], r_values[campaign], bts
        )
        pis = np.load(r.pi(campaign))[: sizes["runs"]].mean(axis=0)
        c2_target = np.load(r.state / "c2" / campaign / "target.npy")
        refs[campaign] = {"v_on": v_on[campaign]}
        for name, pi_star in [
            ("c1_published", references.applied(pis, "published")),
            ("c1_own", pis),
            ("c2", c2_target),
        ]:
            values = {k: float(v) for k, v in references.values(random, pi_star).items()}
            refs[campaign][name] = values | {
                "intervals": references.intervals(random, bts, pi_star)
            }
    refs["men"]["on_policy_value_by_obp"] = json.loads(on_policy.read_text())["v_on"]
    refs["stop_check_relative_differences"] = check

    r.event(event="results written")
    events = [json.loads(x) for x in (r.state / "events.jsonl").read_text().splitlines()]
    RESULTS.mkdir(exist_ok=True)
    dump(RESULTS / "provenance.json", about | {"sizes": sizes, "events": events})
    dump(RESULTS / "checks.json", checks)
    dump(RESULTS / "references.json", refs)
    dump(RESULTS / "labels.json", labels(c1_results, c2_results))
    dump(RESULTS / "c1.json", c1_results)
    dump(RESULTS / "c2.json", c2_results)
    for (claim, campaign), rows in lines.items():
        (RESULTS / claim).mkdir(exist_ok=True)
        text = "".join(json.dumps(x) + "\n" for x in rows)
        (RESULTS / claim / f"{campaign}.jsonl").write_text(text)
    return {"c1": c1_results, "c2": c2_results}


def code_commit():
    """The commit of the code; the run refuses code that differs from it."""

    def git(*args):
        done = subprocess.run(
            ["git", *args], cwd=RESULTS.parent, capture_output=True, text=True, check=True
        )
        return done.stdout.strip()

    if git("status", "--porcelain", "--", ".", "../obd", ":(exclude)results"):
        raise SystemExit("obd_rescore or obd differs from its commit")
    return git("rev-parse", "HEAD")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--work-dir", type=Path, default=WORK_DIR)
    args = parser.parse_args()
    commit = code_commit()
    events = args.work_dir / "run" / "events.jsonl"
    if events.exists():
        lines = [json.loads(x) for x in events.read_text().splitlines()]
        started = {x["commit"] for x in lines if x["event"] == "start"}
        if started - {commit}:
            raise SystemExit(f"the run was started at {started}, not at {commit}")
    try:
        run(args.work_dir, commit=commit)
    except SystemExit as stop:
        with open(events, "a") as f:
            f.write(json.dumps({"time": now(), "event": "stopped", "reason": str(stop)}) + "\n")
        raise


if __name__ == "__main__":
    main()
