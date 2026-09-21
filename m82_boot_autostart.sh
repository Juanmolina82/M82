#!/bin/bash
termux-wake-lock 2>/dev/null
echo "🚀 INICIANDO INFRAESTRUCTURA M82 (32 DAEMONS)"
pkill -f "m82_" 2>/dev/null
sleep 1
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/m82_telegram.log 2>&1 &
sleep 2
if pgrep -f "m82_core_orchestrator.py" > /dev/null; then
    echo "✅ Orquestador y Daemons M82 Activos."
else
    echo "⚠️ Error al arrancar el Orquestador."
fi
