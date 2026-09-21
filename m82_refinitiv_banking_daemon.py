#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

REFINITIV_TOP_STORIES = [
    ("REFINITIV_BANKING", "SocGen Lifts Profitability Target Above 10% For 2026, Pledges Additional Cost Cuts"),
    ("REFINITIV_MARKETS", "World Bank & IMF Back Changes To Debt Framework For Low-Income Countries"),
    ("REFINITIV_FINANCE", "SoftBank Launches $11 Billion Bond Sale To Fund Massive OpenAI Investment"),
    ("REFINITIV_BANKING", "Swiss Business Groups Pressure Parliament Over Strict UBS Capital Rules"),
    ("REFINITIV_MARKETS", "Fed And BoE Probe Major Banks Exposure To Trading Firms After Jane Street Loss")
]

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
    print(f"[{timestamp}] [REFINITIV-DESK] {msg}", flush=True)

def inject_refinitiv_headlines():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    count = 0
    for source, hl in REFINITIV_TOP_STORIES:
        try:
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (source, hl))
            count += 1
            log(f"⚡ [INJECTED] [{source}] -> {hl[:50]}...")
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            log(f"❌ Error en DB: {e}")
    conn.commit()
    conn.close()
    return count

def main():
    init_db()
    log("📡 Daemon Refinitiv Banking & Financial Services desplegado.")
    inject_refinitiv_headlines()

if __name__ == "__main__":
    main()
