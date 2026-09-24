#!/usr/bin/env bash

echo "🛠️ Estabilizando infraestructura M82 para evitar reinicios de Termux..."

# 1. Asegurar Wake Lock
termux-wake-lock

# 2. Detener la masa de procesos paralelos que saturan la RAM
pkill -f "m82_" || true
sleep 2

# 3. Crear Ingestor Unificado y Eficiente (1 solo proceso en vez de 35)
cat << 'INGEST_EOF' > ~/M82/m82_unified_ingestor.py
#!/usr/bin/env python3
import os, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

TARGETS = [
    ("UNGA_NYC_TRACKER", "UNGA OR Trump OR Zelenskyy OR Hormuz"),
    ("REFINITIV_GLOBAL_CHAIN", "ADR OR GDR OR cross-listing arbitrage"),
    ("MACRO_GLOBAL", "Federal Reserve OR ECB OR Interest Rates"),
    ("CRYPTO_COMMODITIES", "Bitcoin OR Crude Oil OR Gold Futures"),
    ("MUSK_EMPIRE", "Tesla OR SpaceX OR xAI OR Starlink"),
    ("DEBT_CREDIT", "High Yield Bonds OR Credit Default Swaps"),
    ("VENEZUELA_LEGITIMACY", "Citgo Auction OR OFAC Sanctions OR Chevron Venezuela"),
    ("DELCY_OSINT", "N818CA OR Helistar OR Bank of Utah Trustee")
]

def insert_headline(tag, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        ''', (tag, headline))
        conn.commit()
        conn.close()
    except Exception:
        pass

def run_cycle():
    for tag, query in TARGETS:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:2]:
                    title = item.find('title').text.rsplit(" - ", 1)[0]
                    insert_headline(tag, title.strip())
        except Exception:
            pass
        time.sleep(2) # Pausa ligera para no saturar CPU

if __name__ == "__main__":
    while True:
        run_cycle()
        time.sleep(60) # Espera 1 minuto entre barridos completos
INGEST_EOF

# 4. Lanzar solo 2 procesos controlados (Ingestor + Orquestador)
nohup python3 -u ~/M82/m82_unified_ingestor.py > ~/M82/m82_ingestor.log 2>&1 &
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/M82/m82_orchestrator.log 2>&1 &

echo "✅ Infraestructura estabilizada. Termux operará sin colapsar."
