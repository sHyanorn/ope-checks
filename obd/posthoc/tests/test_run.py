from obd.posthoc import run
from obd.tests.fixtures import log, rows


def test_load_leaves_out_the_rows_outside_the_week(tmp_path):
    week = 7 * 24 * 60
    frame = log(rows(2, minute=0) + rows(1, minute=-1) + rows(1, minute=week))
    frame.to_parquet(tmp_path / "random_men.parquet")
    assert len(run.load(tmp_path, "random", "men")) == 2


def quantity(estimate, low, high):
    return {"estimate": estimate, "interval": [low, high], "undefined_replicates": 0}


def test_only_quantities_outside_h7_are_compared_with_the_registered_result():
    registered = {
        "h3.ips": quantity(0.9, 0.8, 1.0),
        "h4.rho.3": quantity(1.0, 0.9, 1.1),
        "h7.tv.joint": quantity(0.3, 0.2, 0.4),
    }
    post_hoc = registered | {"h7.tv.joint": quantity(0.01, 0.0, 0.02)}
    assert run.differing(registered, post_hoc) == []
    post_hoc["h4.rho.3"] = quantity(1.0, 0.9, 1.1001)
    assert run.differing(registered, post_hoc) == ["h4.rho.3"]


def test_load_reads_only_the_columns_asked_for(tmp_path):
    log(rows(2, minute=0) + rows(1, minute=-1)).to_parquet(tmp_path / "bts_men.parquet")
    got = run.load(tmp_path, "bts", "men", ["timestamp", "item_id", "position"])
    assert list(got.columns) == ["timestamp", "item_id", "position"] and len(got) == 2
