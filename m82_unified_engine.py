#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, textwrap, random, math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NFT_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

FEEDS = [
    ("VENEZUELA_DESK", "https://news.google.com/rss/search?q=Citgo+OR+OFAC+OR+Chevron+Venezuela"),
    ("REUTERS_BREAKING", "https://news.google.com/rss/search?q=site:reuters.com+breaking"),
    ("GLOBAL_MACRO", "https://news.google.com/rss/search?q=Federal+Reserve+OR+Crude+Oil"),
    ("COMMODITIES_ENERGY", "https://news.google.com/rss/search?q=oil+energy+diesel+record")
]

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
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

def scan_and_dispatch():
    init_db()
    for source, url in FEEDS:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:2]:
                    title = item.find('title').text.rsplit(" - ", 1)[0].strip()
                    
                    conn = sqlite3.connect(DB_PATH, timeout=30.0)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PROCESSED')", (source, title))
                        conn.commit()
                        
                        # Alerta ntfy
                        requests.post(NFT_URL, data=title.encode('utf-8'), headers={"Title": f"M82 [{source}]", "Priority": "high"}, timeout=5)
                        print(f"⚡ [M82 LIVE] {source} -> {title[:50]}...", flush=True)
                    except sqlite3.IntegrityError:
                        pass
                    conn.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    print("🚀 Motor Unificado M82 Iniciado (Ultra-ligero / Sin Signal 9)")
    while True:
        scan_and_dispatch()
        time.sleep(120)
