import pytest

from obd import verdicts as v


def test_h1_rule():
    assert v.h1(0.438, 0.109) == "inconsistent"
    assert v.h1(0.10, 0.01) == "undetermined"  # D must exceed 0.10
    assert v.h1(0.30, 0.15) == "undetermined"  # and twice the noise floor
    assert v.h1(0.20, 0.20) == "not distinguishable from variation within the hour"
    assert v.h1(0.05, 0.04) == "undetermined"


@pytest.mark.parametrize(("n", "needed"), [(5, 5), (9, 9), (10, 9), (12, 11), (20, 18), (30, 27)])
def test_h2_needs_nine_in_ten_cell_intervals_to_contain_one(n, needed):
    def label(containing):
        cells = [(0.9, 1.1)] * containing + [(1.01, 1.2)] * (n - containing)
        return v.h2(1.0, (0.99, 1.01), cells)

    assert label(needed) == "consistent"
    assert label(needed - 1) == "undetermined"


def test_h2_rule():
    cells = [(0.9, 1.1)] * 12
    assert v.h2(1.0, (0.99, 1.01), cells[:4]) == "undetermined"  # fewer than five cells
    assert v.h2(0.98, (0.9, 1.0), cells) == "consistent"
    assert v.h2(0.979, (0.9, 1.0), cells) == "undetermined"
    assert v.h2(1.06, (1.03, 1.09), cells) == "inconsistent"
    assert v.h2(1.06, (1.02, 1.09), cells) == "undetermined"  # interval touches [0.98, 1.02]
    assert v.h2(1.04, (1.03, 1.05), cells) == "undetermined"  # M within [0.95, 1.05]
    assert v.h2(0.90, (0.85, 0.97), cells) == "inconsistent"
    assert v.h2(1.0, (0.99, 1.01), [(1.0, 1.1)] * 12) == "consistent"  # closed intervals


def test_h3_rule():
    assert v.h3((0.79, 0.994)) == "low"
    assert v.h3((0.79, 1.0)) == "no shortfall shown"
    assert v.h3((1.01, 1.2)) == "high"


def test_h4_labels():
    assert v.h4_alignment((0.01, 0.2)) == "raises the estimate"
    assert v.h4_alignment((0.0, 0.2)) == "no change shown"
    assert v.h4_alignment((-0.2, -0.01)) == "lowers the estimate"
    assert v.h4_level((0.8, 0.99)) == "below the on-policy value"
    assert v.h4_level((0.8, 1.0)) == "not distinguishable from the on-policy value"
    assert v.h4_level((1.01, 1.2)) == "above the on-policy value"


@pytest.mark.parametrize(
    ("alignment", "level", "reading"),
    [
        ((0.01, 0.2), (0.9, 1.1), "gap shrinks; the residual cannot be told from zero"),
        ((0.01, 0.2), (0.8, 0.99), "gap shrinks; a residual remains"),
        ((-0.1, 0.2), (0.8, 0.99), "alignment is not shown to reduce the gap"),
        ((-0.2, -0.1), (0.8, 0.99), "alignment is not shown to reduce the gap"),
        ((0.01, 0.2), (1.01, 1.2), "aligned estimate exceeds the on-policy value"),
        ((-0.1, 0.2), (1.01, 1.2), "aligned estimate exceeds the on-policy value"),
        ((-0.1, 0.2), (0.9, 1.1), "cannot be determined"),
        ((-0.2, -0.1), (0.9, 1.1), "cannot be determined"),
    ],
)
def test_h4_reading(alignment, level, reading):
    labels = v.h4_alignment(alignment), v.h4_level(level)
    assert v.h4_reading("low", *labels) == reading
    assert v.h4_reading("no shortfall shown", *labels) == "shortfall not established; gap not read"


def test_h5_rule():
    after = "frequencies after a row are associated with clicks in the random log"
    assert v.h5((0.01, 0.3)) == after
    assert v.h5((-0.3, -0.01)) == "the reverse"
    assert v.h5((0.0, 0.3)) == "not shown"


def test_h6_rule():
    assert v.h6((0.95, 1.1)) == "consistent"  # half-width 0.075
    assert v.h6((0.85, 1.1)) == "undetermined"  # contains 1, half-width 0.125
    assert v.h6((1.01, 1.05)) == "off"
    assert v.h6((0.5, 0.99)) == "off"
    assert v.h6((1.0, 1.1)) == "consistent"


def test_campaigns_differ_when_the_interval_of_their_difference_excludes_zero():
    assert v.campaigns_differ((0.01, 0.2))
    assert not v.campaigns_differ((0.0, 0.2))
