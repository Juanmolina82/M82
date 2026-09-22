import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# RSS con cobertura equivalente a Refinitiv Workspace (M&A, Fed, Energía, IA, Geopolítica)
REFINITIV_RSS_URLS = [
    "https://news.google.com/rss/search?q=(%22Paramount%22+OR+%22Warner+Bros%22+OR+%22OpenAI%22+OR+%22Potash%22+OR+%22LNG%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=(%22Goolsbee%22+OR+%22Bank+of+Canada%22+OR+%22Oil+Tankers%22+OR+%22Refineries%22)+when:1d&hl=en-US&gl=US&ceid=US:en"
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
            ('REFINITIV_DESK', headline)
        )
        conn.commit()
        conn.close()
        print(f"⚡ [REFINITIV_DESK] Inyectado -> {headline[:65]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ DB Error: {e}", flush=True)

def fetch_rss(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = requests.get(url, headers=headers, timeout=12)
        root = ET.fromstring(req.content)
        items = root.findall('.//item/title')
        return [item.text.rsplit(' - ', 1)[0] for item in items if item.text]
    except Exception as e:
        print(f"⚠️ Error cargando RSS: {e}", flush=True)
        return []

def run():
    print("🚀 [DAEMON ONLINE] REFINITIV_DESK - Extrayendo flujo corporativo y macro...", flush=True)
    init_db()
    total = 0
    for url in REFINITIV_RSS_URLS:
        headlines = fetch_rss(url)
        for hl in headlines:
            inject_headline(hl)
            total += 1
    print(f"✅ Inserción finalizada. Total noticias procesadas: {total}", flush=True)

if __name__ == "__main__":
    run()
