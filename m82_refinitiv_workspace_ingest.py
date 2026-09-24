#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

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
    print(f"[{timestamp}] [REFINITIV-INGEST] {msg}", flush=True)

def push_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ Registrado: {headline[:55]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error DB: {e}")

def main():
    init_db()
    log("📡 Adaptador Refinitiv Workspace activo.")
    
    # Inyección de titulares capturados del monitor de Refinitiv
    refinitiv_captures = [
        ("REFINITIV_SPX", "Argentina Launches 1st Fixed ETF: An Effort to Boost the Investable Local Market"),
        ("REFINITIV_SPX", "The A-List: Investors Sense High Uncertainty and Volatility, Experts Advice Staying in Market"),
        ("REFINITIV_SPX", "JM Smucker, Monster Beverage Highlighted in Zacks Credit Survey")
    ]
    
    for src, title in refinitiv_captures:
        push_headline(src, title)

if __name__ == "__main__":
    main()
