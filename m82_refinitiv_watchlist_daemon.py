#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Watchlist M82 dentro de Refinitiv Workspace
M82_WATCHLIST = [
    {"ticker": "UBSG.S", "name": "UBS Group AG", "asset": "EQUITY"},
    {"ticker": "SOGN.PA", "name": "Societe Generale SA", "asset": "EQUITY"},
    {"ticker": "9984.T", "name": "SoftBank Group Corp", "asset": "EQUITY"},
    {"ticker": "AAPL.O", "name": "Apple Inc", "asset": "EQUITY"},
    {"ticker": "BABA.N", "name": "Alibaba Group Holding", "asset": "EQUITY"},
    {"ticker": "CL=F", "name": "Crude Oil WTI Futures", "asset": "COMMODITY"},
    {"ticker": "LCOc1", "name": "Brent Crude Oil", "asset": "COMMODITY"}
]

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [REFINITIV-WATCHLIST] {msg}", flush=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_watchlist_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            name TEXT,
            asset_type TEXT,
            last_price REAL,
            change_pct REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def sync_refinitiv_watchlist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for item in M82_WATCHLIST:
        ticker = item["ticker"]
        name = item["name"]
        asset = item["asset"]
        
        # Simulación de lectura de variaciones desde Refinitiv Workspace
        change_pct = round(random.uniform(-3.5, 3.5), 2)
        price = round(random.uniform(20.0, 350.0), 2)
        
        cursor.execute("""
            INSERT INTO m82_watchlist_quotes (ticker, name, asset_type, last_price, change_pct, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(ticker) DO UPDATE SET
                last_price=excluded.last_price,
                change_pct=excluded.change_pct,
                updated_at=CURRENT_TIMESTAMP
        """, (ticker, name, asset, price, change_pct))
        
        # Inyectar alerta al Stream M82 si la variación supera el 2.5%
        if abs(change_pct) >= 2.5:
            direction = "🟢 UP" if change_pct > 0 else "🔴 DOWN"
            headline = f"REFINITIV WATCHLIST ALERT | {ticker} ({name}) {direction} {change_pct}% | Price: ${price}"
            
            cursor.execute("""
                INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, ("REFINITIV_WATCHLIST", headline))
            log(f"⚡ Alerta inyectada a Stream: {ticker} ({change_pct}%)")
            
    conn.commit()
    conn.close()

def main():
    init_db()
    log("📡 Daemon M82 Refinitiv Watchlist sincronizado.")
    while True:
        sync_refinitiv_watchlist()
        time.sleep(180) # Revisa variaciones de precios cada 3 minutos

if __name__ == "__main__":
    main()
