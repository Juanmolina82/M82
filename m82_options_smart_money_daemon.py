#!/usr/bin/env python3
import os, sys, time, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
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
    print(f"[{timestamp}] [OPTIONS-SMART-MONEY] {msg}", flush=True)

def parse_and_inject_option_flow():
    init_db()
    
    # Datos de la señal de flujo institucional
    source = "OPTIONS_SMART_MONEY"
    headline = "INTC $44M PUT SALE: 5K Jan-28 $200 Puts sold @ $88 -> Smart Money floor set at $112 Breakeven on Agentic AI CPU Rally"

    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status)
            VALUES (?, ?, 'PENDING')
        """, (source, headline))
        conn.commit()
        log(f"✅ Señal inyectada a la cola M82: {headline[:70]}...")
        conn.close()
    except sqlite3.IntegrityError:
        log("ℹ️ La señal ya existe en la base de datos (Duplicado omitido).")
    except Exception as e:
        log(f"❌ Error al escribir en DB: {e}")

if __name__ == "__main__":
    parse_and_inject_option_flow()
