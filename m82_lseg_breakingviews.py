import sqlite3
import os
import time
import requests
from xml.etree import ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

FEEDS = [
    "https://www.reutersagency.com/feed/?best-topics=breakingviews&post_type=best",
    "http://feeds.reuters.com/reuters/financialNews"
]

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            daemon_source TEXT,
            headline TEXT,
            md5_hash TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

def fetch_and_inject():
    init_db()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for url in FEEDS:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                continue

            root = ET.fromstring(res.content)
            conn = sqlite3.connect(DB_PATH, timeout=20.0)
            cursor = conn.cursor()

            for item in root.findall('.//item'):
                title_elem = item.find('title')
                if title_elem is not None and title_elem.text:
                    title = title_elem.text.strip()
                    
                    import hashlib
                    md5 = hashlib.md5(title.encode('utf-8')).hexdigest()
                    ts = time.strftime("%Y-%m-%d %H:%M:%S")

                    try:
                        cursor.execute("""
                            INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, md5_hash, status)
                            VALUES (?, 'REFINITIV_BREAKINGVIEWS', ?, ?, 'PENDING')
                        """, (ts, title, md5))
                        conn.commit()
                        print(f"📥 [LSEG CAPTURADO]: {title[:40]}...", flush=True)
                    except sqlite3.IntegrityError:
                        pass

            conn.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    print("🚀 Escaneo LSEG ultra-rápido (30s)...", flush=True)
    while True:
        fetch_and_inject()
        time.sleep(30)
