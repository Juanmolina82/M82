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
    print(f"[{timestamp}] [MONEY-MARKETS-POLLS] {msg}", flush=True)

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
            log(f"✅ [{source}] Alerta Money Markets/Polls Detectada: {headline[:60]}...")
        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

# Feeds de noticias e inteligencia sobre encuestas de mercado monetario y expectativas de tasas
MONEY_POLLS_FEEDS = {
    "REUTERS_MONEY_MARKET_POLLS": "https://news.google.com/rss/search?q=%22money+market+poll%22+OR+%22interest+rate+poll%22+Reuters+when:1d&hl=en-US&gl=US&ceid=US:en",
    "FED_EXPECTATIONS_SOFR": "https://news.google.com/rss/search?q=%22SOFR%22+OR+%22Treasury+bills%22+OR+%22Fed+rate+cut+forecast%22+when:1d&hl=en-US&gl=US&ceid=US:en",
    "BOND_YIELD_POLLS": "https://news.google.com/rss/search?q=%22bond+yield+poll%22+OR+%22Treasury+yield+forecast%22+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def fetch_money_market_polls():
    for source, url in MONEY_POLLS_FEEDS.items():
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:4]:
                    title = item.find('title').text
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    insert_headline(source, title.strip())
        except Exception as e:
            log(f"⚠️ Error escaneando feed {source}: {e}")

def main():
    init_db()
    log("🏛 Daemon Money Markets & Bond Yield Polls (Refinitiv Analytics) Activo.")
    while True:
        fetch_money_market_polls()
        time.sleep(120)

if __name__ == "__main__":
    main()
