#!/usr/bin/env sh

set -euo pipefail

APP_DIR="/app"
export PYTHONPATH="$APP_DIR"

# TODO: wait-for-it.sh
# rabbitmq is slow, just wait a bit
sleep 15

python3 "$APP_DIR/job.py"
