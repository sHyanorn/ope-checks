"""Post hoc: pairs of Beta parameters that the prior file gives to more than one campaign."""


def shared_pairs(priors):
    """Counts from priors[campaign] = (alpha, beta), one entry per item.

    `shared[x][y]`: how many pairs of x occur among those of y, and whether
    they stand in the same order in both lists (at the first place a pair
    occupies in y).
    """
    pairs = {c: list(zip(*(x.tolist() for x in ab), strict=True)) for c, ab in priors.items()}
    out = {
        "pairs": {c: len(p) for c, p in pairs.items()},
        "distinct": {c: len(set(p)) == len(p) for c, p in pairs.items()},
        "shared": {},
    }
    for x, of_x in pairs.items():
        out["shared"][x] = {}
        for y, of_y in pairs.items():
            if x != y:
                where = [of_y.index(p) for p in of_x if p in of_y]
                out["shared"][x][y] = {"pairs": len(where), "same_order": where == sorted(where)}
    return out
