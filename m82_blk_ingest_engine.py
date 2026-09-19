import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def procesar_e_ingresar_blk():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Asegurar tablas necesarias
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS m82_blk_profile (
        ticker TEXT PRIMARY KEY,
        company_name TEXT,
        market_cap_m REAL,
        shares_outstanding_m REAL,
        employees INTEGER,
        next_earn_date TEXT,
        last_updated TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS m82_blk_metrics (
        ticker TEXT,
        period_end TEXT,
        enterprise_value_m REAL,
        ebitda_m REAL,
        pe_ratio REAL,
        div_yield REAL,
        return_on_equity REAL,
        PRIMARY KEY (ticker, period_end)
    )''')

    # 2. Ingesta de datos de la captura (Refinitiv Workspace)
    blk_general = ('BLK.N', 'BLACKROCK, INC.', 102148.06, 149.21, 19800, '13-Oct-2026', '07-Sep-2026')
    c.execute("INSERT OR REPLACE INTO m82_blk_profile VALUES (?, ?, ?, ?, ?, ?, ?)", blk_general)

    blk_metrics = [
        ('BLK.N', 'FY 2024', 113426.0, 7881.0, 19.33, 2.50, 14.90),
        ('BLK.N', 'FY 2025', 110904.0, 8312.0, 17.80, 2.70, 15.20)
    ]
    c.executemany("INSERT OR REPLACE INTO m82_blk_metrics VALUES (?, ?, ?, ?, ?, ?, ?)", blk_metrics)
    conn.commit()

    # 3. Lectura de Métricas de Snapshot
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Construcción del mensaje para Telegram con plantilla blindada
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *INGESTA INSTITUCIONAL: BLACKROCK, INC. (BLK.N)*
• *Empresa:* BlackRock, Inc. (`BLK.N`)
• *Market Cap:* `$102,148.06M USD`
• *Acciones en Circulación:* `149.21M`
• *Múltiplo P/E Est.:* `17.80x` (FY 2025)
• *Retorno s/ Patrimonio (ROE):* `15.20%`
• *Próximo Reporte Ganancias:* `13-Oct-2026`
• *Status Ingesta:* Datos almacenados en `m82_database.db`

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
    if procesar_e_ingresar_blk():
        print("✅ Datos de BlackRock procesados, almacenados en DB y transmitidos a Telegram.")
