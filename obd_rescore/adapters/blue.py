"""The adapter of C2, run in environment blue (Section 5 of the registration).

    python -I blue.py full OBP NOTEBOOK DATA CAMPAIGN DIR
    python -I blue.py replicates NOTEBOOK DIR BLOCKS.npy OUT.jsonl [--first I] [--last I]
    python -I blue.py on-policy OBP DATA CAMPAIGN OUT.json
    python -I blue.py environment OBP NOTEBOOK

OBP is the clone of shashankg7/recsys2024_optimal_baseline whose obp the notebook
imports; NOTEBOOK the file "BLUE OPE.ipynb" of olivierjeunen/meta-ope-recsys-2025;
DATA the open_bandit_dataset directory that obp reads. `full` runs the notebook on
the full data and writes to DIR its estimates, the target and the compact inputs of
each row; `replicates` calls BLUE with compact inputs on the rows of each replicate,
BLOCKS holding the multiplicities of the 1008 blocks, one row per replicate; a row of
ones gives the full data.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import Record, block_rows, blocks, environment, package_files, sha256  # noqa: E402

# Cells run on the Open Bandit Dataset, counted from 0: the data (1, 3, 5), the target
# (17), the reward model (22, 23) and its shift (25, 26), BLUE (44) and its call (45).
CELLS = (1, 3, 5, 17, 22, 23, 25, 26, 44, 45)
CAMPAIGN_CELL, DATA_CELL, BLUE_CELL = 3, 5, 44
NOTEBOOK_DATA = "'./obd/'"
CHUNK = 200_000


def cells(notebook):
    return ["".join(cell["source"]) for cell in json.loads(Path(notebook).read_text())["cells"]]


def run_notebook(obp_path, notebook, data, campaign):
    """The namespace of the notebook after its cells on the Open Bandit path."""
    sys.path.insert(0, str(obp_path))
    from IPython.core.interactiveshell import InteractiveShell  # noqa: PLC0415

    sources = cells(notebook)
    if sources[CAMPAIGN_CELL] != 'campaign="men"' or sources[DATA_CELL].count(NOTEBOOK_DATA) != 1:
        raise SystemExit(f"{notebook} is not the registered notebook")
    sources[CAMPAIGN_CELL] = f"campaign = {campaign!r}"
    sources[DATA_CELL] = sources[DATA_CELL].replace(NOTEBOOK_DATA, repr(str(data)))
    shell = InteractiveShell.instance()
    for i in CELLS:
        shell.run_cell(sources[i], silent=True).raise_error()
    return shell.user_ns


def compact_rows(ns):
    """Per row: the logged action and the rest at its position (departure 7)."""
    feedback, q = ns["bandit_feedback"], ns["estimated_rewards_by_reg_model"]
    target = ns["action_dist"][0]  # every row holds the same distribution
    action, position = feedback["action"], feedback["position"]
    n = len(action)
    out = {name: np.empty(n) for name in ("pi_fact", "pi_rest", "q_fact", "q_rest")}
    for start in range(0, n, CHUNK):
        rows = np.arange(start, min(start + CHUNK, n))
        pi = target[:, position[rows]].T  # [row, item] at the row's position
        q_at = q[rows, :, position[rows]]
        fact = (np.arange(len(rows)), action[rows])
        out["pi_fact"][rows], out["q_fact"][rows] = pi[fact], q_at[fact]
        pi[fact] = 0
        rest = pi.sum(axis=1)
        out["pi_rest"][rows] = rest
        weighted = (pi * q_at).sum(axis=1)
        out["q_rest"][rows] = np.divide(weighted, rest, out=np.zeros(len(rows)), where=rest > 0)
    out["reward"], out["pscore"] = feedback["reward"], feedback["pscore"]
    return out


def blue_function(notebook):
    """A namespace holding BLUE, from the source of cell 44."""
    ns = {"np": np}
    exec(cells(notebook)[BLUE_CELL], ns)
    return ns


def compact_call(ns, rows, idx):
    """BLUE on the rows `idx` with compact inputs: the means it returns."""
    n = len(idx)
    feedback = {
        "action": np.zeros(n, int),
        "position": np.zeros(n, int),
        "reward": rows["reward"][idx],
        "pscore": rows["pscore"][idx],
    }
    action_dist = np.stack([rows["pi_fact"][idx], rows["pi_rest"][idx]], axis=1)[:, :, None]
    q = np.stack([rows["q_fact"][idx], rows["q_rest"][idx]], axis=1)[:, :, None]
    ns["estimated_rewards_by_reg_model"] = q
    return {name: float(mean) for name, (mean, _) in ns["BLUE"](feedback, action_dist).items()}


def full(args):
    ns = run_notebook(args.obp, args.notebook, args.data, args.campaign)
    feedback = ns["bandit_feedback"]
    result = {
        "rows": int(feedback["n_rounds"]),
        "n_actions": int(feedback["n_actions"]),
        "blue": {name: [float(x) for x in value] for name, value in ns["BLUE_result"].items()},
    }
    rows = compact_rows(ns) | {"block": blocks(ns["dataset"].data["timestamp"])}
    args.dir.mkdir(parents=True, exist_ok=True)
    np.save(args.dir / "target.npy", ns["action_dist"][0])
    np.savez(args.dir / "rows.part.npz", **rows)
    (args.dir / "rows.part.npz").replace(args.dir / "rows.npz")
    (args.dir / "full.json").write_text(json.dumps(result, indent=1) + "\n")


def replicates(args):
    with np.load(args.dir / "rows.npz") as saved:
        rows = dict(saved)
    multiplicities = np.load(args.blocks)
    inputs = {
        "notebook_sha256": sha256(args.notebook),
        "rows_sha256": sha256(args.dir / "rows.npz"),
        "blocks_sha256": sha256(args.blocks),
    }
    record = Record(args.out, inputs)
    ns = blue_function(args.notebook)

    def compute(i):
        idx = block_rows(rows["block"], multiplicities[i])
        return {"i": i, "rows": len(idx)} | compact_call(ns, rows, idx)

    record.check(lambda line: compute(line["i"]))
    done = {line["i"] for line in record.lines}
    for i in range(args.first, min(args.last, len(multiplicities) - 1) + 1):
        if i not in done:
            record.write(compute(i))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("full")
    for name in ("obp", "notebook", "data"):
        p.add_argument(name, type=Path)
    p.add_argument("campaign", choices=("all", "men", "women"))
    p.add_argument("dir", type=Path)
    p = sub.add_parser("replicates")
    for name in ("notebook", "dir", "blocks", "out"):
        p.add_argument(name, type=Path)
    p.add_argument("--first", type=int, default=0)
    p.add_argument("--last", type=int, default=1999)
    p = sub.add_parser("on-policy")
    for name in ("obp", "data"):
        p.add_argument(name, type=Path)
    p.add_argument("campaign", choices=("all", "men", "women"))
    p.add_argument("out", type=Path)
    p = sub.add_parser("environment")
    for name in ("obp", "notebook"):
        p.add_argument(name, type=Path)
    args = parser.parse_args()

    if args.command == "full":
        full(args)
    elif args.command == "replicates":
        replicates(args)
    else:
        sys.path.insert(0, str(args.obp))
        import obp  # noqa: PLC0415
        from obp.dataset import OpenBanditDataset  # noqa: PLC0415

        if args.command == "on-policy":
            value = OpenBanditDataset.calc_on_policy_policy_value_estimate(
                behavior_policy="bts", campaign=args.campaign, data_path=args.data
            )
            args.out.write_text(json.dumps({"v_on": float(value)}) + "\n")
        else:
            print(json.dumps(environment([args.notebook, *package_files(obp)])))


if __name__ == "__main__":
    main()
