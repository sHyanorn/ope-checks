"""The decision rules of the pre-registration. An interval is a pair (low, high)."""


def _contains(interval, x):
    return interval[0] <= x <= interval[1]


def h1(d, d0):
    if d > 0.10 and d > 2 * d0:
        return "inconsistent"
    if d <= d0:
        return "not distinguishable from variation within the hour"
    return "undetermined"


def h2(m, m_interval, cell_intervals):
    n = len(cell_intervals)
    if n < 5:
        return "undetermined"
    containing = sum(_contains(interval, 1) for interval in cell_intervals)
    if 0.98 <= m <= 1.02 and 10 * containing >= 9 * n:  # at least ceil(0.9 n) cells
        return "consistent"
    if not 0.95 <= m <= 1.05 and (m_interval[1] < 0.98 or m_interval[0] > 1.02):
        return "inconsistent"
    return "undetermined"


def h3(ratio_interval):
    if ratio_interval[1] < 1:
        return "low"
    if ratio_interval[0] > 1:
        return "high"
    return "no shortfall shown"


def h4_alignment(d_interval):
    if d_interval[0] > 0:
        return "raises the estimate"
    if d_interval[1] < 0:
        return "lowers the estimate"
    return "no change shown"


def h4_level(rho_interval):
    if rho_interval[1] < 1:
        return "below the on-policy value"
    if rho_interval[0] > 1:
        return "above the on-policy value"
    return "not distinguishable from the on-policy value"


def h4_reading(h3_ips, alignment, level):
    """The reading of the gap, given the labels of H3 (IPS) and H4."""
    if h3_ips != "low":
        return "shortfall not established; gap not read"
    if level == "above the on-policy value":
        return "aligned estimate exceeds the on-policy value"
    below = level == "below the on-policy value"
    if alignment == "raises the estimate":
        if below:
            return "gap shrinks; a residual remains"
        return "gap shrinks; the residual cannot be told from zero"
    return "alignment is not shown to reduce the gap" if below else "cannot be determined"


def h5(difference_interval):
    if difference_interval[0] > 0:
        return "frequencies after a row are associated with clicks in the random log"
    if difference_interval[1] < 0:
        return "the reverse"
    return "not shown"


def h6(ratio_interval):
    if not _contains(ratio_interval, 1):
        return "off"
    if (ratio_interval[1] - ratio_interval[0]) / 2 <= 0.10:
        return "consistent"
    return "undetermined"


def campaigns_differ(difference_interval):
    return not _contains(difference_interval, 0)
