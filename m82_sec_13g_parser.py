import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def procesar_filings_13g():
    try:
        conn = sqlite3.connect("m82_database.db")
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS m82_sec_13g_filings (
            filing_id TEXT PRIMARY KEY,
            issuer_name TEXT,
            reporting_person TEXT,
            shares_beneficially_owned INTEGER,
            percent_of_class REAL,
            sole_voting_power INTEGER,
            sole_dispositive_power INTEGER,
            filing_date TEXT
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
            ovx REAL,
            ltv_spot REAL,
            nav_spot REAL
        )''')

        filings = [
            ('13G_LIBERTY_2026', 'Liberty Media Corp', 'Vanguard Capital Management, LLC', 1223250, 5.11, 178411, 1223250, '09/07/2026'),
            ('13G_ZIONS_2026', 'ZIONS BANCORPORATION, NATIONAL ASSOCIATION /UT', 'Vanguard Capital Management, LLC', 7737521, 5.23, 1137531, 7737521, '09/07/2026')
        ]

        c.executemany("INSERT OR REPLACE INTO m82_sec_13g_filings VALUES (?,?,?,?,?,?,?,?)", filings)
        
        c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
        snap = c.fetchone()
        if not snap:
            snap = (32.50, 18.51, 810.46)

        conn.commit()
        conn.close()

        fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

        mensaje = f"""📜 *M82 SEC SCHEDULE 13G FEED (REFINITIV)*
👤 *Reporting Person:* Vanguard Capital Management, LLC
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *1. LIBERTY MEDIA CORP (Common Stock)*
• *Acciones Poseídas:* `1,223,250`
• *Porcentaje de Clase:* `5.11%` (Participación Mayoritaria >5%)
• *Sole Voting Power:* `178,411`
• *Sole Dispositive Power:* `1,223,250`

📌 *2. ZIONS BANCORPORATION, N.A. (ZION)*
• *Acciones Poseídas:* `7,737,521`
• *Porcentaje de Clase:* `5.23%` (Participación Mayoritaria >5%)
• *Sole Voting Power:* `1,137,531`
• *Sole Dispositive Power:* `7,737,521`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛 *ESTADO DE RIESGO M82*
• *NAV Spot:* `${snap[2]}M USD`
• *LTV Spot:* `{snap[1]}%` | *OVX:* `{snap[0]}%`
"""

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
        if res.status_code == 200:
            print("✅ Registros Schedule 13G de SEC procesados y enviados a Telegram.")
        else:
            print(f"Error en envio a Telegram: {res.text}")

    except Exception as e:
        print(f"Error en procesador SEC 13G: {e}")

if __name__ == "__main__":
    procesar_filings_13g()
