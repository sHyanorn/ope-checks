import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_the_tests_are_collected_without_the_unix_only_resource_module():
    blocked = "import sys; sys.modules['resource'] = None; import pytest; "
    collect = "sys.exit(pytest.main(['--collect-only', '-q', '-p', 'no:cacheprovider']))"
    done = subprocess.run(
        [sys.executable, "-c", blocked + collect], cwd=ROOT, capture_output=True, text=True
    )
    assert done.returncode == 0, done.stdout[-2000:]
