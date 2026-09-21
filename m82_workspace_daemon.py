import os
import time
import sqlite3
import requests
from bs4 import BeautifulSoup

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Titulares capturados directamente de la vista activa de Workspace
WS_INITIAL_FEED = [
    ("GLOBAL_MACRO", "Wall Street Ends Volatile Week With Quiet Finish"),
    ("M_AND_A_CORPORATE", "Warren Buffett Steps Down as Berkshire Hathaway Chairman"),
    ("TECH_AI_STREAM", "Anthropic Shifts Planned IPO to November"),
    ("GEOPOLITICS_DEFENSE", "Trump Says U.S. Has Reached Greenland Security Agreement With Denmark"),
    ("CENTRAL_BANKS", "Bank of Japan Raises Rates, Making U.S. Less Alluring For Tokyo Investors"),
    ("AUTOMOTIVE_SECTOR", "Volkswagen Warns on Profit After Big Porsche Write-Down"),
    ("TECH_AI_STREAM", "Nvidia-Backed Cloud Startup Neocloud Files for IPO"),
    ("GEOPOLITICS_POLICY", "Trump Says He Is Banning CNN, MS-NOW and Politico From the White House"),
    ("TECH_POLICY", "The U.S. and China Want AI Guardrails, But Their Ideas Couldn't Be More Different"),
    ("CENTRAL_BANKS", "How Warsh Raised Rates Without Drawing Trump's Ire"),
    ("CRYPTO_REGULATION", "Christine Lagarde Helped Block Binance's Foothold in Europe"),
    ("US_ECONOMY", "Weeks Before the Midterms, Almost Everything Is Getting More Expensive"),
    ("GEOPOLITICS_DEFENSE", "Russia Seizes Control of Nestle's Local Operations")
]

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def push_to_m82_stream(source_tag, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=20.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute(
            "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING');",
            (source_tag, headline)
        )
        if cursor.rowcount > 0:
            print(f"📥 [INGESTED]: [{source_tag}] -> {headline[:50]}...", flush=True)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ DB Push Error: {e}", flush=True)

def run_workspace_ingestor():
    init_db()
    print("🛰️ [M82 WORKSPACE DAEMON]: Iniciando extracción e ingesta masiva...", flush=True)
    
    # Ingesta inicial de la captura
    for desk, headline in WS_INITIAL_FEED:
        push_to_m82_stream(f"M82_{desk}", headline)
        time.sleep(0.2)
        
    print("✅ Ingesta inicial completada. El Daemon queda monitoreando el flujo...", flush=True)

if __name__ == "__main__":
    run_workspace_ingestor()
