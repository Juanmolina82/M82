import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def procesar_e_ingresar_csco():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Tablas de perfil, datos financieros e instituciones para CSCO
    c.execute('''CREATE TABLE IF NOT EXISTS m82_csco_profile (
        ticker TEXT PRIMARY KEY,
        company_name TEXT,
        market_cap_m REAL,
        close_price REAL,
        isin TEXT,
        employees INTEGER,
        recommendation TEXT,
        last_updated TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS m82_csco_financials (
        ticker TEXT,
        fiscal_year TEXT,
        revenue_m REAL,
        operating_income_m REAL,
        net_income_m REAL,
        eps REAL,
        PRIMARY KEY (ticker, fiscal_year)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS m82_csco_top_holders (
        ticker TEXT,
        investor_name TEXT,
        pct_outstanding REAL,
        shares_m REAL,
        value_m REAL,
        filing_date TEXT,
        PRIMARY KEY (ticker, investor_name)
    )''')

    # 2. Ingesta de Perfil (Datos del reporte LSEG / Refinitiv Workspace)
    profile_data = ('CSCO.O', 'CISCO SYSTEMS INC', 430530.49, 108.61, 'US17275R1023', 84900, 'Buy (2.21)', '08-Sep-2026')
    c.execute("INSERT OR REPLACE INTO m82_csco_profile VALUES (?,?,?,?,?,?,?,?)", profile_data)

    # 3. Ingesta Historica Financiera (De la seccion Financial Summary)
    financials_data = [
        ('CSCO.O', 'FY 2022', 51557.0, 13969.0, 11812.0, 2.82),
        ('CSCO.O', 'FY 2023', 56998.0, 15007.0, 12613.0, 3.07),
        ('CSCO.O', 'FY 2024', 53803.0, 12161.0, 10320.0, 2.54),
        ('CSCO.O', 'FY 2025', 54594.0, 11762.0, 10300.0, 2.56),
        ('CSCO.O', 'FY 2026', 60325.0, 15157.0, 13237.0, 3.32)
    ]
    c.executemany("INSERT OR REPLACE INTO m82_csco_financials VALUES (?,?,?,?,?,?)", financials_data)

    # 4. Ingesta de Top Inversionistas Institucionales
    top_holders = [
        ('CSCO.O', 'Vanguard Capital Management, LLC', 6.21, 244.79, 28752.72, '30-Jun-2026'),
        ('CSCO.O', 'BlackRock Institutional Trust Company, N.A.', 5.48, 215.96, 25366.87, '30-Jun-2026'),
        ('CSCO.O', 'State Street Investment Management (US)', 5.00, 197.15, 23157.60, '30-Jun-2026'),
        ('CSCO.O', 'Invesco Capital Management LLC', 3.09, 121.71, 14296.02, '30-Jun-2026'),
        ('CSCO.O', 'Vanguard Portfolio Management, LLC', 3.03, 119.31, 14014.13, '30-Jun-2026')
    ]
    c.executemany("INSERT OR REPLACE INTO m82_csco_top_holders VALUES (?,?,?,?,?,?)", top_holders)

    conn.commit()

    # 5. Consulta del Snapshot Patrimonial
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 6. Transmision a Telegram
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *INGESTA INSTITUCIONAL: CISCO SYSTEMS INC (`CSCO.O`)*
• *Empresa:* Cisco Systems, Inc. (`CSCO.O`)
• *Precio de Cierre:* `$108.61 USD`
• *Market Cap:* `$430,530.49M USD`
• *Consenso Analistas:* `Buy (2.21)`
• *Principal Accionista:* Vanguard (`6.21%` | `$28,752.72M`)
• *Segundo Accionista:* BlackRock (`5.48%` | `$25,366.87M`)
• *Status Ingesta:* Tablas `m82_csco_*` actualizadas en `m82_database.db`

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
        print(f"Error de transmisión: {e}")
        return False

if __name__ == "__main__":
    if procesar_e_ingresar_csco():
        print("✅ Módulo Cisco Systems (CSCO.O) registrado exitosamente en DB y notificado a Telegram.")
