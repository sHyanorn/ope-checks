"""The references of Section 6 against their definitions, row by row."""

import numpy as np

from obd_rescore import logs, references
from obd_rescore.tests.conftest import ITEMS
from obd_rescore.tests.test_logs import frame


def target(rng, n_items, n=None):
    """Distinct probabilities of each item at each position, each position summing to 1."""
    pi = rng.dirichlet(np.ones(n_items), (n or 1, 3)).transpose(0, 2, 1)
    return pi if n else pi[0]


def test_the_published_layout_reads_index_k_n_plus_a():
    for n_items in ITEMS.values():
        pi = target(np.random.default_rng(n_items), n_items)
        published = references.applied(pi, "published")
        for a in range(n_items):
            for k in range(3):
                j = k * n_items + a
                assert published[a, k] == pi[j // 3, j % 3]
        assert (references.applied(pi, "own") == pi).all()
        kept = np.argwhere(published == pi).tolist()
        assert kept == [[0, 0], [n_items - 1, 2]]
    many = target(np.random.default_rng(1), 34, n=4)
    assert (
        references.applied(many, "published")[2] == references.applied(many[2], "published")
    ).all()


def row_values(log, pi_star):
    w = pi_star[log["item_id"], log["position"] - 1] / log["propensity_score"]
    return (log["click"] * w).mean(), (log["click"] * w).sum() / w.sum()


def test_r_ips_and_r_snips_are_the_formulas_of_section_6(archive):
    rng = np.random.default_rng(2)
    for campaign, n_items in ITEMS.items():
        log = frame(archive, "random", campaign)
        tables = logs.tables(archive, "random", campaign, n_items)
        pis = target(rng, n_items, n=3)
        for layout in ("published", "own"):
            pi_star = references.applied(pis, layout)
            out = references.values(tables, pi_star)
            for t in range(3):
                r_ips, r_snips = row_values(log, pi_star[t])
                np.testing.assert_allclose(out["r_ips"][t], r_ips, rtol=1e-12)
                np.testing.assert_allclose(out["r_snips"][t], r_snips, rtol=1e-12)


def test_intervals_are_percentiles_over_blocks_drawn_jointly_in_both_logs(archive):
    random, bts = frame(archive, "random", "men"), frame(archive, "bts", "men")
    pi_star = references.applied(target(np.random.default_rng(3), ITEMS["men"]), "published")
    draws = {name: [] for name in ("v_on", "r_ips", "r_snips")}
    for i in range(3):
        m = logs.c2_multiplicities(i)
        r = random.iloc[np.repeat(np.arange(len(random)), m[logs.blocks(random["timestamp"])])]
        b = bts.iloc[np.repeat(np.arange(len(bts)), m[logs.blocks(bts["timestamp"])])]
        draws["v_on"].append(b["click"].mean())
        for name, value in zip(("r_ips", "r_snips"), row_values(r, pi_star), strict=True):
            draws[name].append(value)
    out = references.intervals(
        logs.tables(archive, "random", "men", ITEMS["men"]),
        logs.tables(archive, "bts", "men", ITEMS["men"]),
        pi_star,
        n_replicates=3,
    )
    draws["r_ips_over_v_on"] = np.divide(draws["r_ips"], draws["v_on"])
    draws["r_snips_over_v_on"] = np.divide(draws["r_snips"], draws["v_on"])
    for name, values in draws.items():
        expected = np.percentile(values, [2.5, 97.5], method="linear")
        np.testing.assert_allclose(out[name], expected, rtol=1e-12)
