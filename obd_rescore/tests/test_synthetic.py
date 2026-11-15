import zipfile

import pandas as pd

from obd import data
from obd_rescore.tests.conftest import ITEMS, POLICIES


def test_the_archive_passes_the_stop_checks(archive, monkeypatch):
    monkeypatch.setattr(
        data, "ROWS", {(p, c): n for p, n in [("random", 3000), ("bts", 1500)] for c in ITEMS}
    )
    report = data.check(archive, list(ITEMS))
    assert [r["stops"] for r in report.values()] == [[]] * 6


def test_logs_and_item_contexts_have_the_released_columns(archive):
    with zipfile.ZipFile(archive / data.ARCHIVE) as z:
        for campaign, n_items in ITEMS.items():
            for policy in POLICIES:
                folder = f"open_bandit_dataset/{policy}/{campaign}/"
                with z.open(folder + f"{campaign}.csv") as f:
                    header = f.readline().decode().rstrip("\n").split(",")
                assert header == [
                    "",
                    "timestamp",
                    "item_id",
                    "position",
                    "click",
                    "propensity_score",
                    *data.FEATURES,
                    *(f"user-item_affinity_{i}" for i in range(n_items)),
                ]
                with z.open(folder + "item_context.csv") as f:
                    context = pd.read_csv(f, index_col=0)
                assert context.columns.tolist() == ["item_id"] + [
                    f"item_feature_{i}" for i in range(4)
                ]
                assert context["item_id"].tolist() == list(range(n_items))
