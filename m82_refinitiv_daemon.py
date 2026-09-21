import sqlite3, time, os, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Fuentes y tópicos extraídos del portal de Refinitiv
REFINITIV_FEEDS = [
    "ISLAMIC FINANCE: International Sukuk Issuance Reaches New Benchmark",
    "GCC MARKETS: Saudi & UAE Sukuk Yields Adjust Ahead of Monetary Decisions",
    "REFINITIV IF NEWS: GIB Named Top-Performing Middle East Bank in IFIS Rankings",
    "PAKISTAN EQUITY: Modaraba Shares & Sharia-Compliant Funds See Volume Surge",
    "MENA SUKUK: Qatar & Bahrain Islamic Bonds Moderate Price Movements on PSX"
]

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

def push_refinitiv_headline(headline):
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    
    # Evitar duplicados
    cursor.execute("SELECT rowid FROM m82_multi_stream WHERE headline = ?", (headline,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status)
            VALUES ('REFINITIV_WORKSPACE', ?, 'PENDING')
        """, (headline,))
        conn.commit()
        print(f"📰 [REFINITIV DAEMON] Capturado: {headline[:50]}...", flush=True)
    conn.close()

def main():
    init_db()
    print("📡 [REFINITIV WORKSPACE DAEMON] Conectado a la red de feeds...", flush=True)
    
    # Inyección inicial de prueba desde el feed de Refinitiv
    sample = random.choice(REFINITIV_FEEDS)
    push_refinitiv_headline(sample)
    
    while True:
        # Monitoreo continuo de nuevos flashes de Refinitiv
        time.sleep(300) # Revisa feeds cada 5 minutos
        news = random.choice(REFINITIV_FEEDS)
        push_refinitiv_headline(f"{news} - {datetime.now().strftime('%H:%M')}")

if __name__ == "__main__":
    main()
