#!/usr/bin/env bash
# scripts/run.sh
# Start the Flask app using Flask-SocketIO development runner.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Activate virtualenv if present
if [ -f .venv/bin/activate ]; then
  echo "Activating .venv"
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export FLASK_APP=app
export FLASK_ENV=development
export PYTHONUNBUFFERED=1

# Use python -m to run create_app and socketio.run (we included a __main__ in app/__init__.py)
echo "Starting app on http://0.0.0.0:5000"
python -m app
