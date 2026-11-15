"""The environments of the published codes, built by obd_rescore/setup.sh.

Tests that need one run when RESCORE_DIR (default ~/.cache/ope-checks/rescore) holds
it and are skipped otherwise, unless RESCORE_REQUIRE names it.
"""

import os
import subprocess
from pathlib import Path

import numpy as np
import pytest

from obd_rescore import logs
from obd_rescore.tests import synthetic

DIR = Path(os.environ.get("RESCORE_DIR", Path.home() / ".cache" / "ope-checks" / "rescore"))
SOURCES = {
    "mips": DIR / "src" / "icml2022-mips" / "src" / "real",
    "blue": DIR / "src" / "recsys2024_optimal_baseline",
    "notebook": DIR / "src" / "meta-ope-recsys-2025" / "BLUE OPE.ipynb",
}


def python(env):
    path = DIR / "envs" / env / "bin" / "python"
    if path.exists():
        return path
    if env in os.environ.get("RESCORE_REQUIRE", "").split(","):
        pytest.fail(f"{path} is required")
    pytest.skip(f"no environment {env} in {DIR}")


def run(env, code, *args, cwd=None):
    """Run `code` in an environment; returns its standard output."""
    done = subprocess.run(
        [python(env), "-I", "-c", code, *map(str, args)], capture_output=True, text=True, cwd=cwd
    )
    assert done.returncode == 0, done.stderr[-3000:]
    return done.stdout


ITEMS = {"all": 80, "men": 34, "women": 46}
POLICIES = ("random", "bts")


@pytest.fixture(scope="session")
def archive(tmp_path_factory):
    """A small synthetic archive of the three campaigns."""
    path = tmp_path_factory.mktemp("obd")
    campaigns = {c: (n, {"random": 3000, "bts": 1500}) for c, n in ITEMS.items()}
    synthetic.write(path, campaigns, np.random.default_rng(0))
    return path


@pytest.fixture(scope="session")
def extracted(archive):
    """The files obp reads, as `logs.extract` writes them."""
    return logs.extract(archive, archive / "extracted", [(p, c) for p in POLICIES for c in ITEMS])
