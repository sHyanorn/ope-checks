"""Open Bandit Dataset: download, checksums, the stop checks of Section 2, Parquet."""

import hashlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yaml

ARCHIVE = "open_bandit_dataset.zip"
ARCHIVE_URL = "https://research.zozo.com/data_release/" + ARCHIVE
ARCHIVE_SHA256 = "e8ec18196582a5937381a1776382ca940689b90a18d2dcd1fb635be6df614d78"
PRIOR = "prior_bts.yaml"
PRIOR_URL = (
    "https://raw.githubusercontent.com/st-tech/zr-obp/"
    "8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4/obp/policy/conf/" + PRIOR
)
PRIOR_SHA256 = "81a54fbdc184021ccc62ab97de81ec35461c032e3d7f99ccaa0a9745f732d251"
DEFAULT_DIR = Path.home() / ".cache" / "ope-checks" / "obd"

CAMPAIGNS = ("all", "men", "women")  # the index is the stream id of Section 5
ROWS = {
    ("random", "all"): 1_374_327,
    ("random", "men"): 452_949,
    ("random", "women"): 864_585,
    ("bts", "all"): 12_357_200,
    ("bts", "men"): 4_077_727,
    ("bts", "women"): 7_765_497,
}
FEATURES = [f"user_feature_{i}" for i in range(4)]
CHECK_COLUMNS = ["timestamp", "item_id", "position", "propensity_score"]  # no clicks
COLUMNS = [*CHECK_COLUMNS, "click", *FEATURES]

WEEK_START_US = 1_574_553_600_000_000  # 2019-11-24T00:00:00Z
BLOCK_US = 600_000_000  # ten minutes
N_BLOCKS = 1008


def fetch(data_dir):
    """Download the archive and the prior unless present, and verify both."""
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, url, sha256 in [
        (ARCHIVE, ARCHIVE_URL, ARCHIVE_SHA256),
        (PRIOR, PRIOR_URL, PRIOR_SHA256),
    ]:
        path = data_dir / name
        if not path.exists():
            part = path.with_name(name + ".part")
            with urllib.request.urlopen(url) as response, open(part, "wb") as out:
                shutil.copyfileobj(response, out)
            part.rename(path)
        with open(path, "rb") as f:
            digest = hashlib.file_digest(f, "sha256").hexdigest()
        if digest != sha256:
            raise SystemExit(f"{path}: sha256 {digest}, expected {sha256}")


def read_prior(data_dir, campaign):
    """Beta parameters of a campaign's items, indexed by item id."""
    prior = yaml.safe_load((data_dir / PRIOR).read_text())[campaign]
    return np.array(prior["alpha"], float), np.array(prior["beta"], float)


def timestamps_us(column):
    """ISO 8601 strings to UTC microseconds since the epoch."""
    return pd.to_datetime(column, format="ISO8601", utc=True).dt.as_unit("us").astype("int64")


def csv_chunks(data_dir, policy, campaign, columns, chunksize=2_000_000):
    """Chunks of one log, read straight from the archive."""
    member = f"open_bandit_dataset/{policy}/{campaign}/{campaign}.csv"
    with zipfile.ZipFile(data_dir / ARCHIVE) as archive, archive.open(member) as f:
        yield from pd.read_csv(
            f, usecols=columns, dtype=dict.fromkeys(FEATURES, str), chunksize=chunksize
        )


def check_log(chunks, *, expected_rows, n_items, uniform):
    """The stop checks of Section 2 on one log, given chunks of CHECK_COLUMNS.

    Returns what was found and, under "stops", every condition that stops the
    run of the campaign.
    """
    rows = outside = 0
    items, positions, times, deviation = set(), set(), [], 0.0
    for chunk in chunks:
        t = timestamps_us(chunk["timestamp"])
        rows += len(chunk)
        outside += int(((t < WEEK_START_US) | (t >= WEEK_START_US + N_BLOCKS * BLOCK_US)).sum())
        items.update(chunk["item_id"].unique().tolist())
        positions.update(chunk["position"].unique().tolist())
        times += [t.min(), t.max()]
        p = chunk["propensity_score"].to_numpy()
        deviation = float(np.maximum(deviation, np.abs(p - 1 / n_items).max()))  # nan stays
    stops = []
    if rows != expected_rows:
        stops.append(f"{rows} rows, expected {expected_rows}")
    if not items <= set(range(n_items)):
        stops.append(f"item ids {min(items)} to {max(items)}, expected 0 to {n_items - 1}")
    if not positions <= {1, 2, 3}:
        stops.append(f"positions {sorted(positions)}, expected 1 to 3")
    if uniform and not deviation <= 1e-9:
        stops.append(f"propensity differs from 1/{n_items} by up to {deviation:.3g}")
    if outside * 1000 > rows:
        stops.append(f"{outside} of {rows} rows lie outside the week")
    report = {
        "rows": rows,
        "item_ids": [min(items), max(items)],
        "positions": sorted(positions),
        "first_timestamp": pd.Timestamp(min(times), unit="us", tz="UTC").isoformat(),
        "last_timestamp": pd.Timestamp(max(times), unit="us", tz="UTC").isoformat(),
        "rows_outside_week": outside,
        "stops": stops,
    }
    if uniform:
        report["max_propensity_deviation"] = deviation
    return report


def check(data_dir, campaigns):
    """Section 2 checks of both logs of each campaign; reads no click."""
    report = {}
    for campaign in campaigns:
        n_items = len(read_prior(data_dir, campaign)[0])
        for policy in ("random", "bts"):
            report[f"{policy}/{campaign}"] = check_log(
                csv_chunks(data_dir, policy, campaign, CHECK_COLUMNS),
                expected_rows=ROWS[policy, campaign],
                n_items=n_items,
                uniform=policy == "random",
            )
    return report


def to_parquet(data_dir, policy, campaign):
    """Convert one log to Parquet, every row as released, unless already done."""
    path = data_dir / f"{policy}_{campaign}.parquet"
    if path.exists():
        return path
    part = path.with_name(path.name + ".part")
    writer = None
    for chunk in csv_chunks(data_dir, policy, campaign, COLUMNS):
        table = pa.Table.from_pandas(
            chunk.assign(timestamp=timestamps_us(chunk["timestamp"])).astype(
                {"item_id": "int16", "position": "int8", "click": "int8"}
            ),
            preserve_index=False,
        )
        writer = writer or pq.ParquetWriter(part, table.schema)
        writer.write_table(table)
    writer.close()
    part.rename(path)
    return path


def read_log(path):
    """A converted log as a frame, user features as categoricals."""
    return pq.read_table(path, read_dictionary=FEATURES).to_pandas()
