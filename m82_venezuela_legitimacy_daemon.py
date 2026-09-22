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
    print(f"[{timestamp}] [VE-LEGITIMACY] {msg}", flush=True)

def insert_headline(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Señal capturada: {headline[:65]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

VENEZUELA_FEEDS = {
    "CITGO_OFAC_DESK": "https://news.google.com/rss/search?q=(%22CITGO%22+OR+%22OFAC+license%22+OR+%22PDVSA+2020%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "VE_OIL_LEGAL": "https://news.google.com/rss/search?q=(%22Venezuela+oil%22+OR+%22Chevron+Venezuela%22+OR+%22Delcy+Rodriguez%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "VENEZUELA_BONDS": "https://news.google.com/rss/search?q=(%22Venezuela+bonds%22+OR+%22PDVSA+bonds%22+OR+%22EMBI+Venezuela%22)+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def scan_venezuela_signals():
    for source, url in VENEZUELA_FEEDS.items():
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
    log("🇻🇪 Daemon de Legitimidad, Citgo y Riesgo Soberano de Venezuela Activo.")
    
    # Inyectar la señal clave del análisis
    key_signal = "VE_LEGITIMACY_GAP: Oil price up on Hormuz but Nabep/Delcy lacks rule-of-law -> No major IOC entry -> License bridge to Nov 5"
    insert_headline("VE_SOVEREIGN_RISK", key_signal)

    while True:
        scan_venezuela_signals()
        time.sleep(180)

if __name__ == "__main__":
    main()
