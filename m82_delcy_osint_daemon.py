#!/usr/bin/env python3
import os, sys, time, json, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TARGET_N = "N818CA"
ICAO_HEX = "A52623"
FORENSIC_DIR = os.path.expanduser(f"~/M82/forensic/{TARGET_N}")

os.makedirs(FORENSIC_DIR, exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [DELCY_OSINT] {msg}", flush=True)

def check_adsb_tracking():
    url = f"https://api.adsb.lol/v2/icao/{ICAO_HEX}"
    headers = {"User-Agent": "M82-OSINT-Daemon"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            ac_list = data.get("ac", [])
            if ac_list:
                ac = ac_list[0]
                flight = ac.get("flight", "N/A").strip()
                lat = ac.get("lat", 0.0)
                lon = ac.get("lon", 0.0)
                alt = ac.get("alt_baro", 0)
                
                log(f"📍 Detección Activa: {TARGET_N} | Flight: {flight} | Pos: {lat}, {lon} | Alt: {alt}ft")
                
                with open(os.path.join(FORENSIC_DIR, "live_trace.json"), "w") as f:
                    json.dump(ac, f, indent=2)
                
                headline = f"Delcy N818CA Tracker | Flight: {flight} | Alt: {alt}ft | Pos: {lat},{lon}"
                
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id FROM m82_multi_stream 
                    WHERE headline LIKE ? AND timestamp > datetime('now', '-30 minutes')
                """, (f"%{TARGET_N}%",))
                
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO m82_multi_stream (daemon_source, headline, status)
                        VALUES (?, ?, 'PENDING')
                    """, ("DELCY_OSINT", headline))
                    conn.commit()
                    log("✅ Señal OSINT inyectada en m82_multi_stream.")
                
                conn.close()
            else:
                log(f"Sin señal activa en tiempo real para {TARGET_N} (HEX: {ICAO_HEX}).")
    except Exception as e:
        log(f"Error consultando API ADS-B: {e}")

def main():
    log("Iniciando Demonio M82 OSINT - Tracking Delcy Rodríguez / N818CA...")
    while True:
        check_adsb_tracking()
        time.sleep(120)

if __name__ == "__main__":
    main()
