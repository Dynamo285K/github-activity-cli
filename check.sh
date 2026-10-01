#!/usr/bin/env bash

set -euo pipefail

FILE="${1:-github-activity-cli.py}"

if ! command -v ruff >/dev/null 2>&1; then
    echo "Ruff package is not installed. Instal it first." >&2
    echo 'Try using: "python3 -m pip install ruff"'
    exit 1
fi    

echo "==> Lint"
ruff check --fix "$FILE"

echo "==> Format"
ruff format "$FILE"

echo "==> Syntax check"
python3 -m py_compile "$FILE"

echo "DONE"

