#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [VENUES-VOLUME-ANALYZER] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Alerta Venue / DarkPool: {headline[:60]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

VENUE_FEEDS = {
    "DARK_POOL_FLOWS": "https://news.google.com/rss/search?q=%22dark+pool%22+OR+%22off-exchange+volume%22+stocks+when:1d&hl=en-US&gl=US&ceid=US:en",
    "VENUE_VOLUME_SPIKES": "https://news.google.com/rss/search?q=%22volume+spike%22+OR+%22unusual+volume%22+NYSE+NASDAQ+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def fetch_venue_updates():
    for source, url in VENUE_FEEDS.items():
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    insert_headline(source, title.strip())
        except Exception as e:
            log(f"⚠️ Error escaneando feed {source}: {e}")

def main():
    init_db()
    log("📊 Daemon Refinitiv Venues, Dark Pools & Exchange Volume Spikes Activo.")
    while True:
        fetch_venue_updates()
        time.sleep(120)

if __name__ == "__main__":
    main()
