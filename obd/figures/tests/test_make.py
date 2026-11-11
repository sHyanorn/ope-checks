import json
import struct

import pytest

pytest.importorskip("matplotlib")
from obd.figures import make  # noqa: E402


def quantity(estimate, low, high):
    return {"estimate": estimate, "interval": [low, high], "undefined_replicates": 0}


def campaign():
    return {
        "h1": {"d": 0.5, "d0": 0.1, "first_hour": [0.2, 0.1, 0.1]},
        "h4": {"width": 3},
        "quantities": {"h3.ips": quantity(0.95, 0.9, 1.0), "h4.rho.3": quantity(1.0, 0.9, 1.1)},
    }


def size(path):
    """Width and height of a PNG file in pixels."""
    with path.open("rb") as file:
        return struct.unpack(">8x4x4sII", file.read(24))[1:]


def results(tmp_path):
    """Result files with the keys the figures read; the arguments that point `make` at them."""
    pooled = {
        "replicates": 100,
        "weights": {"all": 0.54, "women": 0.46},
        "h4": {"widths": {"all": 3, "women": 3}},
        "quantities": {"h3.ips": quantity(0.97, 0.9, 1.0), "h4.rho": quantity(1.0, 0.9, 1.1)},
    }
    for name, result in {"all": campaign(), "women": campaign(), "pooled": pooled}.items():
        (tmp_path / f"{name}.json").write_text(json.dumps(result))
    unit = {"ips": quantity(0.9, 0.8, 1.0)}
    h3 = {"h3": {"rows": unit, "impressions": unit, "blocks": unit}}
    units = {"replicates": 100, "all": h3, "women": h3, "men": h3}
    (tmp_path / "units.json").write_text(json.dumps(units))
    return ["--registered", str(tmp_path), "--posthoc", str(tmp_path), "--out", str(tmp_path)]


NAMES = ["confirmatory-estimates", "prior-distance", "resampling-units"]


def test_every_figure_is_written_in_both_modes_at_the_same_size(tmp_path):
    make.main(results(tmp_path))

    written = sorted(path.name for path in tmp_path.glob("*.png"))
    assert written == [f"{name}-{mode}.png" for name in NAMES for mode in ("dark", "light")]
    for name in NAMES:
        light, dark = (size(tmp_path / f"{name}-{mode}.png") for mode in ("light", "dark"))
        assert light == dark and light[0] >= 1600


def test_pdf_writes_each_figure_once_and_no_png(tmp_path):
    make.main([*results(tmp_path), "--pdf"])

    assert sorted(path.name for path in tmp_path.glob("*.pdf")) == [f"{name}.pdf" for name in NAMES]
    assert not list(tmp_path.glob("*.png"))
    for name in NAMES:
        assert (tmp_path / f"{name}.pdf").read_bytes().startswith(b"%PDF")
