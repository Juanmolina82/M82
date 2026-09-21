import sys, os, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Filtro Alpha M82: Solo 4 Canales Reales
RSS_MAP = {
    "CRYPTO_COMMODITIES": "https://news.google.com/rss/search?q=Bitcoin+OR+Ethereum+OR+Crude+Oil+when:1d&hl=en-US&gl=US&ceid=US:en",
    "REUTERS_WSJ": "https://news.google.com/rss/search?q=site:reuters.com+OR+site:wsj.com+breaking+when:1d&hl=en-US&gl=US&ceid=US:en",
    "TREASURY_YIELDS": "https://news.google.com/rss/search?q=Treasury+yields+OR+Gold+price+when:1d&hl=en-US&gl=US&ceid=US:en",
    "DARK_POOLS": "https://news.google.com/rss/search?q=dark+pool+block+trade+equities+when:1d&hl=en-US&gl=US&ceid=US:en"
}

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

def inject_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO m82_multi_stream (daemon_source, headline) VALUES (?, ?)", (source, headline))
        conn.commit()
        conn.close()
        print(f"⚡ [FILTERED ALPHA] [{source}] -> {headline[:50]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ DB Error: {e}", flush=True)

def fetch_rss_headlines(url):
    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        root = ET.fromstring(req.content)
        items = root.findall('.//item/title')
        return [item.text.rsplit(' - ', 1)[0] for item in items if item.text]
    except Exception:
        return []

def run_daemon(daemon_name, query=""):
    init_db()
    url = RSS_MAP.get(daemon_name)
    if url:
        headlines = fetch_rss_headlines(url)
        for hl in headlines:
            inject_headline(daemon_name, hl)

if __name__ == "__main__":
    daemon_name = sys.argv[1] if len(sys.argv) > 1 else "REUTERS_WSJ"
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    run_daemon(daemon_name, query)
