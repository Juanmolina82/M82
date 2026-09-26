#!/usr/bin/env bash
termux-wake-lock
echo "🚀 Arrancando Motor Único M82-Lite..."
pkill -9 -f "python3" || true
nohup python3 -u ~/M82/m82_unified_core.py > ~/M82/m82_unified.log 2>&1 &
echo "✨ Infraestructura ultraligera operativa."
