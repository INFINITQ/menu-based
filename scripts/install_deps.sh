#!/usr/bin/env bash
# scripts/install_deps.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Create venv if missing
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found — installing common dev deps"
  pip install flask flask-session flask-socketio python-dotenv boto3 docker sendgrid twilio eventlet
fi

echo "Dependencies installed into .venv"
