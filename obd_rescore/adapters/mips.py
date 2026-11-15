"""The adapter of C1, run in environment mips (Section 5 of the registration).

    python -I mips.py targets SRC CAMPAIGN OUT.npy [--runs N]
    python -I mips.py runs SRC DATA CAMPAIGN PI.npy BLOCKS.npy OUT.jsonl
        [--arms rows blocks] [--targets published own] [--estimators ips mips mips_slope]
        [--first T] [--last T] [--sample N]
    python -I mips.py environment SRC

SRC is src/real of usaito/icml2022-mips; DATA the open_bandit_dataset directory that
obp reads; PI the action distributions written by `targets`; BLOCKS the multiplicities
of the block arm, one row of 1008 per run.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import obp
import pandas as pd
from obp.ope import InverseProbabilityWeighting
from obp.policy import BernoulliTS, Random

sys.path.insert(0, str(Path(__file__).parent))
from common import Record, environment, package_files, sha256  # noqa: E402

N_ITEMS = {"all": 80, "men": 34, "women": 46}
KEYS = ["action", "position", "reward", "pscore", "context", "action_context"]
WEEK_START_NS = 1_574_553_600_000_000_000  # 2019-11-24T00:00:00Z
BLOCK_NS = 600_000_000_000
N_BLOCKS = 1008


def published_code(src):
    sys.path.insert(0, str(src))
    import main  # noqa: PLC0415
    import ope  # noqa: PLC0415

    return main, ope


def targets(campaign, n_runs):
    """pi_t[a, k] of runs 0 to n_runs - 1, drawn in order from one policy (Section 7.1)."""
    policy = BernoulliTS(
        n_actions=N_ITEMS[campaign],
        len_list=3,
        random_state=12345,
        is_zozotown_prior=True,
        campaign=campaign,
    )
    return np.array([policy.compute_batch_action_dist(n_rounds=1)[0] for _ in range(n_runs)])


def blocks(timestamps):
    """The ten-minute block of each timestamp (strings of obp's data, in its order)."""
    t = pd.to_datetime(timestamps, utc=True).values.astype("int64")
    block = (t - WEEK_START_NS) // BLOCK_NS
    if not ((block >= 0) & (block < N_BLOCKS)).all():
        raise SystemExit("a row lies outside the week")
    return block


def block_rows(block, m):
    """Each row repeated in place as often as its block is drawn (departure 5)."""
    return np.repeat(np.arange(len(block)), m[block])


def block_sample(dataset, block, m):
    """The run's data from the rows of the drawn blocks, as obp builds a bootstrap sample."""
    feedback = dataset.obtain_batch_bandit_feedback()
    rows = block_rows(block, m)
    for key in KEYS:
        feedback[key] = feedback[key][rows]
    feedback["n_rounds"] = len(rows)
    return feedback


def layouts(pi, n, target):
    """pi_e and pi_b as the loop of main builds them; own pairs transposed first (departure 3)."""
    n_items = pi.shape[0]
    dist = np.tile(pi, (n, 1, 1))
    if target == "own":
        dist = dist.transpose(0, 2, 1)  # index k n_A + a holds pi(a|k)
    pi_e = dist.reshape(n, 3 * n_items, 1) / 3
    uniform = Random(n_actions=n_items, len_list=3, random_state=12345)
    pi_b = uniform.compute_batch_action_dist(n_rounds=n).reshape(n, 3 * n_items, 1) / 3
    return pi_e, pi_b


def estimates(ope, feedback, pi, target, names):
    """IPS, MIPS (w/o SLOPE) and MIPS (w/ SLOPE) as `run_ope` computes them."""
    pi_e, pi_b = layouts(pi, feedback["n_rounds"], target)
    out = {}
    if "ips" in names:
        out["ips"] = InverseProbabilityWeighting(estimator_name="IPS").estimate_policy_value(
            reward=feedback["reward"],
            action=feedback["action"],
            position=feedback["position"],
            pscore=feedback["pscore"],
            action_dist=pi_e,
        )
    for name, pruning in [("mips", "no"), ("mips_slope", "exact")]:
        if name in names:
            out[name] = ope.MIPS().estimate_policy_value(
                context=feedback["context"],
                reward=feedback["reward"],
                action=feedback["action"],
                action_emb=feedback["action_context"],
                action_dist_b=pi_b,
                action_dist_e=pi_e,
                n_actions=feedback["n_actions"],
                feature_pruning=pruning,
            )
    return {name: float(value) for name, value in out.items()}


def runs(args):
    published, ope = published_code(args.src)
    pis, multiplicities = np.load(args.pi), np.load(args.blocks)
    dataset = published.ModifiedOpenBanditDataset(
        behavior_policy="random", data_path=Path(args.data), campaign=args.campaign
    )
    block = blocks(dataset.data["timestamp"])
    inputs = {k: v for k, v in vars(args).items() if k not in ("command", "out", "first", "last")}
    inputs = {k: str(v) if isinstance(v, Path) else v for k, v in inputs.items()} | {
        "pi_sha256": sha256(args.pi),
        "blocks_sha256": sha256(args.blocks),
        "log_rows": int(dataset.n_rounds),
        "n_actions": int(dataset.n_actions),
    }
    record = Record(args.out, inputs)

    def sample(t, arm):
        if arm == "rows":
            return dataset.sample_bootstrap_bandit_feedback(sample_size=args.sample, random_state=t)
        return block_sample(dataset, block, multiplicities[t])

    def compute(line):
        feedback = sample(line["t"], line["arm"])
        values = estimates(ope, feedback, pis[line["t"]], line["target"], args.estimators)
        keys = {k: line[k] for k in ("t", "arm", "target")}
        return keys | {"rows": int(feedback["n_rounds"])} | values

    record.check(compute)
    done = {(line["t"], line["arm"], line["target"]) for line in record.lines}
    for t in range(args.first, args.last + 1):
        for arm in args.arms:
            if all((t, arm, target) in done for target in args.targets):
                continue
            feedback = sample(t, arm)
            for target in args.targets:
                if (t, arm, target) not in done:
                    values = estimates(ope, feedback, pis[t], target, args.estimators)
                    keys = {"t": t, "arm": arm, "target": target}
                    record.write(keys | {"rows": int(feedback["n_rounds"])} | values)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("targets")
    p.add_argument("src", type=Path)
    p.add_argument("campaign", choices=N_ITEMS)
    p.add_argument("out", type=Path)
    p.add_argument("--runs", type=int, default=500)
    p = sub.add_parser("runs")
    for name in ("src", "data"):
        p.add_argument(name, type=Path)
    p.add_argument("campaign", choices=N_ITEMS)
    for name in ("pi", "blocks", "out"):
        p.add_argument(name, type=Path)
    p.add_argument("--arms", nargs="+", default=["rows", "blocks"])
    p.add_argument("--targets", nargs="+", default=["published", "own"])
    p.add_argument("--estimators", nargs="+", default=["ips", "mips", "mips_slope"])
    p.add_argument("--first", type=int, default=0)
    p.add_argument("--last", type=int, default=499)
    p.add_argument("--sample", type=int, default=100_000)
    p = sub.add_parser("environment")
    p.add_argument("src", type=Path)
    args = parser.parse_args()

    if args.command == "targets":
        part = args.out.with_suffix(".part.npy")
        np.save(part, targets(args.campaign, args.runs))
        part.replace(args.out)
    elif args.command == "runs":
        runs(args)
    else:
        published, ope = published_code(args.src)
        files = [Path(published.__file__), Path(ope.__file__), *package_files(obp)]
        print(json.dumps(environment(files)))


if __name__ == "__main__":
    main()
