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
    print(f"[{timestamp}] [GLOBAL-CHAIN-ARBITRAGE] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Evento Arbitraje/Chain: {headline[:60]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

CHAIN_FEEDS = {
    "CROSS_MARKET_ARBITRAGE": "https://news.google.com/rss/search?q=%22ADR%22+OR+%22GDR%22+OR+%22cross-listing%22+arbitrage+when:1d&hl=en-US&gl=US&ceid=US:en",
    "GLOBAL_TICKER_CHAIN": "https://news.google.com/rss/search?q=%22JPMorgan%22+OR+%22dual-listing%22+volume+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def fetch_chain_updates():
    for source, url in CHAIN_FEEDS.items():
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
    log("🌐 Daemon Refinitiv Global Chain & Cross-Market Arbitrage Activo.")
    while True:
        fetch_chain_updates()
        time.sleep(120)

if __name__ == "__main__":
    main()
