#!/data/data/com.termux/files/usr/bin/bash
DATE=$(date +%Y-%m-%d)
DB_PATH="$HOME/M82/m82_database.db"

echo "M82 Daily Alpha Briefing - $DATE" > /data/data/com.termux/files/usr/tmp/alpha.txt
echo "=========================================" >> /data/data/com.termux/files/usr/tmp/alpha.txt

if [ -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" "SELECT headline FROM m82_multi_stream ORDER BY id DESC LIMIT 5;" >> /data/data/com.termux/files/usr/tmp/alpha.txt 2>/dev/null
else
    echo "• Evento destacado M82: Monitoreo activo de Escrow" >> /data/data/com.termux/files/usr/tmp/alpha.txt
fi

echo "📄 Reporte de Inteligencia Diario listo."
