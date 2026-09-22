#!/bin/bash

echo "=================================================="
echo "🚀 INICIANDO INFRAESTRUCTURA INTEGRADA M82 AGI CORE"
echo "=================================================="

# 1. Mantener CPU despierta en Android
termux-wake-lock 2>/dev/null

# 2. Detener instancias previas para evitar colisiones
pkill -f "m82_core_orchestrator" 2>/dev/null
pkill -f "m82_refinitiv_global_chain_daemon" 2>/dev/null
sleep 1

# 3. Iniciar Daemon de Refinitiv
nohup python3 -u ~/M82/m82_refinitiv_global_chain_daemon.py > ~/M82/m82_refinitiv.log 2>&1 &

# 4. Iniciar Orquestador Central
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/M82/m82_orchestrator.log 2>&1 &

echo "=================================================="
echo "✅ SERVICIOS M82 OPERATIVOS EN SEGUNDO PLANO"
echo "=================================================="
