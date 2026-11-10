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


def test_every_figure_is_written_in_both_modes_at_the_same_size(tmp_path):
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

    make.main(["--registered", str(tmp_path), "--posthoc", str(tmp_path), "--out", str(tmp_path)])

    written = sorted(path.name for path in tmp_path.glob("*.png"))
    names = ["confirmatory-estimates", "prior-distance", "resampling-units"]
    assert written == [f"{name}-{mode}.png" for name in names for mode in ("dark", "light")]
    for name in names:
        light, dark = (size(tmp_path / f"{name}-{mode}.png") for mode in ("light", "dark"))
        assert light == dark and light[0] >= 1600
