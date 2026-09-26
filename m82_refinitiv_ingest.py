#!/usr/bin/env python3
import os, sys, sqlite3

# Importación robusta para evitar ModuleNotFoundError
sys.path.append(os.path.expanduser("~/M82"))
from m82_db import get_connection

HEADLINES = [
    ("REFINITIV_MARKETS", "US MARKETS DOWN: NASDAQ leads losses down -1.13%, S&P 500 drops -0.75%"),
    ("REFINITIV_SECTORS", "SECTOR PERFORMANCE: Consumer Cyclicals (-0.97%) and Financials (-0.53%) drag Wall St"),
    ("REFINITIV_INDICES", "DOW JONES FLATS AT 31,818.84 (-0.17%) amid broad market weakness")
]

def push_headlines():
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    for source, hl in HEADLINES:
        try:
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (source, hl))
            count += 1
            print(f"📥 [INGESTED] -> {hl[:50]}...")
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    return count

if __name__ == "__main__":
    inserted = push_headlines()
    print(f"✅ Ingesta finalizada. {inserted} señales agregadas a la cola M82.")
