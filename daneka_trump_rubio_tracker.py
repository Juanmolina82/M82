#!/usr/bin/env python3
import sqlite3, time, os, datetime, requests
DB = os.path.expanduser("~/M82/db/m82_database.db")

def push_card(source, headline, alpha, tag):
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA journal_mode=WAL;")
    cur = conn.cursor()
    cur.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES (?,?,?,?,?,?)",
    (source, headline, "LIVE", alpha, "TRUMP_RUBIO_MCM", tag))
    conn.commit()
    conn.close()
    print(f"[{datetime.datetime.now()}] DANEKA PUSH {source} → {headline}")

# Loop cada 60s
while True:
    # Aquí va tu LSEG websocket — por ahora polling mock para trigger
    brent = 114.72 # reemplazar por LSEG feed real
    if brent > 115:
        push_card("REFINITIVOILDESK", f"Brent ${brent} 5M high — Merey $93.92 — off-Hormuz hedge", 0.92, "BRENT_THRESHOLD")
    
    # Trump / Rubio — scrape Reuters / State Dept
    push_card("TRUMP_RUBIO_DESK", "[TRACKING] Trump Gold Deal $150M Minerven/Trafigura — Rubio eval Qatar bridge $2BN — Iran threat active", 0.99, "TRUMP_RUBIO_STEP")
    
    time.sleep(60)
