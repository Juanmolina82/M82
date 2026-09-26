#!/usr/bin/env python3
import sqlite3, os, time, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Feeds públicos y sindicados de LSEG / Reuters para consumo de bajo ancho de banda
FEEDS = [
    "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    "http://feeds.reuters.com/reuters/businessNews"
]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] [M82-LSEG] {msg}", flush=True)

def fetch_data():
    log("📡 Escaneando noticias financieras LSEG / Refinitiv...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        conn = sqlite3.connect(DB_PATH, timeout=15.0)
        cursor = conn.cursor()
        
        # Asegurar tabla de destino
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS m82_multi_stream (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daemon_source TEXT,
                unified_summary TEXT,
                status TEXT DEFAULT 'PENDING',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        count = 0
        for url in FEEDS:
            try:
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200:
                    root = ET.fromstring(r.content)
                    for item in root.findall('.//item')[:3]:
                        title = item.find('title')
                        if title is not None and title.text:
                            headline = title.text.strip()
                            
                            # Evitar duplicados recientes
                            cursor.execute(
                                "SELECT id FROM m82_multi_stream WHERE unified_summary = ? LIMIT 1", 
                                (headline,)
                            )
                            if not cursor.fetchone():
                                cursor.execute(
                                    "INSERT INTO m82_multi_stream (daemon_source, unified_summary, status) VALUES (?, ?, 'PENDING')",
                                    ("LSEG_NEWS_WSJ", headline)
                                )
                                count += 1
            except Exception:
                continue

        conn.commit()
        conn.close()
        if count > 0:
            log(f"✅ {count} nuevas noticias capturadas e ingresadas en cola PENDING.")
        else:
            log("ℹ️ Sin novedades relevantes en el ciclo actual.")

    except Exception as e:
        log(f"⚠️ Error en módulo LSEG: {e}")

if __name__ == "__main__":
    fetch_data()
