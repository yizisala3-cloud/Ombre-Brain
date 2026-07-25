#!/bin/bash
set -e

# Apply persona engine patches
echo "[Ombre] Applying persona_engine patches..."
python patch_persona.py

echo "[Ombre] Starting Brain (server.py) on :8000..."
python server.py &
BRAIN_PID=$!
echo "[Ombre] Starting Gateway (gateway.py) on :8010..."
python gateway.py &
GATEWAY_PID=$!
echo "[Ombre] Both services started."
wait -n $BRAIN_PID $GATEWAY_PID
echo "[Ombre] A service exited, shutting down..."
kill $BRAIN_PID $GATEWAY_PID 2>/dev/null || true
