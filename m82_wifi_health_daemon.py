#!/usr/bin/env python3
import os, sys, time, sqlite3, subprocess

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GATEWAY_IP = "192.168.2.1"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [WIFI-5G-MONITOR] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM m82_multi_stream WHERE headline = ?", (headline,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (source, headline))
            conn.commit()
            log(f"✅ [{source}] Evento Registrado: {headline[:60]}...")
        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def check_network_health():
    # Test de ping al Gateway 192.168.2.1
    res = subprocess.run(["ping", "-c", "2", "-w", "3", GATEWAY_IP], capture_output=True, text=True)
    if res.returncode != 0:
        insert_headline("WIFI_DROP_ALERT", f"ALERTA RED: Pérdida de enlace con el Gateway {GATEWAY_IP}")
    else:
        log(f"🟢 Enlace Gateway {GATEWAY_IP} activo.")

def main():
    init_db()
    log("📡 Daemon Wi-Fi 5GHz & Gateway Monitor Activo.")
    while True:
        check_network_health()
        time.sleep(60)

if __name__ == "__main__":
    main()
