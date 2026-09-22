import sys, os, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Mapa Unificado de Todos los Daemons de Inteligencia M82
RSS_MAP = {
    "TRUMP_XI_TRUCE_TIMELINE": "https://news.google.com/rss/search?q=(%22Trump+Xi+summit%22+OR+%22China+tariffs+truce%22+OR+%22rare+earths+fentanyl%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "TRUMP_NEWSROOM": "https://news.google.com/rss/search?q=(%22Donald+Trump%22+OR+%22Trump+administration%22+OR+%22Trump+tariffs%22+OR+%22Trump+policy%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "MUSK_INC": "https://news.google.com/rss/search?q=SpaceX+OR+Tesla+OR+Starlink+OR+xAI+OR+Neuralink+when:1d&hl=en-US&gl=US&ceid=US:en",
    "SPACEX_TELECOM": "https://news.google.com/rss/search?q=SpaceX+Starlink+Verizon+AT%26T+T-Mobile+spectrum+when:1d&hl=en-US&gl=US&ceid=US:en",
    "GEOPOLITICS_AI": "https://news.google.com/rss/search?q=(%22US-China%22+%22AI+safety%22+OR+%22trade+talks%22+OR+%22semiconductor+export%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "NEW_YORK_DESK": "https://news.google.com/rss/search?q=(%22Wall+Street%22+OR+%22NYSE%22+OR+%22Nasdaq%22+OR+%22Federal+Reserve+Bank+of+New+York%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
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

def run_daemon(daemon_name, query=""):
    print(f"🚀 [DAEMON ONLINE] {daemon_name} activo.", flush=True)
    init_db()
    url = RSS_MAP.get(daemon_name)
    if url:
        headlines = fetch_rss_headlines(url)
        for hl in headlines:
            inject_headline(daemon_name, hl)

if __name__ == "__main__":
    daemon_name = sys.argv[1] if len(sys.argv) > 1 else "REUTERS_TOP"
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    run_daemon(daemon_name, query)
