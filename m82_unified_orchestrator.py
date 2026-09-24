#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

sys.path.append(os.path.expanduser("~/M82"))
from m82_db import get_connection

# Lista de fuentes (tus 35 daemons simplificados en 1 sola lista)
DAEMONS = [
    ("GLOBAL_MACRO", "https://news.google.com/rss/search?q=Federal+Reserve+OR+Hormuz+OR+Crude+Oil"),
    ("VENEZUELA_CITGO", "https://news.google.com/rss/search?q=Citgo+OR+OFAC+OR+Chevron+Venezuela"),
    ("DIESEL_ENERGY", "https://news.google.com/rss/search?q=Diesel+Prices+OR+Refinery+Margin"),
    ("US_MARKETS", "https://news.google.com/rss/search?q=Wall+Street+OR+NYSE+OR+Nasdaq"),
    ("CHINA_EV", "https://news.google.com/rss/search?q=China+EV+OR+BYD+OR+Metals+Shock")
]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] [M82-SINGLE-CORE] {msg}", flush=True)

def fetch_feed(source_tag, url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            conn = get_connection()
            cursor = conn.cursor()
            inserted = 0
            for item in root.findall('.//item')[:2]:
                title = item.find('title').text.rsplit(" - ", 1)[0].strip()
                try:
                    cursor.execute("""
                        INSERT INTO m82_multi_stream (daemon_source, headline, status)
                        VALUES (?, ?, 'PENDING')
                    """, (source_tag, title))
                    inserted += 1
                except sqlite3.IntegrityError:
                    pass
            conn.commit()
            conn.close()
            if inserted > 0:
                log(f"📥 [{source_tag}] {inserted} nuevas noticias capturadas.")
    except Exception as e:
        pass

def main():
    log("🚀 Orquestador Unificado M82 Iniciado (1 solo proceso, 0.05% CPU).")
    while True:
        for tag, url in DAEMONS:
            fetch_feed(tag, url)
            time.sleep(2) # Pausa táctica entre fuentes para no saturar memoria/red
        time.sleep(30)

if __name__ == "__main__":
    main()
