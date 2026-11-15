"""Time and memory of the run's steps on synthetic logs of the registered sizes.

    python -m obd_rescore.tests.timing DIR [--work-dir W]

DIR receives the synthetic archive, written once, and the outputs of the steps; W holds
the environments that setup.sh writes. Prints seconds, CPU seconds and peak memory.
"""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

import numpy as np

from obd import data
from obd_rescore import envs, logs
from obd_rescore.run import N_ITEMS, WORK_DIR
from obd_rescore.tests import synthetic

N_RUNS, N_REPLICATES = 3, 20


def measure(commands, log):
    """Run commands at once: wall and CPU seconds and peak GB of each, by name."""
    start, out, running = time.perf_counter(), {}, {}
    with open(log, "a") as f:
        for name, command in commands:
            process = subprocess.Popen(command, stdout=f, stderr=f, env=envs.environ())
            running[process.pid] = name
        while running:
            pid, status, usage = os.wait4(-1, 0)
            name = running.pop(pid)
            if status:
                raise SystemExit(f"{name} failed; see {log}")
            out[name] = {
                "seconds": round(time.perf_counter() - start, 1),
                "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 1),
                "peak_gb": round(usage.ru_maxrss / 2**20, 2),
            }
    return out


def timed(function, *args):
    start = time.perf_counter()
    function(*args)
    return round(time.perf_counter() - start, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("dir", type=Path)
    parser.add_argument("--work-dir", type=Path, default=WORK_DIR)
    args = parser.parse_args()
    d, work, log = args.dir, args.work_dir, args.dir / "timing.log"
    d.mkdir(parents=True, exist_ok=True)
    src = envs.sources(work)
    out = {}
    if not (d / data.ARCHIVE).exists():
        campaigns = {
            c: (n, {p: data.ROWS[p, c] for p in ("random", "bts")}) for c, n in N_ITEMS.items()
        }
        out["write_archive"] = timed(synthetic.write, d, campaigns, np.random.default_rng(0))
    out["stop_checks"] = timed(data.check, d, data.CAMPAIGNS)
    out["extract"] = timed(logs.extract, d, d, [("random", c) for c in N_ITEMS])
    out["tables"] = {
        f"{p}/{c}": timed(logs.tables, d, p, c, n)
        for c, n in N_ITEMS.items()
        for p in ("random", "bts")
    }
    obp_data = d / logs.ROOT

    def mips(*a):
        return envs.adapter(work, "mips", *a)

    def blue(*a):
        return envs.adapter(work, "blue", *a)

    out["full"] = {}
    for c in N_ITEMS:  # one at a time: the full data of All needs most of the memory
        command = blue("full", src["blue"], src["notebook"], obp_data, c, d / "c2" / c)
        out["full"] |= measure([(c, command)], log)
    out["targets"] = measure(
        [
            (c, mips("targets", src["mips"], c, d / f"pi_{c}.npy", "--runs", N_RUNS))
            for c in N_ITEMS
        ],
        log,
    )
    for c in N_ITEMS:
        np.save(d / f"blocks_{c}.npy", [logs.c1_multiplicities(c, t) for t in range(N_RUNS)])

    def c1(name, c, last, *options):
        files = [d / f"pi_{c}.npy", d / f"blocks_{c}.npy", d / f"{name}_{last}.jsonl"]
        return name, mips("runs", src["mips"], obp_data, c, *files, "--last", last, *options)

    groups = [("all_rows", "all", "--arms", "rows"), ("all_blocks", "all", "--arms", "blocks")]
    groups += [("men", "men"), ("women", "women")]
    out["c1_load"] = {}
    for name, c, *options in groups:
        out["c1_load"] |= measure([c1(name, c, -1, *options)], log)
    out["c1_together"] = measure(
        [c1(name, c, N_RUNS - 1, *options) for name, c, *options in groups], log
    )

    np.save(d / "replicates.npy", [logs.c2_multiplicities(i) for i in range(N_REPLICATES)])
    out["c2_load"], out["c2_replicates"] = {}, {}
    for c in N_ITEMS:
        for key, last in (("c2_load", -1), ("c2_replicates", N_REPLICATES - 1)):
            files = [d / "c2" / c, d / "replicates.npy", d / "c2" / f"{c}_{last}.jsonl"]
            command = blue("replicates", src["notebook"], *files, "--last", last)
            out[key] |= measure([(c, command)], log)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
