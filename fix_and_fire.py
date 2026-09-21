import sqlite3, os, hashlib, time, sys

# 1. Localizar la base de datos real
possible_paths = [
    os.path.expanduser("~/M82/m82_database.db"),
    os.path.expanduser("~/m82_database.db")
]

db_path = None
for p in possible_paths:
    if os.path.exists(p):
        db_path = p
        break

if not db_path:
    db_path = possible_paths[0]

print(f"🛢️ Usando base de datos: {db_path}")

conn = sqlite3.connect(db_path, timeout=15)
cursor = conn.cursor()

# 2. Asegurar que la tabla m82_multi_stream exista con el esquema completo
cursor.execute("""
CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    daemon_source TEXT,
    headline TEXT,
    md5_hash TEXT UNIQUE,
    status TEXT DEFAULT 'PENDING'
);
""")

# 3. Titulares para la ráfaga
test_headlines = [
    "Chevron nears Venezuela deal as US prepares 17-field oil lease",
    "Delcy Rodriguez requests escrow release for payroll",
    "PDVSA Orinoco oil exports surge following new OFAC guidelines"
]

ts = time.strftime('%Y-%m-%d %H:%M:%S')

# 4. Inyección
for title in test_headlines:
    h = hashlib.md5(title.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, md5_hash, status)
            VALUES (?, 'REUTERS_BREAKING_ONLY', ?, ?, 'PENDING')
        """, (ts, title, h))
        print(f"📥 Evento inyectado a DB: {title}")
    except sqlite3.IntegrityError:
        # Si ya existía, forzamos su estado a PENDING para re-despacharlo
        cursor.execute("UPDATE m82_multi_stream SET status = 'PENDING' WHERE md5_hash = ?", (h,))
        print(f"🔄 Estado restablecido a PENDING: {title}")

conn.commit()
conn.close()
print("✅ Inyección completada con éxito.")
