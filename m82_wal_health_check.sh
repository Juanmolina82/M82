#!/usr/bin/env bash
set -e
DB=~/M82/m82_database.db
echo "🔍 [M82 WAL HEALTH CHECK] Verificando contención..."
sqlite3 $DB <<SQL
PRAGMA busy_timeout=60000;
PRAGMA journal_mode=WAL;
PRAGMA wal_checkpoint(TRUNCATE);
SQL
STATUS=$(sqlite3 $DB "PRAGMA wal_checkpoint(TRUNCATE);")
echo "📊 WAL STATUS: $STATUS"
if echo "$STATUS" | grep -q "0|0|0\|0 busy.*0 log.*0"; then
  echo "🟢 VERIFICACIÓN COMPLETADA – CERO CONTENCIÓN EN NODO CARACAS HQ / CHARALLAVE EDGE"
else
  echo "⚠️ Contención residual: $STATUS — aplicando purge extra..."
  sqlite3 $DB "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(RESTART); PRAGMA wal_checkpoint(TRUNCATE);"
fi
sqlite3 $DB "PRAGMA wal_checkpoint(TRUNCATE);"
