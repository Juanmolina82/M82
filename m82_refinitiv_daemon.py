import sqlite3, os, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
URL = "https://news.google.com/rss/search?q=site:reuters.com+OR+site:refinitiv.com&hl=en-US&gl=US&ceid=US:en"

def scan_refinitiv():
    try:
        r = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text.rsplit(" - ", 1)[0].strip()
                try:
                    cursor.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES ('REFINITIV_DESK', ?, 'PENDING')", (title,))
                except sqlite3.IntegrityError:
                    pass
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error Refinitiv: {e}")

if __name__ == "__main__":
    scan_refinitiv()
