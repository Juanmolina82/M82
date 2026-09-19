import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def registrar_tickers():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Crear tabla para seguimiento de Tickers
    c.execute('''CREATE TABLE IF NOT EXISTS m82_tracked_tickers (
        ticker TEXT PRIMARY KEY,
        exchange TEXT,
        asset_name TEXT,
        date_added TEXT
    )''')

    # 2. Inserción de los tickers enviados
    tickers_data = [
        ('VCX.AX', 'ASX', 'Vicinity Centres', datetime.now().strftime("%Y-%m-%d")),
        ('SCG.AX', 'ASX', 'Scentre Group', datetime.now().strftime("%Y-%m-%d")),
        ('C.N', 'NYSE', 'Citigroup Inc.', datetime.now().strftime("%Y-%m-%d"))
    ]

    c.executemany("INSERT OR REPLACE INTO m82_tracked_tickers VALUES (?,?,?,?)", tickers_data)

    # 3. Leer métricas de Snapshot
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Plantilla Blindada para Telegram
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *INGESTA DE TICKERS: SEGUIMIENTO INSTRUMENTAL*
• *VCX.AX:* Vicinity Centres (ASX - Australia)
• *SCG.AX:* Scentre Group (ASX - Australia)
• *C.N:* Citigroup Inc. (NYSE - EE. UU.)
• *Status Ingesta:* Tickers agregados a `m82_tracked_tickers`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡 *MONITOR DE RIESGO Y PATRIMONIO*
• *NAV Spot:* `${snap[2]}M USD`
• *LTV Spot:* `{snap[1]}%` (Umbral máximo: 19.0%)
• *Índice OVX:* `{snap[0]}%` (Umbral límite: 35.0%)
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": mensaje,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })
        return res.status_code == 200
    except Exception as e:
        print(f"Error de envío: {e}")
        return False

if __name__ == "__main__":
    if registrar_tickers():
        print("✅ Tickers registrados exitosamente y notificados a Telegram.")
