import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def inicializar_y_blindar_db():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    
    # 1. Tabla Snapshot (Métria LTV / NAV / OVX protegida)
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    c.execute("SELECT COUNT(*) FROM snapshot")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO snapshot VALUES (32.50, 18.51, 810.46)")

    # 2. Tabla SEC Filings 13G
    c.execute('''CREATE TABLE IF NOT EXISTS m82_sec_13g_filings (
        filing_id TEXT PRIMARY KEY, issuer_name TEXT, reporting_person TEXT,
        shares_beneficially_owned INTEGER, percent_of_class REAL,
        sole_voting_power INTEGER, sole_dispositive_power INTEGER, filing_date TEXT
    )''')

    # 3. Tabla Argus Commodities Services (Catálogo Refinitiv)
    c.execute('''CREATE TABLE IF NOT EXISTS m82_argus_services (
        category TEXT, product_name TEXT, service_type TEXT
    )''')

    conn.commit()
    conn.close()

def enviar_alerta_estandar(cuerpo_contenido):
    inicializar_y_blindar_db()
    
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # FORMATO RÍGIDO / BLINDADO DE M82
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{cuerpo_contenido}

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
        print(f"Error en transmisión: {e}")
        return False

if __name__ == "__main__":
    cuerpo_argus = """📌 *ARGUS MEDIA / COMMODITIES SERVICES CATALOG*
• *Crude Oil:* Americas Crude, Caspian Markets, Crude & Refined Outlook
• *Oil Products:* Asphalt, European/US Refined Products Forward Curves
• *Gas & Power:* North American Natural Gas, Air Daily, Implied Volatilities
• *Metals & Agriculture:* Battery Materials, Global Steel, AgriMarkets
• *Data Suite:* Argus Direct®, Forward Curves, Near-term Outlooks & Analytics"""
    
    if enviar_alerta_estandar(cuerpo_argus):
        print("✅ Alerta enviada a Telegram con formato blindado.")
