import sqlite3
import requests
from datetime import datetime
import os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def ingest_copper_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Tabla de Métricas de Metales Base (LME / SHFE / COMEX)
    c.execute('''CREATE TABLE IF NOT EXISTS m82_metals_metrics (
        ric TEXT PRIMARY KEY,
        metal_name TEXT,
        lme_3m_price REAL,
        all_time_high REAL,
        shfe_price REAL,
        price_target TEXT,
        last_updated TEXT
    )''')

    metals_data = (
        'CMCU3',
        'LME 3-Month Copper',
        10230.00,
        10779.00,
        72270.00,
        '$11,000 USD/MT',
        '09-Sep-2026'
    )
    c.execute("INSERT OR REPLACE INTO m82_metals_metrics VALUES (?,?,?,?,?,?,?)", metals_data)

    # 2. Registro del Feed de Noticias LSEG / Reuters
    c.execute('''CREATE TABLE IF NOT EXISTS m82_market_news (
        news_id TEXT PRIMARY KEY,
        headline TEXT,
        source TEXT,
        asset_class TEXT,
        key_takeaways TEXT,
        timestamp TEXT
    )''')

    news_entry = (
        'REUTERS_COPPER_20260909',
        'Copper hovers below record high as non-US supply tightness remains in focus',
        'Reuters / Refinitiv Workspace',
        'Base Metals',
        'Restricciones de oferta fuera de EE.UU. por aranceles a cobre refinado; StoneX prevé $11,000/t a corto plazo; SHFE inventarios en 72,270 t.',
        '09-Sep-2026 00:06 VET'
    )
    c.execute("INSERT OR REPLACE INTO m82_market_news VALUES (?,?,?,?,?,?)", news_entry)

    conn.commit()

    # 3. Consulta Snapshot Patrimonial
    try:
        c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
        snap = c.fetchone()
    except Exception:
        snap = (32.5, 18.51, 810.46)

    conn.close()

    # 4. Construcción y Transmisión de Payload
    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *INGESTA COMMODITIES: COBRE BASE (`CMCU3`)*
• *Titular Reuters:* _Copper hovers below record high as non-US supply tightness remains in focus_
• *LME 3-Month (`CMCU3`):* `$10,230.00 USD/MT`
• *Récord Histórico Reciente:* `$10,779.00 USD/MT` (Martes 08-Sep)
• *Shanghai Futures (`SCFcv1`):* `72,270 Yuan/MT`
• *Target Analistas (StoneX):* `$11,000 USD/MT`
• *Catalizador:* Restricción de oferta fuera de EE.UU. por aranceles a importación de cobre refinado.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡 *MONITOR DE RIESGO Y PATRIMONIO*
• *NAV Spot:* `${snap[2]}M USD`
• *LTV Spot:* `{snap[1]}%` (Umbral máximo: 19.0%)
• *Índice OVX:* `{snap[0]}%`
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": mensaje,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }, timeout=8)
        if res.status_code == 200:
            print("✅ Ingesta de Cobre registrada en DB y notificada a Telegram.")
        else:
            print(f"⚠️ Registro en DB correcto. Telegram status: {res.status_code}")
    except Exception as e:
        print(f"⚠️ Registro en DB correcto. Conexión diferida: {e}")

if __name__ == "__main__":
    ingest_copper_data()
