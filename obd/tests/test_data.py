import zipfile

import numpy as np
import pandas as pd
import pytest

from obd import data
from obd.tests.synthetic import raw_log, uniform

N_ITEMS = 5


@pytest.fixture
def log():
    rng = np.random.default_rng(0)
    return raw_log(rng, 3000, uniform(N_ITEMS), np.full(N_ITEMS, 0.1))


def stops(log, expected_rows=3000, is_uniform=True, chunks=1):
    parts = [log.iloc[i::chunks] for i in range(chunks)]
    report = data.check_log(parts, expected_rows=expected_rows, n_items=N_ITEMS, uniform=is_uniform)
    return report["stops"]


def test_a_log_as_registered_passes(log):
    report = data.check_log([log], expected_rows=3000, n_items=N_ITEMS, uniform=True)
    assert report["stops"] == []
    assert report["rows"] == 3000
    assert report["item_ids"] == [0, N_ITEMS - 1]
    assert report["positions"] == [1, 2, 3]
    assert report["rows_outside_week"] == 0
    assert report["first_timestamp"] == log["timestamp"].min().isoformat()
    assert report["last_timestamp"] == log["timestamp"].max().isoformat()


def test_rows_are_counted_across_chunks(log):
    assert stops(log, chunks=3) == []
    assert stops(log, expected_rows=3001, chunks=3) == ["3000 rows, expected 3001"]


def test_item_id_beyond_the_prior_stops(log):
    log.loc[7, "item_id"] = N_ITEMS
    assert stops(log) == [f"item ids 0 to {N_ITEMS}, expected 0 to {N_ITEMS - 1}"]


def test_fourth_position_stops(log):
    log.loc[7, "position"] = 4
    assert stops(log) == ["positions [1, 2, 3, 4], expected 1 to 3"]


def test_random_log_propensity_off_uniform_stops(log):
    log.loc[7, "propensity_score"] = 1 / N_ITEMS + 5e-17  # as stored in the files
    assert stops(log) == []
    log.loc[7, "propensity_score"] = 1 / N_ITEMS + 2e-9
    assert len(stops(log)) == 1
    assert stops(log, is_uniform=False) == []


def test_missing_propensity_in_the_random_log_stops(log):
    log.loc[7, "propensity_score"] = np.nan
    assert len(stops(log)) == 1
    assert len(stops(log, chunks=3)) == 1


@pytest.mark.parametrize(
    ("timestamp", "outside"),
    [
        ("2019-11-24 00:00:00+00:00", False),
        ("2019-11-23 23:59:59.999999+00:00", True),
        ("2019-11-30 23:59:59.999999+00:00", False),
        ("2019-12-01 00:00:00+00:00", True),
    ],
)
def test_week_boundaries(log, timestamp, outside):
    log.loc[7, "timestamp"] = pd.Timestamp(timestamp)
    report = data.check_log([log], expected_rows=3000, n_items=N_ITEMS, uniform=True)
    assert report["rows_outside_week"] == int(outside)


def test_more_than_one_row_in_a_thousand_outside_the_week_stops(log):
    late = pd.Timestamp("2019-12-01 00:00:00+00:00")
    log.loc[:2, "timestamp"] = late  # 3 of 3000: exactly 0.1%
    assert stops(log) == []
    log.loc[3, "timestamp"] = late
    assert stops(log) == ["4 of 3000 rows lie outside the week"]


def test_timestamps_parse_as_released():
    released = pd.Series(["2019-11-24 00:00:03.800821+00:00", "2019-11-24 00:00:04+00:00"])
    assert data.timestamps_us(released).tolist() == [
        data.WEEK_START_US + 3_800_821,
        data.WEEK_START_US + 4_000_000,
    ]


def test_parquet_round_trip(tmp_path, log):
    released = log.assign(filler=0.0)
    with zipfile.ZipFile(tmp_path / data.ARCHIVE, "w") as archive:
        archive.writestr("open_bandit_dataset/random/men/men.csv", released.to_csv())
    converted = data.read_log(data.to_parquet(tmp_path, "random", "men"))
    assert sorted(converted.columns) == sorted(data.COLUMNS)
    assert converted["timestamp"].tolist() == data.timestamps_us(log["timestamp"]).tolist()
    for column in ["item_id", "position", "click", "propensity_score", *data.FEATURES]:
        assert converted[column].tolist() == log[column].tolist()
