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
sleep 4

# -------- HEALTH CHECK --------
echo "▶ Health check"
if ! curl -s "$APP_URL/health" | grep "ok" >/dev/null; then
  echo "❌ Health check failed"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Health OK"

# -------- FREE ANALYZE --------
echo "▶ Free API key – track metadata"
if ! curl -s -H "X-API-Key: $FREE_KEY" \
  "$APP_URL/analyze/$TRACK_ID" | grep "track_name" >/dev/null; then
  echo "❌ Free analyze failed"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Free analyze works"

# -------- INVALID KEY --------
echo "▶ Invalid API key blocked"
STATUS=$(curl -o /dev/null -s -w "%{http_code}" \
  -H "X-API-Key: wrong-key" \
  "$APP_URL/analyze/$TRACK_ID")

if [ "$STATUS" != "401" ]; then
  echo "❌ Invalid key not rejected (status=$STATUS)"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Invalid key rejected"

# -------- USAGE LIMIT --------
echo "▶ Usage limit enforcement"

LIMIT_STATUS="200"
for i in {1..25}; do
  LIMIT_STATUS=$(curl -o /dev/null -s -w "%{http_code}" \
    -H "X-API-Key: limit-test-key" \
    "$APP_URL/analyze/$TRACK_ID")

  if [ "$LIMIT_STATUS" = "403" ]; then
    break
  fi
done

if [ "$LIMIT_STATUS" != "403" ]; then
  echo "❌ Usage limit NOT enforced"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Usage limit enforced"


# -------- PREMIUM BLOCK --------
echo "▶ Premium feature blocked for free user"
STATUS=$(curl -o /dev/null -s -w "%{http_code}" \
  -X POST \
  -H "X-API-Key: $FREE_KEY" \
  "$APP_URL/premium/audio-features/$TRACK_ID")

if [ "$STATUS" != "402" ]; then
  echo "❌ Premium feature not blocked (status=$STATUS)"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Premium blocked correctly"

# -------- PREMIUM ALLOWED --------
echo "▶ Premium feature allowed"
if ! curl -s -X POST \
  -H "X-API-Key: $PREMIUM_KEY" \
  "$APP_URL/premium/audio-features/$TRACK_ID" \
  | grep "Premium Audio Features" >/dev/null; then
  echo "❌ Premium access failed"
  kill $SERVER_PID
  exit 1
fi
echo "✔ Premium access works"

# -------- SHUTDOWN --------
echo "▶ Shutting down server"
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true

echo "======================================"
echo " ALL E2E TESTS PASSED"
echo "======================================"
