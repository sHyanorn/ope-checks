"""The adapter of C1 on synthetic logs: T1, T2, T6, T7 and resumed runs."""

import json

import numpy as np
import pandas as pd
import pytest

from obd_rescore import envs, logs, references
from obd_rescore.tests import synthetic
from obd_rescore.tests.conftest import ITEMS, SOURCES, adapter, call, python, run
from obd_rescore.tests.test_logs import ON_POLICY, frame

N_RUNS = 3
SAMPLE = 1000
T1_ROWS, T1_SAMPLE = 20_000, 5000  # enough clicks for the reward model of the published loop


@pytest.fixture(scope="module")
def inputs(tmp_path_factory):
    """The targets of the first runs, drawn by the adapter, and the multiplicities of
    the block arm, drawn on this study's side."""
    path = tmp_path_factory.mktemp("mips")
    files = {}
    for campaign in ITEMS:
        pi, blocks = path / f"pi_{campaign}.npy", path / f"blocks_{campaign}.npy"
        adapter("mips", "targets", SOURCES["mips"], campaign, pi, "--runs", N_RUNS)
        np.save(blocks, [logs.c1_multiplicities(campaign, t) for t in range(N_RUNS)])
        files[campaign] = pi, blocks
    return files


def runs(extracted, inputs, campaign, out, *options):
    adapter("mips", "runs", SOURCES["mips"], extracted, campaign, *inputs[campaign], out, *options)
    return [json.loads(line) for line in out.read_text().splitlines()]


def test_t1_the_row_arm_repeats_the_published_loop_bit_for_bit(tmp_path, inputs):
    archive = tmp_path / "obd"
    archive.mkdir()
    rows = {"random": T1_ROWS, "bts": 3000}
    synthetic.write(archive, {"all": (ITEMS["all"], rows)}, np.random.default_rng(1))
    launch = tmp_path / "launch"
    logs.extract(archive, launch / "real", [("random", "all"), ("bts", "all")])
    main = SOURCES["mips"] / "main.py"
    settings = [f"setting.n_seeds={N_RUNS}", f"setting.sample_size={T1_SAMPLE}"]
    call([python("mips"), main, *settings], launch)
    result = launch / "real" / "logs" / f"sample_size={T1_SAMPLE}" / "all" / "df" / "result_df.csv"
    published = pd.read_csv(result, index_col=0, float_precision="round_trip")
    # run-major; the stack of the loop drops estimators whose error is not finite
    published["t"] = (published["est"] == "IPS").cumsum() - 1
    assert published["t"].max() == N_RUNS - 1

    data = launch / "real" / logs.ROOT
    options = ["--arms", "rows", "--targets", "published", "--last", N_RUNS - 1]
    header, *lines = runs(
        data, inputs, "all", tmp_path / "runs.jsonl", *options, "--sample", T1_SAMPLE
    )
    assert header["inputs"]["n_actions"] == 240
    v_on = np.float64(run("mips", ON_POLICY, "all", data))
    assert [line["t"] for line in lines] == list(range(N_RUNS))
    for line in lines:
        se = published[published["t"] == line["t"]].set_index("est")["se"]
        assert (np.float64(line["ips"]) - v_on) ** 2 == se["IPS"]
        assert (v_on - np.float64(line["mips"])) ** 2 == se["MIPS (w/o SLOPE)"]
        assert (v_on - np.float64(line["mips_slope"])) ** 2 == se["MIPS (w/ SLOPE)"]


WEIGHTS = """
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import mips
from obp.ope import InverseProbabilityWeighting

pi = np.array(json.loads(sys.argv[2]))
n_items = len(pi)
a, k = (x.ravel() for x in np.meshgrid(np.arange(n_items), np.arange(3), indexing="ij"))
action = k * n_items + a  # as pre_process numbers the logged action
n = len(action)
out = {}
for target in ("published", "own"):
    pi_e, _ = mips.layouts(pi, n, target)
    out[target] = InverseProbabilityWeighting()._estimate_round_rewards(
        reward=np.ones(n), action=action, position=np.zeros(n, int),
        pscore=np.full(n, 1 / n_items) / 3, action_dist=pi_e).tolist()
print(json.dumps(out))
"""


