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
            headline TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [US-ME-ENERGY-FUND] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM m82_multi_stream WHERE headline = ?", (headline,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (source, headline))
            conn.commit()
            log(f"✅ [{source}] Evento Registrado: {headline[:60]}...")
        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

FUND_FEEDS = {
    "US_ME_ENERGY_FUND": "https://news.google.com/rss/search?q=%22Development+Finance+Corporation%22+OR+%22Partnership+for+Allied+Trust+and+Construction%22+OR+%22Middle+East+energy+fund%22+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def fetch_fund_news():
    for source, url in FUND_FEEDS.items():
        try:
            r = requests.get(url, timeout=10)
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
    log("🏛️ Daemon US $5B Middle East Energy Fund Wire Activo.")
    while True:
        fetch_fund_news()
        time.sleep(120)

if __name__ == "__main__":
    main()
