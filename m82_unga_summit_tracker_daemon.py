#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

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
    print(f"[{timestamp}] [UNGA-SUMMIT-TRACKER] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Señal inyectada: {headline[:65]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

UNGA_FEEDS = {
    "UNGA_TRUMP_SPEECH": "https://news.google.com/rss/search?q=(%22Trump%22+AND+%22UNGA%22+OR+%22United+Nations+General+Assembly%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "UNGA_BILATERALS": "https://news.google.com/rss/search?q=(%22Trump%22+AND+(%22Zelenskyy%22+OR+%22UK+Prime+Minister%22+OR+%22Japan%22+OR+%22Greenland%22))+when:1d&hl=en-US&gl=US&ceid=US:en",
    "UNGA_AMERICAS_GCC": "https://news.google.com/rss/search?q=(%22Shield of the Americas%22+OR+%22Gulf Cooperation Council%22+OR+%22Venezuela%22)+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def scan_unga_signals():
    for source, url in UNGA_FEEDS.items():
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

UNGA_SCHEDULE_SIGNALS = [
    ("UNGA_SPEECH_0955", "UNGA_09:55_EST: Pres. Trump addresses UN General Assembly -> Key focus on global trade, Hormuz & energy security"),
    ("UNGA_DENMARK_GREENLAND", "UNGA_10:40_EST: Trilateral signing with Denmark & Greenland Prime Ministers -> Arctic strategic security & minerals"),
    ("UNGA_UK_JAPAN_BILATS", "UNGA_11:45_EST: UK & Japan Bilaterals -> Post-tariff trade agreements & Indo-Pacific defense axis"),
    ("UNGA_UKRAINE_1315", "UNGA_13:15_EST: Trump - Zelenskyy Bilateral -> Peace framework conditions & military aid pipeline"),
    ("UNGA_AMERICAS_SHIELD", "UNGA_14:15_EST: Shield of the Americas Summit -> Regional security, cartel interception & supply chain resilience"),
    ("UNGA_GCC_1445", "UNGA_14:45_EST: Multilateral with Gulf Cooperation Council -> Hormuz strait crisis, oil production quotas & Middle East stability"),
    ("UNGA_VE_PULLASIDE_1940", "UNGA_19:40_EST: Informal Pull-aside with Venezuela Leadership -> Citgo license bridge, rule-of-law transition & oil export caps")
]

def main():
    init_db()
    log("🏛️ Daemon de Monitoreo de la Cumbre UNGA Nueva York & Geopolítica Global Activo.")
    
    for source, signal in UNGA_SCHEDULE_SIGNALS:
        insert_headline(source, signal)

    while True:
        scan_unga_signals()
        time.sleep(180)

if __name__ == "__main__":
    main()
