import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# RSS especializado con términos de búsqueda estrictos sobre Donald Trump y Mercados
TRUMP_RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=(%22Donald+Trump%22+OR+%22Trump+administration%22+OR+%22Trump+tariffs%22+"
    "OR+%22Trump+policy%22+OR+%22Trump+Xi+summit%22)+when:1d"
    "&hl=en-US&gl=US&ceid=US:en"
)

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
            ('TRUMP_NEWSROOM', headline)
        )
        conn.commit()
        conn.close()
        print(f"⚡ [TRUMP_NEWSROOM] Inyectado -> {headline[:65]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ DB Error: {e}", flush=True)

def fetch_rss():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = requests.get(TRUMP_RSS_URL, headers=headers, timeout=12)
        root = ET.fromstring(req.content)
        items = root.findall('.//item/title')
        return [item.text.rsplit(' - ', 1)[0] for item in items if item.text]
    except Exception as e:
        print(f"⚠️ Error al conectar con el RSS: {e}", flush=True)
        return []

def run():
    print("🚀 [DAEMON ONLINE] TRUMP_NEWSROOM - Escaneando titulares...", flush=True)
    init_db()
    headlines = fetch_rss()
    count = 0
    for hl in headlines:
        inject_headline(hl)
        count += 1
    print(f"✅ Proceso finalizado. Total titulares procesados: {count}", flush=True)

if __name__ == "__main__":
    run()
