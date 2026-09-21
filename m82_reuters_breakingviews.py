import os, sys, time, sqlite3, urllib.parse
import feedparser

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

QUERIES = [
    'site:reuters.com/breakingviews when:2d',
    '(Diesel OR "Deutsche Telekom" OR Cosco OR Tata OR "Bank of England") when:2d'
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
            ('REUTERS_BREAKINGVIEWS', headline)
        )
        conn.commit()
        conn.close()
        print(f"⚡ [BREAKINGVIEWS] Inyectado -> {headline[:65]}...", flush=True)
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
        for entry in feed.entries:
            title = entry.title.rsplit(' - ', 1)[0]
            headlines.append(title)
        return headlines
    except Exception as e:
        print(f"⚠️ Error procesando RSS: {e}", flush=True)
        return []

def run():
    print("🚀 [DAEMON ONLINE] REUTERS_BREAKINGVIEWS - Extrayendo análisis...", flush=True)
    init_db()
    total = 0
    for q in QUERIES:
        headlines = fetch_rss(q)
        for hl in headlines:
            inject_headline(hl)
            total += 1
    print(f"✅ Inserción finalizada. Total artículos procesados: {total}", flush=True)

if __name__ == "__main__":
    run()
