"""Post hoc: the user feature values that occur in only one of the two logs (H7)."""

import numpy as np

from obd import estimators as est
from obd import run, tables
from obd.data import FEATURES


def one_log_values(random, bts):
    """By user feature, the values that occur in only one of the two logs.

    Amendment 7 matched a feature if exactly one value occurs only in each log.
    A row is marked if it holds such a value in every matched feature. Every
    value found comes with its log, its rows, its share of that log's rows and
    how many of its rows are marked.
    """
    logs = {"random": random, "bts": bts}
    values = {
        log: {name: set(frame[name].unique()) for name in FEATURES} for log, frame in logs.items()
    }
    only = {
        "random": {name: sorted(values["random"][name] - values["bts"][name]) for name in FEATURES},
        "bts": {name: sorted(values["bts"][name] - values["random"][name]) for name in FEATURES},
    }
    matched = [name for name in FEATURES if all(len(only[log][name]) == 1 for log in logs)]
    marked = {}
    for log, frame in logs.items():
        marked[log] = np.ones(len(frame), bool)
        for name in matched:
            marked[log] &= (frame[name] == only[log][name][0]).to_numpy()
    return {
        "matched_features": matched,
        "rows_marked": {log: int(m.sum()) for log, m in marked.items()},
        "values": {
            name: [
                {
                    "log": log,
                    "value": value,
                    "rows": int(holds.sum()),
                    "share_of_rows": float(holds.mean()),
                    "rows_marked": int((holds & marked[log]).sum()),
                }
                for log, frame in logs.items()
                for value in only[log][name]
                for holds in [(frame[name] == value).to_numpy()]
            ]
            for name in FEATURES
        },
    }


def same_category(found):
    """By unmatched feature, the value of each log that holds exactly the marked rows.

    A feature is paired only if each log has exactly one such value.
    """
    pairs = {}
    for name, values in found["values"].items():
        exact = {
            log: [
                v["value"]
                for v in values
                if v["log"] == log and v["rows"] == v["rows_marked"] == rows
            ]
            for log, rows in found["rows_marked"].items()
        }
        if name not in found["matched_features"] and all(len(x) == 1 for x in exact.values()):
            pairs[name] = {log: x[0] for log, x in exact.items()}
    return pairs


def rewritten(random, pairs):
    """The random log with each paired value written as the BTS log writes it."""
    return random.assign(
        **{
            name: random[name].cat.rename_categories({pair["random"]: pair["bts"]})
            for name, pair in pairs.items()
        }
    )


def quantities(random, bts, alpha, beta, stream, n_replicates=est.N_REPLICATES):
    """Every bootstrapped quantity of a campaign, computed and summarised by the registered code."""
    t, facts = tables.build(random, bts, alpha / (alpha + beta))
    width, _ = est.choose_width(est.hours(t.b_rows), est.hours(t.r_rows))
    point, replicates = run.bootstrap(
        t,
        est.fixed_prior_target(alpha, beta, stream),
        width,
        est.eligible_cells(facts["min_propensity"]),
        n_replicates,
    )
    return {name: run.summarise(point[name], replicates[name]) for name in point}
