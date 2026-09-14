#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "========================================"
echo " TestRail MCP - client install (Unix)"
echo "========================================"
echo
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.11+."
  exit 1
fi
python3 --version
shopt -s nullglob
wheels=(wheel/*.whl)
if [ "${#wheels[@]}" -eq 0 ]; then
  echo "ERROR: No .whl file in wheel/"
  exit 1
fi
if [ ! -d .venv ]; then
  echo "Creating virtual environment .venv ..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
for f in wheel/*.whl; do
  echo "Installing $f"
  python -m pip install "$f"
done
echo
echo "Done. Next: read docs/CLIENT_USER_GUIDE.md and configure Cursor MCP."
echo "Optional: copy .env.example to .env in this folder."
