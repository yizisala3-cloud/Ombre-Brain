#!/bin/bash
set -e

# --- Patch persona_engine.py at startup ---
# 1. Fix default model from 'deepseek-chat' to 'deepseek-v4-pro'
sed -i 's/self.persona_cfg.get("model", "deepseek-chat")/self.persona_cfg.get("model", "deepseek-v4-pro")/' persona_engine.py

# 2. Add response_format to _completion_options to force JSON output
# Replace the _completion_options method to include response_format
sed -i 's/"max_tokens": self.max_tokens,/"max_tokens": self.max_tokens,\n            "response_format": {"type": "json_object"},/' persona_engine.py

echo "[Ombre] Applied persona_engine patches (model default + json response_format)"

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
