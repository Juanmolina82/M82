import sys, os, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

RSS_MAP = {
    "REUTERS_TOP": "https://news.google.com/rss/search?q=site:reuters.com",
    "TECH_AI_CAPEX": "https://news.google.com/rss/search?q=AI+Capex",
    "VENEZUELA_DESK": "https://news.google.com/rss/search?q=Venezuela+bonds",
    "COMMODITIES_ENERGY": "https://news.google.com/rss/search?q=oil+energy",
    "GLOBAL_MACRO_FED": "https://news.google.com/rss/search?q=Federal+Reserve",
    "LATAM_FX_SOV": "https://news.google.com/rss/search?q=LatAm+FX",
    "MARKET_QUANT": "https://news.google.com/rss/search?q=quant+markets",
    "GEOPOLITICS_DEFENSE": "https://news.google.com/rss/search?q=geopolitics",
    "DEBT_CRYPTO": "https://news.google.com/rss/search?q=Bonds+Crypto",
    "MA_DEALS": "https://news.google.com/rss/search?q=Mergers+Acquisitions",
    "GLOBAL_NEWS_BREAKING": "https://news.google.com/rss/search?q=Boeing+OR+Porsche+OR+Maersk+OR+Volvo+OR+Energy"
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
        print(f"⚡ [INJECTED] [{source}] -> {headline[:50]}...", flush=True)
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

def run_daemon(daemon_name, interval=300):
    print(f"🚀 [DAEMON ONLINE] {daemon_name} activo. Intervalo: {interval}s (5 min)", flush=True)
    init_db()
    url = RSS_MAP.get(daemon_name)
    if not url:
        print(f"❌ Error: Tópico '{daemon_name}' no existe en RSS_MAP.", flush=True)
        return

    while True:
        try:
            headlines = fetch_rss_headlines(url)
            for hl in headlines:
                inject_headline(daemon_name, hl)
        except Exception as e:
            print(f"⚠️ Error en {daemon_name}: {e}", flush=True)
        
        time.sleep(interval)

if __name__ == "__main__":
    daemon_name = sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_NEWS_BREAKING"
    run_daemon(daemon_name)
