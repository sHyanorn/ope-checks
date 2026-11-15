"""The adapter of C2 on synthetic logs: T3, T4, T6 and T7."""

import json

import numpy as np
import pytest

from obd_rescore import envs, logs, references
from obd_rescore.tests import synthetic
from obd_rescore.tests.conftest import ITEMS, POLICIES, SOURCES, adapter, run
from obd_rescore.tests.test_logs import frame

# enough clicks at each position for the reward model's five folds
ROWS = {"random": 20_000, "bts": 3000}
CAMPAIGNS = ("men", "women")  # each run of the notebook draws its target a million times


@pytest.fixture(scope="module")
def data(tmp_path_factory):
    """An archive, the files obp reads, and the output of `full` for each campaign."""
    path = tmp_path_factory.mktemp("blue")
    synthetic.write(path, {c: (ITEMS[c], ROWS) for c in CAMPAIGNS}, np.random.default_rng(2))
    extracted = logs.extract(path, path, [(p, c) for p in POLICIES for c in CAMPAIGNS])
    for campaign in CAMPAIGNS:
        args = [SOURCES["blue"], SOURCES["notebook"], extracted, campaign, path / campaign]
        adapter("blue", "full", *args)
    return path, extracted


def full(data, campaign):
    return json.loads((data[0] / campaign / "full.json").read_text())


NOTEBOOK = """
import json, sys
sys.path.insert(0, sys.argv[1])
from IPython.core.interactiveshell import InteractiveShell
shell = InteractiveShell.instance()
for i, cell in enumerate(json.load(open(sys.argv[2]))["cells"][:46]):
    source = "".join(cell["source"])
    if cell["cell_type"] == "code":
        source = f"campaign = {sys.argv[3]!r}" if i == 3 else source
        shell.run_cell(source, silent=True).raise_error()
result = shell.user_ns["BLUE_result"]
print(json.dumps({name: float(mean) for name, (mean, _) in result.items()}))
"""


def test_t3_the_adapter_gives_the_notebook_run_in_order(data, tmp_path):
    (tmp_path / "obd").symlink_to(data[1])  # the notebook reads ./obd/
    args = [SOURCES["blue"], SOURCES["notebook"], "men"]
    notebook = json.loads(run("blue", NOTEBOOK, *args, cwd=tmp_path).splitlines()[-1])
    ours = full(data, "men")
    assert ours["rows"] == ROWS["random"]
    assert sorted(ours["blue"]) == sorted(notebook)
    for name, value in notebook.items():
        np.testing.assert_allclose(ours["blue"][name][0], value, rtol=1e-9)


COMPACT = """
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import blue
ns = blue.run_notebook(*sys.argv[2:6])
fn = blue.blue_function(sys.argv[3])
feedback, q, dist = ns["bandit_feedback"], ns["estimated_rewards_by_reg_model"], ns["action_dist"]
block = blue.blocks(ns["dataset"].data["timestamp"])
degenerate = dist[0].copy()
degenerate[:, 0] = 0
degenerate[feedback["action"][0], 0] = 1  # its item holds all of the first position
out = []
for target in (dist[0], degenerate):
    ns["action_dist"] = np.broadcast_to(target, dist.shape)
    rows = blue.compact_rows(ns)
    for m in [np.ones(1008, int), *np.load(sys.argv[6])]:
        idx = blue.block_rows(block, m)
        fn["estimated_rewards_by_reg_model"] = q[idx]
        whole = {k: v[0] for k, v in fn["BLUE"](
            {k: feedback[k][idx] for k in ("action", "position", "reward", "pscore")},
            ns["action_dist"][idx]).items()}
        out.append({"full": whole, "compact": blue.compact_call(fn, rows, idx),
                    "rest_zero": int((rows["pi_rest"][idx] == 0).sum())})
print(json.dumps(out, default=float))
"""


def test_t4_compact_and_full_inputs_give_the_same_estimates(data, tmp_path):
    blocks = tmp_path / "blocks.npy"
    np.save(blocks, [logs.c2_multiplicities(i) for i in range(2)])
    args = [envs.ADAPTERS, SOURCES["blue"], SOURCES["notebook"], data[1], "men", blocks]
    calls = json.loads(run("blue", COMPACT, *args).splitlines()[-1])
    assert len(calls) == 6
    assert [c["rest_zero"] > 0 for c in calls] == [False] * 3 + [True] * 3
    for call in calls:
        assert sorted(call["full"]) == sorted(call["compact"])
        for name, value in call["full"].items():
            np.testing.assert_allclose(call["compact"][name], value, rtol=1e-9)


def test_t6_t7_replicates_hold_the_drawn_blocks_and_ips_is_the_reference(data, tmp_path):
    path, _ = data
    log = frame(path, "random", "women")
    target = np.load(path / "women" / "target.npy")
    blocks = tmp_path / "blocks.npy"
    np.save(blocks, [np.ones(1008, int), *(logs.c2_multiplicities(i) for i in range(2))])
    out = tmp_path / "replicates.jsonl"
    adapter("blue", "replicates", SOURCES["notebook"], path / "women", blocks, out)
    lines = [json.loads(line) for line in out.read_text().splitlines()[1:]]
    assert [line["i"] for line in lines] == [0, 1, 2]
    block = logs.blocks(log["timestamp"])
    for line, m in zip(lines, np.load(blocks), strict=True):
        drawn = log.iloc[np.repeat(np.arange(len(log)), m[block])]
        w = target[drawn["item_id"], drawn["position"] - 1] / drawn["propensity_score"]
        assert line["rows"] == len(drawn)
        np.testing.assert_allclose(line["IPS"], (drawn["click"] * w).mean(), rtol=1e-12)
        np.testing.assert_allclose(line["SNIPS"], (drawn["click"] * w).sum() / w.sum(), rtol=1e-12)

    tables = logs.tables(path, "random", "women", ITEMS["women"])
    ours = references.values(tables, target)
    published = full(data, "women")["blue"]
    np.testing.assert_allclose(ours["r_ips"], published["IPS"][0], rtol=1e-12)
    np.testing.assert_allclose(ours["r_snips"], published["SNIPS"][0], rtol=1e-12)
    np.testing.assert_allclose(lines[0]["IPS"], published["IPS"][0], rtol=1e-12)