@pytest.mark.parametrize("n_items", ITEMS.values())
def test_t2_ips_weights_each_pair_by_its_layout(n_items):
    pi = np.random.default_rng(n_items).dirichlet(np.ones(n_items), 3).T
    weights = json.loads(run("mips", WEIGHTS, envs.ADAPTERS, json.dumps(pi.tolist())))
    a, k = (x.ravel() for x in np.meshgrid(np.arange(n_items), np.arange(3), indexing="ij"))
    j = k * n_items + a
    expected = {"published": n_items * pi[j // 3, j % 3], "own": n_items * pi[a, k]}
    for target in ("published", "own"):
        np.testing.assert_allclose(weights[target], expected[target], rtol=1e-12)
    same = np.isclose(weights["published"], weights["own"], rtol=1e-12)
    assert sorted(zip(a[same], k[same], strict=True)) == [(0, 0), (n_items - 1, 2)]


PUBLISHED_MIPS = """
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import mips
published, ope = mips.published_code(sys.argv[2])
dataset = published.ModifiedOpenBanditDataset(
    behavior_policy="random", data_path=sys.argv[3], campaign=sys.argv[4])
feedback = dataset.obtain_batch_bandit_feedback()
pi = np.load(sys.argv[5])[0]
n, n_items = feedback["n_rounds"], len(pi)
j = np.arange(3 * n_items)  # the logged action of item a at position k is k n_A + a
layout = {"published": pi[j // 3, j % 3], "own": pi[j % n_items, j // n_items]}
uniform = np.full((n, 3 * n_items, 1), 1 / n_items / 3)
out = {}
for target, pi_star in layout.items():
    direct = {name: float(ope.MIPS().estimate_policy_value(
        context=feedback["context"], reward=feedback["reward"], action=feedback["action"],
        action_emb=feedback["action_context"], action_dist_b=uniform,
        action_dist_e=np.tile(pi_star[:, None] / 3, (n, 1, 1)),
        n_actions=feedback["n_actions"], feature_pruning=pruning))
        for name, pruning in [("mips", "no"), ("mips_slope", "exact")]}
    adapter = mips.estimates(ope, feedback, pi, target, list(direct))
    out[target] = {"adapter": adapter, "direct": direct}
print(json.dumps(out))
"""


@pytest.mark.parametrize("campaign", ITEMS)
def test_t2_the_published_mips_is_given_the_layout_of_each_target(campaign, extracted, inputs):
    args = [envs.ADAPTERS, SOURCES["mips"], extracted, campaign, inputs[campaign][0]]
    out = json.loads(run("mips", PUBLISHED_MIPS, *args))
    for target in ("published", "own"):
        assert out[target]["adapter"] == out[target]["direct"]
    for name in ("mips", "mips_slope"):  # the two layouts are told apart
        assert out["published"]["direct"][name] != out["own"]["direct"][name]


BLOCKS = """
import json, sys
import numpy as np
import pandas as pd
sys.path.insert(0, sys.argv[1])
import mips
published, ope = mips.published_code(sys.argv[2])
dataset = published.ModifiedOpenBanditDataset(
    behavior_policy="random", data_path=sys.argv[3], campaign="all")
timestamps = dataset.data["timestamp"]
m = np.array(json.loads(sys.argv[4]))
edges = mips.blocks(pd.Series(json.loads(sys.argv[5])))
try:
    mips.blocks(pd.Series(["2019-12-01 00:00:00.000000+00:00"]))
    outside = None
except SystemExit as stop:
    outside = str(stop)
print(json.dumps({
    "timestamps": timestamps.tolist(),
    "block": mips.blocks(timestamps).tolist(),
    "rows": mips.block_rows(mips.blocks(timestamps), m).tolist(),
    "edges": edges.tolist(),
    "outside": outside,
}))
"""
EDGES = [
    "2019-11-24 00:00:00.000000+00:00",
    "2019-11-24 00:09:59.999999+00:00",
    "2019-11-24 00:10:00.000000+00:00",
    "2019-11-24 09:10:00.000000+09:00",
    "2019-11-24 00:20:00+00:00",  # a whole second, written without its fraction
    "2019-11-30 23:59:59.999999+00:00",
]


def test_t6_a_block_run_holds_each_row_as_often_as_its_block_is_drawn(extracted):
    m = logs.c1_multiplicities("all", 0)
    args = [envs.ADAPTERS, SOURCES["mips"], extracted, json.dumps(m.tolist()), json.dumps(EDGES)]
    out = json.loads(run("mips", BLOCKS, *args))
    block = np.array(out["block"])
    assert (block == logs.blocks(pd.Series(out["timestamps"]))).all()
    assert out["edges"] == [0, 0, 1, 1, 2, 1007]
    assert out["outside"] == "a row lies outside the week"
    rows = np.array(out["rows"])
    assert (np.diff(rows) >= 0).all()  # in place, in obp's order
    assert (np.bincount(rows, minlength=len(block)) == m[block]).all()


def test_t6_the_block_arm_uses_the_multiplicities_drawn_here(tmp_path, archive, extracted, inputs):
    options = ["--arms", "blocks", "--targets", "own", "--estimators", "ips", "--last", N_RUNS - 1]
    _, *lines = runs(extracted, inputs, "all", tmp_path / "blocks.jsonl", *options)
    log = frame(archive, "random", "all")
    block = logs.blocks(log["timestamp"])
    pis = np.load(inputs["all"][0])
    for line in lines:
        m = logs.c1_multiplicities("all", line["t"])
        drawn = log.iloc[np.repeat(np.arange(len(log)), m[block])]
        pi_star = pis[line["t"]][drawn["item_id"], drawn["position"] - 1]
        ips = (drawn["click"] * pi_star / drawn["propensity_score"]).mean()
        assert line["rows"] == len(drawn)
        np.testing.assert_allclose(line["ips"], ips, rtol=1e-12)


WHOLE_LOG = """
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import mips
from obp.ope import SelfNormalizedInverseProbabilityWeighting
published, ope = mips.published_code(sys.argv[2])
dataset = published.ModifiedOpenBanditDataset(
    behavior_policy="random", data_path=sys.argv[3], campaign=sys.argv[4])
feedback = dataset.obtain_batch_bandit_feedback()
pi = np.load(sys.argv[5])[0]
out = {}
for target in ("published", "own"):
    pi_e, _ = mips.layouts(pi, feedback["n_rounds"], target)
    snips = SelfNormalizedInverseProbabilityWeighting().estimate_policy_value(
        reward=feedback["reward"], action=feedback["action"],
        position=feedback["position"], pscore=feedback["pscore"], action_dist=pi_e)
    ips = mips.estimates(ope, feedback, pi, target, ["ips"])["ips"]
    out[target] = {"r_ips": ips, "r_snips": float(snips)}
print(json.dumps(out))
"""


@pytest.mark.parametrize("campaign", ITEMS)
def test_t7_the_references_are_the_adapter_on_the_whole_random_log(
    campaign, archive, extracted, inputs
):
    pi = inputs[campaign][0]
    args = [envs.ADAPTERS, SOURCES["mips"], extracted, campaign, pi]
    adapter_values = json.loads(run("mips", WHOLE_LOG, *args))
    tables = logs.tables(archive, "random", campaign, ITEMS[campaign])
    for target, values in adapter_values.items():
        ours = references.values(tables, references.applied(np.load(pi)[0], target))
        # the sums run in another order: equal up to rounding
        for name, value in values.items():
            np.testing.assert_allclose(ours[name], value, rtol=1e-12)


def test_a_resumed_process_repeats_its_last_line_and_continues(tmp_path, extracted, inputs):
    options = ["--arms", "rows", "--targets", "own", "--estimators", "ips", "--sample", SAMPLE]
    whole = runs(extracted, inputs, "men", tmp_path / "whole.jsonl", *options, "--last", 2)
    part = tmp_path / "part.jsonl"
    runs(extracted, inputs, "men", part, *options, "--last", 0)
    part.write_text(part.read_text() + '{"t": 1, "arm"')  # a line cut off by a stop
    assert runs(extracted, inputs, "men", part, *options, "--last", 2) == whole

    lines = part.read_text().splitlines()
    last = json.loads(lines[-1]) | {"ips": 0.5}
    part.write_text("\n".join([*lines[:-1], json.dumps(last)]) + "\n")
    with pytest.raises(AssertionError, match="does not repeat its last line"):
        runs(extracted, inputs, "men", part, *options, "--last", 2)
    with pytest.raises(AssertionError, match="written under other inputs"):
        runs(extracted, inputs, "men", tmp_path / "whole.jsonl", *options[:-1], 999, "--last", 2)
