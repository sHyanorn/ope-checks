"""A small synthetic archive shared by the tests."""

import numpy as np
import pytest

from obd_rescore.tests import synthetic

ITEMS = {"all": 80, "men": 34, "women": 46}
POLICIES = ("random", "bts")


@pytest.fixture(scope="session")
def archive(tmp_path_factory):
    """A small synthetic archive of the three campaigns."""
    path = tmp_path_factory.mktemp("obd")
    campaigns = {c: (n, {"random": 3000, "bts": 1500}) for c, n in ITEMS.items()}
    synthetic.write(path, campaigns, np.random.default_rng(0))
    return path
