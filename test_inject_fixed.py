import sqlite3, os, hashlib, time

DB_PATHS = [
    os.path.expanduser("~/M82/m82_database.db"),
    os.path.expanduser("~/m82_database.db")
]

db_path = None
for p in DB_PATHS:
    if os.path.exists(p):
        db_path = p
        break

if not db_path:
    db_path = DB_PATHS[0]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

test_headlines = [
    "Chevron nears Venezuela deal as US prepares 17-field oil lease",
    "Delcy Rodriguez requests escrow release for payroll",
    "PDVSA Orinoco oil exports surge following new OFAC guidelines"
]

ts = time.strftime('%Y-%m-%d %H:%M:%S')

for title in test_headlines:
    h = hashlib.md5(title.encode()).hexdigest()
    try:
        # Intenta insercion con esquema completo (timestamp, daemon_source, headline, md5_hash, status)
        cursor.execute("""
            INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, md5_hash, status)
            VALUES (?, 'REUTERS_BREAKING_ONLY', ?, ?, 'PENDING')
        """, (ts, title, h))
        print(f"📥 Evento inyectado a DB: {title}")
    except sqlite3.OperationalError:
        # Si la tabla tiene esquema simplificado (daemon_source, headline, status)
        try:
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES ('REUTERS_BREAKING_ONLY', ?, 'PENDING')
            """, (title,))
            print(f"📥 Evento inyectado (modo simplificado): {title}")
        except Exception as e:
            print(f"❌ Error al insertar: {e}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Ya existía en DB: {title}")

conn.commit()
conn.close()
