"""Synthetic archives in the layout of the released one. No real data."""

import zipfile

import numpy as np
import pandas as pd

from obd import data
from obd.tests import synthetic

CATEGORIES = (5, 12, 30)  # values of item_feature_1 to item_feature_3


def item_context(rng, n_items):
    """An item context file: a price and three hashed categorical features."""
    columns = {
        "item_id": np.arange(n_items),
        "item_feature_0": rng.uniform(-1, 1, n_items).round(6),
    }
    for i, n in enumerate(CATEGORIES, 1):
        columns[f"item_feature_{i}"] = [f"{v:032x}" for v in rng.integers(0, n, n_items)]
    return pd.DataFrame(columns)


def write(data_dir, campaigns, rng):
    """An archive and a prior file as `obd.data` and obp read them.

    `campaigns` maps a campaign to its number of items and its rows by policy,
    as in `obd.tests.synthetic.write_archive`; each log directory also gets the
    item context file of its campaign.
    """
    synthetic.write_archive(data_dir, campaigns, rng)
    with zipfile.ZipFile(data_dir / data.ARCHIVE, "a", zipfile.ZIP_DEFLATED) as z:
        for campaign, (n_items, rows) in campaigns.items():
            text = item_context(rng, n_items).to_csv()
            for policy in rows:
                z.writestr(f"open_bandit_dataset/{policy}/{campaign}/item_context.csv", text)
