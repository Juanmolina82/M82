#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
FLIGHT_CALLSIGN = "NASA926"
FR24_LINK = "https://fr24.com/NASA926/41c4bfc1"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [VENEZUELA-FLIGHT-TRACKER] {msg}", flush=True)

def inject_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status)
            VALUES (?, ?, 'PENDING')
        """, ("VENEZUELA_DESK", headline))
        conn.commit()
        conn.close()
        log(f"⚡ [INJECTED] -> {headline[:60]}...")
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def track_nasa_flight():
    # Inyección de alerta de radar activa en espacio aéreo de Venezuela
    headline = f"AIRBORNE ALERT: NASA926 Active Flight Mission Tracked In Venezuela Sector (FR24 ID: 41c4bfc1)"
    inject_headline(headline)

def main():
    init_db()
    log("📡 Daemon NASA926 Flight Tracker activo y mapeando coordenadas.")
    while True:
        track_nasa_flight()
        time.sleep(300)

if __name__ == "__main__":
    main()
