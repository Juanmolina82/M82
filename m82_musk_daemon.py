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
    print(f"[{timestamp}] [MUSK-INC] {msg}", flush=True)

def insert_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM m82_multi_stream WHERE headline = ?", (headline,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, ("MUSK_INC", headline))
            conn.commit()
            log(f"✅ Noticia ingresada: {headline[:60]}...")
        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def fetch_musk_updates():
    rss_urls = [
        "https://news.google.com/rss/search?q=SpaceX+OR+Tesla+OR+Starlink+OR+xAI+OR+Neuralink+when:1d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=Elon+Musk+Boring+Company+when:1d&hl=en-US&gl=US&ceid=US:en"
    ]
    for url in rss_urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    insert_headline(title.strip())
        except Exception as e:
            log(f"⚠️ Error escaneando feed: {e}")

def main():
    init_db()
    log("🚀 Daemon Musk Inc / SpaceX / Tesla / xAI activado.")
    while True:
        fetch_musk_updates()
        time.sleep(120)

if __name__ == "__main__":
    main()
