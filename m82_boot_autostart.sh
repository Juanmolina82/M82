#!/bin/bash
echo "=== INICIANDO SISTEMA INTEGRADO M82 CORE ==="
termux-wake-lock
pkill -f "m82_" 2>/dev/null
sleep 2

nohup python3 -u ~/M82/m82_refinitiv_global_chain_daemon.py > ~/M82/m82_refinitiv.log 2>&1 &
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/M82/m82_orchestrator.log 2>&1 &

echo "=== M82 INFRAESTRUCTURA OPERATIVA ==="
