import json

import numpy as np
import pytest
from pytest import approx

from obd import run
from obd.tests.synthetic import write_archive

N = 20  # replicates


@pytest.fixture(scope="module")
def data_dir(tmp_path_factory):
    directory = tmp_path_factory.mktemp("obd")
    sizes = {"random": 30_000, "bts": 60_000}
    write_archive(directory, {"all": (6, sizes), "women": (4, sizes)}, np.random.default_rng(3))
    return directory


@pytest.fixture(scope="module")
def analysed(data_dir):
    return {campaign: run.analyse(data_dir, campaign, n_replicates=N) for campaign in run.POOL}


def test_a_campaign_is_analysed_end_to_end(analysed):
    result, replicates = analysed["all"]
    json.dumps(result, default=lambda x: x.item())
    assert result["rows"] == {"random": 30_000, "bts": 60_000}
    assert all(len(draws) == N for draws in replicates.values())
    q = result["quantities"]
    # the recorded propensities of the synthetic BTS log are its true policy
    assert q["h2.m"]["estimate"] == approx(1, abs=0.02)
    assert result["h1"]["label"] == "inconsistent"  # the policy is not the prior
    assert result["h4"]["evaluable"]


def test_pooled_unit_weights_the_campaigns_replicate_by_replicate(analysed):
    results = {campaign: result for campaign, (result, _) in analysed.items()}
    replicates = {campaign: draws for campaign, (_, draws) in analysed.items()}
    pooled = run.pool(results, replicates, n_replicates=N)

    def own(name, campaign):
        key = name if name.startswith("h3") else f"{name}.{results[campaign]['h4']['width']}"
        return results[campaign]["quantities"][key]["estimate"], replicates[campaign][key]

    for name in ("h3.ips", "h3.snips", "h4.rho", "h4.d"):
        (all_, all_draws), (women, women_draws) = own(name, "all"), own(name, "women")
        assert pooled["quantities"][name]["estimate"] == approx(0.54 * all_ + 0.46 * women)
        assert pooled["quantities"][name]["interval"] == approx(
            np.percentile(0.54 * all_draws + 0.46 * women_draws, [2.5, 97.5]).tolist()
        )
        assert pooled["quantities"][name + ".all_minus_women"]["interval"] == approx(
            np.percentile(all_draws - women_draws, [2.5, 97.5]).tolist()
        )
    assert pooled["h4"]["widths"] == {c: results[c]["h4"]["width"] for c in run.POOL}
    assert isinstance(pooled["h3"]["ips"]["campaigns_differ"], bool)


def test_a_campaign_that_stops_is_not_analysed(tmp_path):
    sizes = {"random": 300, "bts": 300}
    write_archive(tmp_path, {"men": (6, sizes)}, np.random.default_rng(3))
    with pytest.raises(SystemExit, match="300 rows, expected 452949"):
        run.run(tmp_path, ["men"])
    assert not list(tmp_path.glob("*.parquet"))


def test_both_confirmatory_campaigns_are_checked_before_either_is_analysed(tmp_path):
    sizes = {"random": 300, "bts": 300}
    write_archive(tmp_path, {"all": (6, sizes), "women": (4, sizes)}, np.random.default_rng(3))
    with pytest.raises(SystemExit, match="bts/women"):
        run.run(tmp_path, ["all"])
    assert not list(tmp_path.glob("*.parquet"))


def test_undefined_replicates_are_left_out_and_counted():
    summary = run.summarise(1.0, np.array([np.nan, np.inf, *np.arange(100.0)]))
    assert summary["undefined_replicates"] == 2
    assert summary["interval"] == approx([2.475, 96.525])


def test_a_quantity_undefined_in_over_one_percent_of_replicates_gets_no_label():
    def label(undefined):
        q = {"x": {"interval": [0.5, 0.9], "undefined_replicates": undefined}}
        return run.labelled(q, 1000, ["x"], run.verdicts.h3)

    assert label(10) == "low"
    assert label(11).startswith("not evaluable")
    assert run.reading("low", label(11), "below the on-policy value") is None
    assert run.reading("low", "raises the estimate", "below the on-policy value") == (
        "gap shrinks; a residual remains"
    )


def test_h2_is_undetermined_with_fewer_than_five_eligible_cells():
    undefined = {"estimate": np.nan, "interval": [np.nan, np.nan], "undefined_replicates": N}
    assert run.h2_label({"h2.m": undefined}, N) == "undetermined"
    cell = {"estimate": 1.0, "interval": [0.9, 1.1], "undefined_replicates": 0}
    q = {"h2.m": cell} | {f"h2.s.{item}.1": cell for item in range(5)}
    assert run.h2_label(q, N) == "consistent"
    assert run.h2_label(dict(list(q.items())[:5]), N) == "undetermined"
