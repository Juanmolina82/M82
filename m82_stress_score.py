#!/usr/bin/env python3
import os, sys, time, sqlite3, urllib.parse, xml.etree.ElementTree as ET
import requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

def compute_stress_score():
    base_score = 5.0
    factors = []

    scenarios = [
        {"name": "Dark Pool & Inst Selling", "query": "SPY dark pool distribution institutional selling", "weight": 1.5},
        {"name": "Germany/AfD Escalation", "query": "Germany AfD election market risk", "weight": 1.0},
        {"name": "APAC Missile / Geopolitics", "query": "North Korea ballistic missile launch", "weight": 1.2},
        {"name": "Macro Risk / Yields Spike", "query": "Federal Reserve inflation yields risk", "weight": 1.0}
    ]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

    for item in scenarios:
        encoded = urllib.parse.quote(item["query"])
        url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                items = root.findall('.//item')
                count = len(items)
                if count > 0:
                    added = min(item["weight"], round(count * 0.3, 1))
                    base_score += added
                    factors.append(f"{item['name']} (+{added})")
        except Exception as e:
            print(f"⚠️ Error escaneando {item['name']}: {e}", flush=True)

    final_score = min(round(base_score, 1), 10.0)
    if not factors:
        factors.append("Baseline Macro Volatility")
    return final_score, factors

def inject_signal():
    init_db()
    score, factors = compute_stress_score()
    triggers_str = ", ".join(factors)
    headline = f"SPY Stress {score}/10 - Institutional Distribution Confirmed | Triggers: {triggers_str}"
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)",
            ('DAILY_ALPHA_STRESS', headline)
        )
        conn.commit()
        conn.close()
        print(f"✅ [STRESS SCORE] Generado e inyectado a DB M82:\n{headline}", flush=True)
    except sqlite3.IntegrityError:
        print("⚠️ Esta lectura de estrés ya fue registrada previamente en la BD.", flush=True)
    except Exception as e:
        print(f"❌ Error en DB: {e}", flush=True)

if __name__ == "__main__":
    inject_signal()
