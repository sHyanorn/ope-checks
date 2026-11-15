#!/usr/bin/env bash
# The third-party code at its registered commits and the three environments of Section 5.
#
#     obd_rescore/setup.sh DIR [ENV ...]     ENV: study, mips, blue (default: all three)
#
# Writes DIR/src/<repository> and DIR/envs/<env>. The environments are installed from
# locks/<env>.txt with their hashes; study.txt is compiled from pyproject.toml with
#     uv pip compile pyproject.toml --extra dev -p 3.13.14 --generate-hashes --no-header
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
dir=$(realpath -m "$1")
shift
envs=("$@")
[ ${#envs[@]} -gt 0 ] || envs=(study mips blue)
mkdir -p "$dir/src" "$dir/envs"

fetch() { # repository, commit
  local path="$dir/src/${1#*/}"
  [ -d "$path" ] || git clone -q "https://github.com/$1.git" "$path"
  git -C "$path" checkout -q "$2"
  if [ "$(git -C "$path" rev-parse HEAD)" != "$2" ]; then
    echo "$path is not at $2" >&2
    exit 1
  fi
}

fetch usaito/icml2022-mips 08d65ce04d597d2f7660bfb6da93bf77c86f8b1b
fetch olivierjeunen/meta-ope-recsys-2025 f77886a93358a5063656ff073539a03b04d4bb53
fetch shashankg7/recsys2024_optimal_baseline 137cdbe2488f434f0dbc2997f5bec1194b874a27

declare -A python=([study]=3.13.14 [mips]=3.9.25 [blue]=3.12.2)
for env in "${envs[@]}"; do
  uv python install -q "${python[$env]}"
  [ -x "$dir/envs/$env/bin/python" ] || uv venv -q -p "${python[$env]}" "$dir/envs/$env"
  uv pip sync -q -p "$dir/envs/$env/bin/python" --require-hashes "$here/locks/$env.txt"
done
if [[ " ${envs[*]} " == *" study "* ]]; then
  uv pip install -q -p "$dir/envs/study/bin/python" --no-deps -e "$here/.."
fi
