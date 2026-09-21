import os, time, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

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

def inject_headline(source, headline):
    if not headline or len(headline) < 10:
        return
    md5 = hashlib.md5(headline.encode('utf-8')).hexdigest()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(DB_PATH, timeout=20.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (timestamp, daemon_source, headline, md5_hash, status)
            VALUES (?, ?, ?, ?, 'PENDING')
        """, (ts, source, headline, md5))
        conn.commit()
        conn.close()
        print(f"📥 [CAPTURADO]: {headline[:50]}...", flush=True)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"❌ Error DB: {e}", flush=True)

# Titulares extraídos directamente de la captura de Refinitiv Front Page
FRONT_PAGE_NEWS = [
    ("GEOPOLITICS_DEFENSE", "Flames, smoke seen near Riyadh airport; Houthis claim attacks on Saudi capital"),
    ("TECH_AI_CAPEX", "Ten days that changed the course of AI"),
    ("GEOPOLITICS_DEFENSE", "White House turns away CNN, MS NOW, Politico reporters after Trump's ban"),
    ("GEOPOLITICS_DEFENSE", "Greenland, Denmark say Trump deal won't compromise sovereignty"),
    ("GEOPOLITICS_DEFENSE", "Defence firm Anduril says US delay on Taiwan arms sales affecting its business"),
    ("GLOBAL_MACRO_FED", "China keeps benchmark lending rates unchanged for 14th month in September"),
    ("VENEZUELA_DESK", "Venezuela leader Rodriguez signs agreement with French Oil Company TotalEnergies"),
    ("GEOPOLITICS_DEFENSE", "US says it killed four in strike on vessel in the Caribbean"),
    ("GEOPOLITICS_DEFENSE", "Israeli strikes kill three people in Gaza, medics say"),
    ("MARKET_QUANT", "Democrats try to ride data center backlash to election victory in rural US Midwest"),
    ("TECH_AI_CAPEX", "China investigates Meituan and Alibaba units for suspected antitrust violations"),
    ("GLOBAL_MACRO_FED", "IMF tells EU ministers AI could boost growth but increase economic strains"),
    ("TECH_AI_CAPEX", "US judge signals rejection of part of TikTok privacy settlement")
]

if __name__ == "__main__":
    init_db()
    print("🚀 Inyectando nueva ráfaga de Refinitiv Front Page...", flush=True)
    
    for src, title in FRONT_PAGE_NEWS:
        inject_headline(src, title)

    print("✅ Ráfaga inyectada en la cola PENDING.")
