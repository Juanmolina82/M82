#!/usr/bin/env python3
import os, sys, time, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [GEOPOLITICS-DAEMON] {msg}", flush=True)

def push_geopolitical_signal(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ Señal Geopolítica Registrada: {headline}")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error DB: {e}")

def main():
    init_db()
    log("📡 Daemon M82 de Geopolítica & Licencias OFAC Activo.")
    
    headlines = [
        "OFAC LICENSES: Licencia Chevron opera bajo esquema rolling mensual sin garantia tras expiracion de GL 41B",
        "GEOPOLITICS RISK: Ventana critica de renovacion OFAC el 27 de Noviembre condiciona liquidez de Caracas previo al 10 de Enero",
        "US TREASURIES: Rendimiento del bono a 30Y en 5.48% eleva presion en cumbre Bilateral por tenencia de deuda china"
    ]

    for h in headlines:
        push_geopolitical_signal("M82_GEOPOLITICS_OFAC", h)
        time.sleep(1)

if __name__ == "__main__":
    main()
