"""The run on a small synthetic archive, and T8 through the run's own labelling."""

import json
import subprocess
import sys

import numpy as np
import pytest

from obd import data
from obd.tests.synthetic import raw_log, uniform
from obd_rescore import logs, references, rules
from obd_rescore import run as registered
from obd_rescore.tests import synthetic
from obd_rescore.tests.conftest import DIR, ITEMS, python

ROWS = {"random": 20_000, "bts": 3000}
SIZES = {"runs": 6, "replication_runs": 4, "replicates": 5, "sample": 1000}


@pytest.fixture
def small(tmp_path, monkeypatch):
    """A work directory with a synthetic archive, sized for a short run."""
    python("mips"), python("blue")
    work = tmp_path / "work"
    (work / "data").mkdir(parents=True)
    for name in ("envs", "src"):
        (work / name).symlink_to(DIR / name)
    synthetic.write(
        work / "data", {c: (n, ROWS) for c, n in ITEMS.items()}, np.random.default_rng(3)
    )
    monkeypatch.setattr(data, "fetch", lambda data_dir: None)
    monkeypatch.setattr(data, "ROWS", {(p, c): n for p, n in ROWS.items() for c in ITEMS})
    monkeypatch.setattr(logs, "SAMPLE", SIZES["sample"])  # 50 blocks per block run
    monkeypatch.setattr(registered, "RESULTS", tmp_path / "results")
    return work


def changed(record, number, **values):
    """The text of a record with the values of one line changed."""
    lines = record.read_text().splitlines()
    lines[number] = json.dumps(json.loads(lines[number]) | values)
    return "\n".join(lines) + "\n"


def test_the_run_computes_the_replications_first_and_resumes(small, monkeypatch):
    seen, replication = {}, registered.replication

    def recorded(r):
        out = replication(r)
        seen["state"] = sorted(str(p.relative_to(r.state)) for p in r.state.rglob("*.*"))
        return out

    monkeypatch.setattr(registered, "replication", recorded)
    first = registered.run(small, SIZES, slots=4, commit="c")
    # the replications need only V_on of All and Men's, the targets of All, the rows
    # arm of All with the published target, and the full data of Men's
    jobs = ["pi_all", "full_men", "replication_0", "replication_2"]
    assert seen["state"] == sorted(
        ["checks.json", "events.jsonl", "tables/bts_all.npz", "tables/bts_men.npz"]
        + ["c1/pi_all.npy", "c1/blocks_all.npy", "c1/replication_0.jsonl", "c1/replication_2.jsonl"]
        + ["c2/men/full.json", "c2/men/rows.npz", "c2/men/target.npy"]
        + [f"logs/{job}.log" for job in jobs]
    )
    results = registered.RESULTS
    replication_c1 = json.loads((results / "replication.json").read_text())["c1"]
    assert replication_c1["comparison"]["runs"] == SIZES["replication_runs"]
    labels = {"holds", "flips", "undecided", "not evaluable", "references differ"}
    for campaign, out in first["c1"].items():
        assert len(out["cells"]) == 4
        for cell in out["cells"].values():
            assert {cell["label_v_on"], cell["label_target"]} <= labels
            assert ("r_snips" in cell["comparisons"]) == (campaign == "men")
    for out in first["c2"].values():
        assert out["unbiasedness"]["replicates"] == SIZES["replicates"]
        assert max(abs(d) for d in out["compact_minus_full"].values()) < 1e-12
    for campaign in ITEMS:
        lines = [json.loads(x) for x in (results / "c1" / campaign).with_suffix(".jsonl").open()]
        assert len(lines) == SIZES["runs"] * 4
        names = ("r_ips", "r_snips") if campaign == "men" else ("r_ips",)
        # each run is scored against the references of its own target
        tables = logs.tables(small / "data", "random", campaign, ITEMS[campaign])
        pis = np.load(small / "run" / "c1" / f"pi_{campaign}.npy")
        values = {
            target: references.values(tables, references.applied(pis, target))
            for target in registered.TARGETS
        }
        for x in lines:
            for name in names:
                assert x[name] == values[x["target"]][name][x["t"]]
        for arm, target in [("rows", "published"), ("blocks", "own")]:
            runs = sorted(
                (x for x in lines if (x["arm"], x["target"]) == (arm, target)), key=lambda x: x["t"]
            )
            cell = first["c1"][campaign]["cells"][f"{arm}/{target}"]
            for name in names:
                again = rules.compare(
                    [x["mips_slope"] for x in runs],
                    [x["ips"] for x in runs],
                    [x[name] for x in runs],
                )
                assert again == cell["comparisons"][name]
        replicates = [
            json.loads(x) for x in (results / "c2" / campaign).with_suffix(".jsonl").open()
        ]
        assert len(replicates) == SIZES["replicates"] and "v_on_i" in replicates[0]
        differences = [x["BLUE"] - x["IPS"] for x in replicates]
        interval = np.percentile(differences, [2.5, 97.5], method="linear").tolist()
        assert first["c2"][campaign]["unbiasedness"]["interval"] == interval
    labels = json.loads((results / "labels.json").read_text())
    primary = first["c1"]["all"]["cells"]["blocks/own"]["label_target"]
    assert labels["primary"]["c1_all_blocks_own_against_the_target"] == primary

    men = small / "run" / "c1" / "men.jsonl"
    men.write_text("".join(men.read_text().splitlines(keepends=True)[:-3]))
    c1 = (results / "c1.json").read_text()
    assert registered.run(small, SIZES, slots=4, commit="c") == first
    assert (results / "c1.json").read_text() == c1
    about = json.loads((results / "provenance.json").read_text())
    assert [x["event"] for x in about["events"]].count("start") == 2
    assert about["study"]["float_parsing"] == logs.float_parsing()

    # a count or a line that the checks before the labels read, changed in the state
    state = small / "run"
    full = state / "c2" / "all" / "full.json"
    replicates = state / "c2" / "men_replicates.jsonl"
    replication = state / "c1" / "replication_0.jsonl"
    for path, text, stop in [
        (full, json.dumps(json.loads(full.read_text()) | {"rows": 7}), "obp read .* of all"),
        (replicates, changed(replicates, 1, rows=7), "rows of men to other blocks"),
        (replication, changed(replication, 1, ips=0.5), "run 0 does not repeat the replication"),
    ]:
        kept = path.read_text()
        path.write_text(text)
        with pytest.raises(SystemExit, match=stop):
            registered.run(small, SIZES, slots=4, commit="c")
        path.write_text(kept)

    target = small / "run" / "c2" / "women" / "target.npy"
    np.save(target, np.load(target) * (1 + 2e-9))
    with pytest.raises(SystemExit, match="differs from BLUE's IPS"):
        registered.run(small, SIZES, slots=4, commit="c")
    np.save(target, np.load(target) * np.nan)
    with pytest.raises(SystemExit, match="differs from BLUE's IPS"):
        registered.run(small, SIZES, slots=4, commit="c")


