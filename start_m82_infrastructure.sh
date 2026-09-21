#!/bin/bash

echo "=========================================="
echo "🚀 INICIANDO AUTOMATIZACIÓN M82 FULL STACK"
echo "=========================================="

# Crear carpetas necesarias
mkdir -p ~/M82/backups
mkdir -p ~/storage/pictures/Telegram
mkdir -p ~/storage/shared/Pictures/Telegram

# Lista de procesos a mantener activos
DAEMONS=(
    "m82_daemon_factory.py"
    "m82_macro_daemon.py"
    "m82_scheduler_v9.py"
    "m82_core_orchestrator.py"
)

# Iniciar cada script si no está corriendo actualmente
for daemon in "${DAEMONS[@]}"; do
    if ! pgrep -f "$daemon" > /dev/null; then
        echo "⚡ Iniciando $daemon..."
        nohup python3 -u ~/M82/$daemon > ~/m82_$(echo $daemon | cut -d'.' -f1).log 2>&1 &
        sleep 1
    else
        echo "✅ $daemon ya está en ejecución."
    fi
done

echo "=========================================="
echo "🔥 TODA LA INFRAESTRUCTURA M82 ESTÁ ACTIVA"
echo "=========================================="
