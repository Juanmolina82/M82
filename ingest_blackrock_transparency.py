import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def procesar_notificacion_transparencia():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Asegurar tabla de divulgaciones y snapshots
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS m82_regulatory_filings (
        filing_hash TEXT PRIMARY KEY,
        issuer_name TEXT,
        reporting_person TEXT,
        threshold_crossed TEXT,
        event_date TEXT,
        filing_date TEXT,
        details TEXT
    )''')

    # 2. Ingesta de la notificación recibida (PublicNow / Retail Estates / BlackRock)
    filing_data = (
        '90093DBA17845F30AC4CBC6A4E6B1FD49B43F8F4',
        'Retail Estates NV/SA (Euronext: RET)',
        'BlackRock, Inc. / BlackRock Institutional Trust Company',
        '> 3.00% (Derechos de voto)',
        '01/09/2026 - 02/09/2026',
        '07/09/2026',
        'BlackRock supera el umbral del 3% de derechos de voto en Retail Estates NV/SA (515,647 acciones / 3.43%)'
    )

    c.execute("INSERT OR REPLACE INTO m82_regulatory_filings VALUES (?, ?, ?, ?, ?, ?, ?)", filing_data)
    conn.commit()

    # 3. Consultar snapshot del sistema
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Generar reporte para Telegram en formato M82
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *REGULATORY FILING INGESTION: TRANSPARENCY NOTICE*
• *Emisor:* `Retail Estates NV/SA`
• *Sujeto Notificante:* `BlackRock, Inc.`
• *Entidad Operativa:* `BlackRock Institutional Trust Company, N.A.`
• *Umbral Cruzado:* `> 3.00%` (Derechos de Voto)
• *Posición Total:* `3.43%` (`515,647` acciones)
• *Fecha Evento:* `01-02 Sep 2026` | *Publicación:* `07 Sep 2026`
• *Hash Doc:* `90093DBA17845F30AC4CBC6A4E6B1FD49B43F8F4`

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
    if procesar_notificacion_transparencia():
        print("✅ Documento de transparencia procesado, guardado en DB y transmitido a Telegram.")
