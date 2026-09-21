#!/data/data/com.termux/files/usr/bin/bash

BACKUP_DIR="$HOME/M82_BACKUPS"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

# Respaldo SQLite con WAL Checkpoint (evita respaldar DBs corruptas)
sqlite3 "$HOME/M82/m82_database.db" ".backup '$BACKUP_DIR/m82_db_$TIMESTAMP.db'"

# Respaldo de Scripts
tar -czf "$BACKUP_DIR/m82_scripts_$TIMESTAMP.tar.gz" -C "$HOME" M82/*.py M82/*.sh M82/.env 2>/dev/null

# Retener solo los últimos 7 respaldos para optimizar espacio
ls -dt $BACKUP_DIR/* | tail -n +15 | xargs rm -rf 2>/dev/null
