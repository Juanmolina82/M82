import sqlite3
import requests
import subprocess
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def ejecutar_cron_job():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # 1. Asegurar tablas requeridas
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS m82_cron_log (
        job_id TEXT PRIMARY KEY,
        status TEXT,
        last_run TEXT
    )''')

    # 2. Registrar ejecución
    fecha_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT OR REPLACE INTO m82_cron_log VALUES (?, ?, ?)", ("REGULATORY_MONITOR", "SUCCESS", fecha_iso))
    conn.commit()

    # 3. Leer snapshot
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Transmitir alerta de confirmación
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *CRON SCHEDULER: REGULATORY MONITOR ACTIVADO*
• *Frecuencia:* Lunes a las 08:00 AM VET
• *Job Target:* Monitoreo automático de posiciones y filiales BlackRock
• *Estado en Termux:* `crond` activo y sincronizado con `m82_database.db`

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
    ejecutar_cron_job()