def test_a_stop_check_ends_the_run_before_any_click_is_read(small, monkeypatch):
    rows = dict(data.ROWS) | {("bts", "women"): ROWS["bts"] + 1}
    monkeypatch.setattr(data, "ROWS", rows)
    with pytest.raises(SystemExit, match="stopped by the checks"):
        registered.run(small, SIZES, slots=4, commit="c")
    state = sorted(p.name for p in (small / "run").rglob("*.*"))
    assert state == ["checks.json", "events.jsonl"]


def test_the_run_refuses_another_numpy(tmp_path, monkeypatch):
    monkeypatch.setattr(np, "__version__", "2.6.0")
    with pytest.raises(SystemExit, match="numpy 2.5"):
        registered.run(tmp_path, SIZES, slots=4, commit="c")
    assert not list(tmp_path.iterdir())


def test_the_run_stops_on_other_commits_and_on_another_prior(small, monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(registered, "COMMITS", registered.COMMITS | {"icml2022-mips": "0" * 40})
        with pytest.raises(SystemExit, match="not at the registered commits"):
            registered.run(small, SIZES, slots=4, commit="c")
    monkeypatch.setattr(data, "PRIOR_SHA256", "0" * 64)
    with pytest.raises(SystemExit, match="the prior of environment mips is not the registered"):
        registered.run(small, SIZES, slots=4, commit="c")
    assert [p.name for p in (small / "run").rglob("*.*")] == ["events.jsonl"]


def test_main_refuses_another_commit_and_records_a_stop(tmp_path, monkeypatch):
    events = tmp_path / "run" / "events.jsonl"
    events.parent.mkdir()
    events.write_text(json.dumps({"event": "start", "commit": "a"}) + "\n")
    monkeypatch.setattr(sys, "argv", ["run", "--work-dir", str(tmp_path)])
    monkeypatch.setattr(registered, "code_commit", lambda: "b")
    with pytest.raises(SystemExit, match="not at b"):
        registered.main()

    def stopped(work_dir, commit):
        raise SystemExit("a reason")

    monkeypatch.setattr(registered, "code_commit", lambda: "a")
    monkeypatch.setattr(registered, "run", stopped)
    with pytest.raises(SystemExit, match="a reason"):
        registered.main()
    last = json.loads(events.read_text().splitlines()[-1])
    assert (last["event"], last["reason"]) == ("stopped", "a reason")


def test_the_run_refuses_code_that_differs_from_its_commit(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", tmp_path], check=True)
    monkeypatch.setattr(registered, "RESULTS", tmp_path / "obd_rescore" / "results")
    (tmp_path / "obd_rescore").mkdir()
    (tmp_path / "obd_rescore" / "run.py").write_text("")
    with pytest.raises(SystemExit, match="differs from its commit"):
        registered.code_commit()


def test_t8_an_estimator_moved_towards_v_on_holds_against_it_and_flips_against_the_target():
    rng = np.random.default_rng(8)
    n_items = 10
    click_rate = rng.uniform(0.02, 0.06, n_items)
    log = raw_log(rng, 30_000, uniform(n_items), click_rate)
    pi = rng.dirichlet(np.ones(n_items), 3).T  # pi[a, k]
    value = (pi * click_rate[:, None]).sum() / 3  # the target's value on this log
    w = pi[log["item_id"], log["position"] - 1] / log["propensity_score"]
    contribution = (log["click"] * w).to_numpy()
    r_ips = contribution.mean()
    assert r_ips == pytest.approx(value, rel=0.05)
    v_on = 1.5 * value  # the on-policy value, set apart from the target's
    ips = np.array([contribution[rng.integers(0, len(log), 3000)].mean() for _ in range(500)])
    moved = ips + 0.5 * (v_on - r_ips)
    moved[0], moved[1] = np.nan, ips[1]  # removed, and a tie
    refs = {"v_on": v_on, "r_ips": r_ips}

    cell = registered.c1_cell({"ips": ips, "mips": moved, "mips_slope": moved}, refs, v_on, False)
    assert (cell["label_v_on"], cell["label_target"]) == ("holds", "flips")
    for comparison in cell["comparisons"].values():
        assert (comparison["removed"], comparison["ties"] >= 1) == (1, True)

    draws = {"BLUE": moved} | dict.fromkeys(registered.OTHERS, ips)
    labels = registered.c2_labels(draws, refs | {"r_snips": r_ips}, men=True)
    assert (labels["label_v_on"], labels["label_target"]) == ("holds", "flips")
