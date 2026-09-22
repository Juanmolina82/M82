import os, sys, time, sqlite3, urllib.parse
import feedparser

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Búsquedas avanzadas orientadas a Block Buy, Whales & Institutional Flows
BLOCK_QUERIES = [
    '("block trade" OR "institutional buy" OR "whale buy") (NVDA OR AMD OR ARM OR INTC) when:1d',
    '("block trade" OR "merger arbitrage" OR "unusual options") (Paramount OR "Warner Bros") when:1d',
    '("T-Mobile" OR TMUS) ("block trade" OR "Starlink" OR "Direct-to-Cell") when:1d',
    '("dark pool" OR "block buy") (LNG OR Potash OR Oil) when:1d'
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

def inject_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)",
            ('BLOCK_TRADES_FLOW', headline)
        )
        conn.commit()
        conn.close()
        print(f"🐋 [BLOCK_TRADES] Flujo Detectado -> {headline[:65]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ DB Error: {e}", flush=True)

def fetch_rss(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        headlines = []
        for entry in feed.entries[:4]:
            title = entry.title.rsplit(' - ', 1)[0]
            headlines.append(title)
        return headlines
    except Exception as e:
        print(f"⚠️ Error procesando RSS: {e}", flush=True)
        return []

def run():
    print("🚀 [DAEMON ONLINE] BLOCK_TRADES_FLOW - Escaneando compras institucionales y Dark Pools...", flush=True)
    init_db()
    while True:
        total = 0
        for q in BLOCK_QUERIES:
            headlines = fetch_rss(q)
            for hl in headlines:
                inject_headline(hl)
                total += 1
        print(f"✅ Ciclo finalizado. Se procesaron {total} alertas institucionales.", flush=True)
        time.sleep(300) # Reescaneo cada 5 minutos

if __name__ == "__main__":
    run()
