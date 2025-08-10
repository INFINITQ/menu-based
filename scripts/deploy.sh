#!/usr/bin/env bash
# scripts/deploy.sh
# Basic local 'deploy' step for developer convenience.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Stopping any existing process (if using systemd, adjust this script)"
# Example: pkill -f "python -m app" || true

echo "Installing dependencies..."
./scripts/install_deps.sh

echo "Starting app in background (use 'fg' or see logs)"
# Run with nohup for demo (not production)
nohup ./scripts/run.sh > logs/app.log 2>&1 &

echo "Started. Logs: $ROOT_DIR/logs/app.log"
