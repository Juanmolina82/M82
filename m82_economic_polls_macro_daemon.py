#!/usr/bin/env python3
import os, time, sqlite3, requests, xml.etree.ElementTree as ET
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
FEEDS = {"ECONOMIC_POLLS_MACRO": "https://news.google.com/rss/search?q=%22economic+forecast%22+OR+%22money+market+yields%22+when:1d&hl=en-US&gl=US&ceid=US:en"}
def insert(src, hdl):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM m82_multi_stream WHERE headline = ?", (hdl,))
        if not c.fetchone():
            c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING')", (src, hdl))
            conn.commit()
        conn.close()
    except Exception: pass
def main():
    while True:
        for src, url in FEEDS.items():
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    for item in ET.fromstring(r.content).findall('.//item')[:2]:
                        t = item.find('title').text.rsplit(" - ", 1)[0].strip()
                        insert(src, t)
            except Exception: pass
        time.sleep(120)
if __name__ == "__main__": main()
