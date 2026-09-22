#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_health_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            status TEXT,
            response_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_health(target, status, rtime=0.0):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_health_log (target, status, response_time)
            VALUES (?, ?, ?)
        """, (target, status, rtime))
        conn.commit()
        conn.close()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [HEALTH-CHECK] {target}: {status} ({rtime:.3f}s)", flush=True)
    except Exception as e:
        print(f"❌ Error guardando log: {e}", flush=True)

def check_endpoints():
    endpoints = {
        "META_GRAPH_API": "https://graph.facebook.com",
        "TELEGRAM_BOT_API": "https://api.telegram.org",
        "SEC_EDGAR_API": "https://www.sec.gov"
    }
    
    for name, url in endpoints.items():
        try:
            start = time.time()
            r = requests.get(url, timeout=5, headers={"User-Agent": "M82-Monitor/1.0"})
            elapsed = time.time() - start
            if r.status_code < 500:
                log_health(name, "ONLINE", elapsed)
            else:
                log_health(name, f"HTTP_{r.status_code}", elapsed)
        except Exception as e:
            log_health(name, "BLIND_SPOT_OUTAGE", 0.0)

def main():
    init_db()
    print("🛡️ M82 API & Scraper Health Checker Activo.")
    while True:
        check_endpoints()
        time.sleep(300) # Verificación cada 5 min

if __name__ == "__main__":
    main()
