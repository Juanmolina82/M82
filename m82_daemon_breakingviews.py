import time
import os
import sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
DAEMON_NAME = "BREAKINGVIEWS"
QUERY = "Topic:BREAKINGVIEWS OR Topic:VIEWS OR Topic:COLUMN"

def inject_headline(source, headline):
    if not headline:
        return
    try:
        conn = sqlite3.connect(DB_PATH, timeout=20.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING');",
            (source, headline)
        )
        conn.commit()
        conn.close()
        print(f"📥 [{source}] Inyectado: {headline[:60]}...", flush=True)
    except sqlite3.IntegrityError:
        pass # Duplicado ignorado
    except Exception as e:
        print(f"❌ Error DB en {source}: {e}", flush=True)

def run_daemon():
    print(f"🚀 Daemon {DAEMON_NAME} ONLINE (Query: {QUERY})...", flush=True)
    use_refinitiv = False
    
    try:
        import lseg.data as ld
        ld.open_session()
        use_refinitiv = True
    except Exception:
        use_refinitiv = False

    while True:
        try:
            if use_refinitiv:
                import lseg.data as ld
                headlines_df = ld.news.get_headlines(query=QUERY, count=10)
                if headlines_df is not None and not headlines_df.empty:
                    col = 'headline' if 'headline' in headlines_df.columns else headlines_df.columns[0]
                    for title in headlines_df[col]:
                        inject_headline(DAEMON_NAME, str(title))
            else:
                # Vía RSS Backup en caso de estar fuera de sesión
                import xml.etree.ElementTree as ET
                import requests
                rss_url = "https://news.google.com/rss/search?q=Reuters+Breakingviews&hl=en-US&gl=US&ceid=US:en"
                res = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                root = ET.fromstring(res.content)
                for item in root.findall('.//item/title')[:5]:
                    title_text = item.text.rsplit(' - ', 1)[0]
                    inject_headline(DAEMON_NAME, title_text)
        except Exception as e:
            print(f"⚠️ Exception en {DAEMON_NAME}: {e}", flush=True)

        time.sleep(120) # Consulta cada 2 minutos para no saturar Refinitiv

if __name__ == "__main__":
    run_daemon()
