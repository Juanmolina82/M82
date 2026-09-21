import os, time, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
DAEMON_NAME = "WORLD_NEWS"

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

def inject_headline(headline):
    if not headline:
        return
    md5 = hashlib.md5(headline.encode('utf-8')).hexdigest()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(DB_PATH, timeout=20.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, md5_hash, status)
            VALUES (?, ?, ?, ?, 'PENDING')
        """, (ts, DAEMON_NAME, headline, md5))
        conn.commit()
        conn.close()
        print(f"📥 [{DAEMON_NAME}] Inyectado: {headline[:50]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ Error DB: {e}", flush=True)

# Titulares capturados directamente de la vista World News de Refinitiv
WORLD_HEADLINES = [
    "CHINA'S CXMT SAYS NEW MEMORY CHIP PLATFORM ENTERS MASS PRODUCTION",
    "RUSSIAN ELECTION: CAST AS TEST OF SUPPORT FOR UKRAINE WAR, ENTERS FINAL DAY",
    "MERZ UNDER PRESSURE AS TWO MORE GERMAN STATES GO TO THE POLLS",
    "GLOBAL MARKETS-Global stocks edge higher as dollar bides its time ahead of inflation data",
    "Trump used to hate China. Here's why he's now hiring out his tax expertise for it",
    "Brazil's setter economy braces for European sanctions"
]

if __name__ == "__main__":
    init_db()
    print(f"🚀 Daemon {DAEMON_NAME} ONLINE...", flush=True)
    
    # Inyección inmediata de titulares visibles
    for h in WORLD_HEADLINES:
        inject_headline(h)
