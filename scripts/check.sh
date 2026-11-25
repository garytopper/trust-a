#!/usr/bin/env bash
# Run inside a fresh virtual environment after installing requirements-dev.lock.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/sync-skill-references.py --check
python -m compileall -q scripts src examples tests
python -m ruff check src examples scripts tests
python -m ruff format --check src examples/run_workflow.py tests
python -m mypy --check-untyped-defs src/trust_a examples/run_workflow.py
# Normalize wheel timestamps for rebuilds of the same checkout.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-$(git log -1 --format=%ct)}"
python -m build --no-isolation
version=$(python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
python -m pip install --no-deps --force-reinstall "dist/trust_a_toolkit-${version}-py3-none-any.whl"
python -m pip check
python -I -m unittest discover -s tests -v
python -I tests/consumer_smoke.py
