#!/data/data/com.termux/files/usr/bin/bash
mkdir -p ~/M82/logs

# Registrar en la base de datos como HIGH STRESS (Nivel 9)
sqlite3 ~/M82/m82_database.db "INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, status) VALUES (datetime('now'), 'GEOPOLITICS_DEFENSE', 'HIGH STRESS: N.Korea Fires Short-Range Ballistic Missiles Into Sea of Japan During US-ROK Drills', 'PENDING');" 2>/dev/null || true

# Inyectar evento de estrés global en la tabla de métricas/eventos
sqlite3 ~/M82/m82_database.db "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, title TEXT, stress INTEGER);" 2>/dev/null || true
sqlite3 ~/M82/m82_database.db "INSERT INTO events (title, stress) VALUES ('NK SRBM + Iran Comms Cut + NATO Probe Rumor', 9);"

echo "✅ Evento registrado en m82_database.db con nivel HIGH STRESS (9/10)."
