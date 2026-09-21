#!/bin/bash
termux-wake-lock 2>/dev/null
if ! pgrep -f "m82_core_orchestrator.py" > /dev/null; then
    echo "[$(date)] ⚠️ Orquestador M82 caído. Reiniciando infraestructura..." >> ~/m82_guardian.log
    nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/m82_telegram.log 2>&1 &
fi
