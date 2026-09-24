#!/bin/bash
termux-wake-lock
pkill -f python

echo "🛡️ Iniciando M82 en Modo Unificado Seguro..."
nohup python3 -u ~/M82/m82_unified_master.py > ~/m82_execution.log 2>&1 &

echo "✅ M82 operando de forma estable en segundo plano."
echo "📋 Para ver logs en vivo: tail -f ~/m82_execution.log"
