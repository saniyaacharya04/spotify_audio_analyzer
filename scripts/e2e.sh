#!/usr/bin/env bash
set -e

echo "======================================"
echo " Spotify Audio Analyzer – E2E Test"
echo "======================================"

# -------- CONFIG --------
APP_HOST="127.0.0.1"
APP_PORT="9000"
APP_URL="http://${APP_HOST}:${APP_PORT}"
TRACK_ID="3n3Ppam7vgaVa1iaRUc9Lp"
FREE_KEY="demo-key"
PREMIUM_KEY="premium-key"

# -------- CLEAN PREVIOUS RUN --------
echo "▶ Killing any running uvicorn"
pkill -f "uvicorn src.main:app" || true

echo "▶ Cleaning test database"
rm -f usage.db
touch usage.db
chmod 666 usage.db

# -------- DEPENDENCIES --------
echo "▶ Checking Python"
python --version

echo "▶ Installing dependencies"
pip install -r requirements.txt > /dev/null

# -------- START SERVER --------
echo "▶ Starting API server on port ${APP_PORT}"
uvicorn src.main:app \
  --host ${APP_HOST} \
  --port ${APP_PORT} \
  > /tmp/spotify_e2e.log 2>&1 &

SERVER_PID=$!

# -------- HEALTH CHECK --------
echo "▶ Waiting for API to become ready"
READY=0
for i in {1..15}; do
  if curl -s "$APP_URL/health" | grep "ok" >/dev/null; then
    READY=1
    echo "✔ Health OK"
    break
  fi
  sleep 1
done

if [ "$READY" -ne 1 ]; then
  echo "❌ Health check failed"
  echo "---- uvicorn log ----"
  cat /tmp/spotify_e2e.log || true
  exit 1
fi

