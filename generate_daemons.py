import os

DAEMONS = [
    ("m82_lseg_green_economy_daemon.py", "LSEG_GREEN_ECONOMY", "Green Economy Mark OR LSEG GRCS OR FTSE EOAS"),
    ("m82_unga_summit_tracker_daemon.py", "UNGA_NYC_TRACKER", "UNGA OR Trump OR Zelenskyy OR Hormuz"),
    ("m82_refinitiv_global_chain_daemon.py", "REFINITIV_GLOBAL_CHAIN", "ADR OR GDR OR cross-listing arbitrage"),
    ("m82_refinitiv_venues_charts_daemon.py", "REFINITIV_VENUES", "dark pool OR off-exchange volume"),
    ("m82_reuters_breakingviews.py", "REUTERS_BREAKINGVIEWS", "Reuters breakingviews OR M&A deal"),
    ("m82_macro_daemon.py", "MACRO_GLOBAL", "Federal Reserve OR ECB OR Interest Rates"),
    ("m82_delcy_osint_daemon.py", "DELCY_OSINT", "N818CA OR Helistar OR Bank of Utah Trustee"),
    ("m82_stress_score.py", "DAILY_ALPHA_STRESS", "SPY stress OR dark pool distribution")
]

template = """#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{tag}] {{msg}}", flush=True)

def insert_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        ''', ('{tag}', headline))
        conn.commit()
        log(f"✅ Señal Capturada: {{headline[:60]}}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error DB: {{e}}")

def scan():
    url = f"https://news.google.com/rss/search?q={query_str}&hl=en-US&gl=US&ceid=US:en"
    try:
        r = requests.get(url, headers={{'User-Agent': 'Mozilla/5.0'}}, timeout=10)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                insert_headline(title.strip())
    except Exception as e:
        log(f"⚠️ Error escaneando feed: {{e}}")

def main():
    init_db()
    log("📡 Daemon en ejecución continua...")
    while True:
        scan()
        time.sleep(180)

if __name__ == "__main__":
    main()
"""

for filename, tag, query in DAEMONS:
    filepath = os.path.expanduser(f"~/M82/{filename}")
    if not os.path.exists(filepath):
        query_formatted = query.replace(" ", "+")
        content = template.format(tag=tag, query_str=query_formatted)
        with open(filepath, "w") as f:
            f.write(content)
        os.chmod(filepath, 0o755)

print("✅ Todos los Daemons M82 han sido estructurados e inicializados.")
