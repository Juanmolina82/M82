import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def procesar_advfiling():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Asegurar tablas requeridas
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS m82_refinitiv_advfilings (
        document_id TEXT PRIMARY KEY,
        source_url TEXT,
        filing_type TEXT,
        ingested_at TEXT,
        status TEXT
    )''')

    # 2. Ingesta del registro del documento Refinitiv
    doc_id = "261272958"
    url_doc = "https://workspace.refinitiv.com/web/Apps/AdvFilings/?enowappcontainerver#/view/261272958/asfiled/dcn?external=true"
    fecha_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT OR REPLACE INTO m82_refinitiv_advfilings VALUES (?, ?, ?, ?, ?)",
              (doc_id, url_doc, "AdvFilings / AsFiled DCN", fecha_iso, "INGESTED"))
    
    conn.commit()

    # 3. Leer snapshot de riesgo patrimonial
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Enviar notificación blindada a Telegram
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *REFINITIV ADVFILINGS INGESTION*
• *Document ID:* `{doc_id}`
• *Fuente:* `Refinitiv Workspace (AdvFilings)`
• *Tipo:* `AsFiled DCN / Regulatory Document`
• *Estado Ingesta:* Registrado en `m82_database.db`
• *Link Ref:* [Abrir en Refinitiv Workspace]({url_doc})

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
    if procesar_advfiling():
        print("✅ Documento de Refinitiv (261272958) procesado, guardado en DB y enviado a Telegram.")
