#!/usr/bin/env bash

termux-wake-lock

echo "🚀 [M82] Reiniciando entorno y procesos..."
pkill -f "m82_" || true

echo "🚀 [M82] Arrancando Orquestador Maestro..."
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/M82/m82_orchestrator.log 2>&1 &

echo "🚀 [M82] Lanzando Daemons concurrentes..."
for daemon in ~/M82/m82_*.py; do
    if [[ "$daemon" != *"m82_core_orchestrator.py"* ]]; then
        bname=$(basename "$daemon")
        nohup python3 -u "$daemon" > ~/M82/${bname%.py}.log 2>&1 &
    fi
done

echo "✨ Infraestructura M82 totalmente desplegada y ejecutándose."
