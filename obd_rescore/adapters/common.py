"""What both adapters share: their records and the files they use."""

import hashlib
import json
import os
import sys
from importlib import metadata
from pathlib import Path


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def package_files(package):
    """The files of an imported package, without the OBD sample shipped with obp."""
    root = Path(package.__file__).parent
    sample = root / "dataset" / "obd"
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and sample not in p.parents and "__pycache__" not in p.parts
    )


def environment(files):
    """The Python version, the installed packages and the sha256 of each file used."""
    return {
        "python": sys.version.split()[0],
        "packages": sorted(f"{d.metadata['Name']}=={d.version}" for d in metadata.distributions()),
        "files": {str(p): sha256(p) for p in files},
    }


class Record:
    """Lines of JSON written one at a time; the first holds the inputs that decide them.

    An existing record is continued only under the same inputs. A line cut off by a
    stop is dropped. `check` recomputes the last line written before a resumed
    process continues.
    """

    def __init__(self, path, inputs):
        self.path = Path(path)
        inputs = json.loads(json.dumps(inputs))
        if self.path.exists():
            text = self.path.read_text()
            text = text[: text.rfind("\n") + 1]
            lines = [json.loads(line) for line in text.splitlines()]
            if lines[0] != {"inputs": inputs}:
                raise SystemExit(f"{self.path} was written under other inputs")
            self.path.write_text(text)
            self.lines = lines[1:]
        else:
            self.path.write_text(json.dumps({"inputs": inputs}) + "\n")
            self.lines = []

    def check(self, compute):
        """`compute(line)` must give the last line again."""
        if self.lines and compute(self.lines[-1]) != self.lines[-1]:
            raise SystemExit(f"{self.path}: the resumed process does not repeat its last line")

    def write(self, line):
        with open(self.path, "a") as f:
            f.write(json.dumps(line) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.lines.append(line)
