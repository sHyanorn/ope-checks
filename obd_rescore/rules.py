"""The decision rules of Section 8 of the registration."""

import numpy as np

Z = 1.959964
PUBLISHED_SHARE, SHARE_TOLERANCE = 0.80, 0.065  # Section 8.5, C1
RELATIVE_TOLERANCE = 1e-6  # Section 8.5, C2


def wilson(k, n):
    """The 95% Wilson score interval of k successes in n trials."""
    p, z2 = k / n, Z**2
    centre = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = Z / (1 + z2 / n) * np.sqrt(p * (1 - p) / n + z2 / (4 * n**2))
    return [float(centre - half), float(centre + half)]


def too_many_removed(removed, n):
    """More than 1% of the runs or replicates."""
    return removed * 100 > n


def compare(y, x, v):
    """Section 8.1: the claimed estimator `y` against `x`, both scored against `v`.

    Each argument holds one value per run or replicate; `v` may be one value for all.
    """
    y, x = np.asarray(y, float), np.asarray(x, float)
    v = np.broadcast_to(np.asarray(v, float), y.shape)
    kept = np.isfinite(y) & np.isfinite(x) & np.isfinite(v)
    n, n_kept = len(y), int(kept.sum())
    error_y, error_x = np.abs(y - v)[kept], np.abs(x - v)[kept]
    closer, farther = int((error_y < error_x).sum()), int((error_x < error_y).sum())
    out = {
        "runs": n,
        "removed": n - n_kept,
        "y_closer": closer,
        "x_closer": farther,
        "ties": n_kept - closer - farther,
    }
    if n_kept:
        out |= {
            "p": closer / n_kept,
            "p_interval": wilson(closer, n_kept),
            "q": farther / n_kept,
            "q_interval": wilson(farther, n_kept),
        }
    if too_many_removed(out["removed"], n):
        out["label"] = "not evaluable"
    elif out["p_interval"][0] > 0.5:
        out["label"] = "holds"
    elif out["q_interval"][0] > 0.5:
        out["label"] = "flips"
    else:
        out["label"] = "undecided"
    return out


def across_estimators(labels):
    """Section 8.3: the labels of BLUE against each estimator, under one reference."""
    if "flips" in labels:
        return "flips"
    if "not evaluable" in labels:
        return "not evaluable"
    return "holds" if all(label == "holds" for label in labels) else "undecided"


def across_references(ips, snips):
    """Section 8.4: the labels against R_IPS and R_SNIPS on Men's."""
    if ips == snips:
        return ips
    if "not evaluable" in (ips, snips):
        return "not evaluable"
    return "references differ"


def unbiasedness(blue, ips):
    """Section 8.3, primary: the interval of BLUE - IPS over the replicates."""
    blue, ips = np.asarray(blue, float), np.asarray(ips, float)
    finite = (blue - ips)[np.isfinite(blue) & np.isfinite(ips)]
    out = {"replicates": len(blue), "removed": len(blue) - len(finite)}
    if len(finite):
        low, high = np.percentile(finite, [2.5, 97.5], method="linear")
        out["interval"] = [float(low), float(high)]
    if too_many_removed(out["removed"], len(blue)):
        out["label"] = "not evaluable"
    else:
        low, high = out["interval"]
        out["label"] = "not contradicted" if low <= 0 <= high else "contradicted"
    return out


def replication_c1(comparison):
    """Section 8.5: the share of runs in which MIPS (w/ SLOPE) is closer than IPS."""
    if comparison["label"] == "not evaluable":
        return "not evaluable"
    if abs(comparison["p"] - PUBLISHED_SHARE) <= SHARE_TOLERANCE:
        return "reproduced"
    return "published share not reproduced"


def replication_c2(values, published):
    """Section 8.5: each value within a relative 1e-6 of the printed one."""
    differences = {name: values[name] - published[name] for name in published}
    within = all(abs(d) <= RELATIVE_TOLERANCE * abs(published[n]) for n, d in differences.items())
    return {
        "label": "reproduced" if within else "not reproduced",
        "differences": differences,
    }
