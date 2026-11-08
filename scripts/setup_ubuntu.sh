#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip nodejs npm
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
(cd frontend && npm install)
echo "Backend and frontend dependencies installed."
echo "API: source .venv/bin/activate && uvicorn agentshield.api:app --app-dir backend --reload"
echo "UI:  cd frontend && npm run dev"
