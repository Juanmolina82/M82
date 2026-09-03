#!/data/data/com.termux/files/usr/bin/bash

# Configuración
BACKUP_DIR="$HOME/M82_Backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/m82_core_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

# 1. Copia de respaldo local comprimida
tar --exclude='*.log' \
    --exclude='__pycache__' \
    -czf "$BACKUP_FILE" -C "$HOME" M82

# 2. Respaldar configuración de Crontab
crontab -l > "$HOME/M82/cron_backup.bak"

print("[OK] Respaldo comprimido creado en: $BACKUP_FILE")
