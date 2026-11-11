"""Coverage, its Monte Carlo interval and the labels of Section 9."""

import numpy as np

from obd_coverage.moments import Z

BAND = (0.925, 0.975)


def wilson(k, n):
    """Wilson 95% interval of a proportion of k in n."""
    p, z2 = k / n, Z**2
    centre = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = Z * np.sqrt(p * (1 - p) / n + z2 / (4 * n**2)) / (1 + z2 / n)
    return float(centre - half), float(centre + half)


def label(interval):
    low, high = interval
    if BAND[0] <= low and high <= BAND[1]:
        return "adequate"
    if high < BAND[0]:
        return "under-covers"
    if low > BAND[1]:
        return "over-covers"
    return "unresolved"


def cell(estimate, low, high, sd, truth):
    """What Section 8 reports for one scenario, campaign, quantity and unit.

    The arguments run over the data sets: the estimate, the ends of its
    interval and the standard deviation of its replicates.
    """
    n = len(estimate)
    covered = int(((low <= truth) & (truth <= high)).sum())
    interval = wilson(covered, n)
    centre = estimate.mean()
    return {
        "coverage": covered / n,
        "wilson": list(interval),
        "label": label(interval),
        "contains_nominal": bool(interval[0] <= 0.95 <= interval[1]),
        "interval_below_truth": float((high < truth).mean()),
        "interval_above_truth": float((low > truth).mean()),
        "mean_width": float((high - low).mean()),
        "median_width": float(np.median(high - low)),
        "sd_of_replicates_over_sd_of_estimate": float(sd.mean() / estimate.std(ddof=1)),
        "coverage_of_mean_estimate": float(((low <= centre) & (centre <= high)).mean()),
    }


def spread(x):
    """Mean and percentiles of a ratio over the data sets."""
    low, median, high = np.percentile(x, [2.5, 50, 97.5])
    return {
        "mean": float(x.mean()),
        "p2.5": float(low),
        "median": float(median),
        "p97.5": float(high),
    }


def shortest_adequate(labels):
    """Item 3 of Section 9, from the labels by block length in increasing order.

    Returns the shortest adequate length and whether every longer one is
    adequate too, or (None, False).
    """
    lengths = list(labels)
    for i, minutes in enumerate(lengths):
        if labels[minutes] == "adequate":
            return minutes, all(labels[m] == "adequate" for m in lengths[i:])
    return None, False
