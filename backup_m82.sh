#!/data/data/com.termux/files/usr/bin/bash
BACKUP_DIR="$HOME/M82_Backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/m82_core_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

tar --exclude='*.log' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    -czf "$BACKUP_FILE" -C "$HOME" M82

crontab -l > "$HOME/M82/cron_backup.bak" 2>/dev/null
echo "[OK] Respaldo comprimido M82 creado en: $BACKUP_FILE"
