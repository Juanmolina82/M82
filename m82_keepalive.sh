#!/bin/bash
termux-wake-lock
while true; do
    echo "🚀 Manteniendo M82 activo..."
    python3 ~/M82/m82_high_frequency.py
    echo "⚠️ Proceso interrumpido. Reiniciando en 3 segundos..."
    sleep 3
done
