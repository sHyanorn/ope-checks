"""The logs on this study's side; T5, and T6 on this side."""

import functools
import zipfile

import numpy as np
import pandas as pd
import pytest

from obd import data
from obd_rescore import logs
from obd_rescore.tests.conftest import ITEMS, POLICIES, SOURCES, run


def frame(archive, policy, campaign):
    with (
        zipfile.ZipFile(archive / data.ARCHIVE) as z,
        z.open(logs.member(policy, campaign)) as f,
    ):
        return pd.read_csv(f, index_col=0, float_precision="round_trip")


def test_each_row_is_summed_into_its_block_item_and_position(archive):
    for policy in POLICIES:
        log = frame(archive, policy, "men")
        since = pd.to_datetime(log["timestamp"], utc=True) - pd.Timestamp("2019-11-24", tz="UTC")
        cell = ((since // pd.Timedelta(minutes=10)).to_numpy(), log["item_id"], log["position"] - 1)
        click, w = log["click"].to_numpy(), 1 / log["propensity_score"].to_numpy()
        tables = logs.tables(archive, policy, "men", ITEMS["men"])
        expected = {"rows": 1, "clicks": click, "click_w": click * w, "w": w}
        for name, table in tables.items():
            sums = np.zeros((data.N_BLOCKS, ITEMS["men"], 3))
            np.add.at(sums, cell, expected[name])
            np.testing.assert_allclose(table, sums, rtol=1e-12, atol=0)
        names = ["rows", "clicks"] + (["click_w", "w"] if policy == "random" else [])
        assert sorted(tables) == sorted(names)


def test_tables_add_up_across_chunks(archive, monkeypatch):
    whole = logs.tables(archive, "random", "all", ITEMS["all"])
    monkeypatch.setattr(logs, "chunks", functools.partial(logs.chunks, chunksize=700))
    parts = logs.tables(archive, "random", "all", ITEMS["all"])
    for name, table in whole.items():
        np.testing.assert_allclose(parts[name], table, rtol=1e-12, atol=0)


def test_blocks_are_utc_ten_minute_intervals_of_the_week():
    stamps = [
        "2019-11-24 00:00:00.000000+00:00",
        "2019-11-24 00:09:59.999999+00:00",
        "2019-11-24 00:10:00.000000+00:00",
        "2019-11-24 09:10:00.000000+09:00",
        "2019-11-30 23:59:59.999999+00:00",
    ]
    assert logs.blocks(pd.Series(stamps)).tolist() == [0, 0, 1, 1, 1007]
    for outside in ["2019-11-23 23:59:59.999999+00:00", "2019-12-01 00:00:00.000000+00:00"]:
        with pytest.raises(SystemExit):
            logs.blocks(pd.Series([outside]))


def test_the_block_arm_draws_the_registered_blocks():
    assert [logs.blocks_per_run(c) for c in data.CAMPAIGNS] == [73, 223, 117]
    m = logs.c1_multiplicities("women", 7)
    rng = np.random.default_rng([20261115, 0, 2, 7])
    assert m.tolist() == rng.multinomial(117, np.full(1008, 1 / 1008)).tolist()
    m = logs.c2_multiplicities(5)
    rng = np.random.default_rng([20261110, 0, 5])
    assert m.tolist() == rng.multinomial(1008, np.full(1008, 1 / 1008)).tolist()


ON_POLICY = """
import sys
from pathlib import Path
sys.path[:0] = sys.argv[3:]  # the obp of env blue
from obp.dataset import OpenBanditDataset
print(repr(OpenBanditDataset.calc_on_policy_policy_value_estimate(
    behavior_policy="bts", campaign=sys.argv[1], data_path=Path(sys.argv[2]))))
"""


@pytest.mark.parametrize("env", ["mips", "blue"])
def test_t5_v_on_equals_obp_bit_for_bit(env, archive, extracted):
    for campaign, n_items in ITEMS.items():
        ours = logs.on_policy_value(logs.tables(archive, "bts", campaign, n_items))
        path = [SOURCES["blue"]] if env == "blue" else []
        theirs = float(run(env, ON_POLICY, campaign, extracted, *path))
        assert ours == theirs
