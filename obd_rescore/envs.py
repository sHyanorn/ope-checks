"""The environments of Section 5 and the calls of the adapters in them."""

import os
from pathlib import Path

ADAPTERS = Path(__file__).parent / "adapters"
# One thread per process, so that a resumed process repeats its sums exactly.
THREADS = dict.fromkeys(("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"), "1")


def python(work_dir, env):
    return work_dir / "envs" / env / "bin" / "python"


def sources(work_dir):
    """The published code of C1, the obp of C2 and the notebook of C2."""
    src = work_dir / "src"
    return {
        "mips": src / "icml2022-mips" / "src" / "real",
        "blue": src / "recsys2024_optimal_baseline",
        "notebook": src / "meta-ope-recsys-2025" / "BLUE OPE.ipynb",
    }


def adapter(work_dir, env, *args):
    """The command that runs an adapter in its environment."""
    return [str(python(work_dir, env)), "-I", str(ADAPTERS / f"{env}.py"), *map(str, args)]


def environ():
    return os.environ | THREADS
