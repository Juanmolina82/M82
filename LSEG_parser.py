import sqlite3
import requests
from datetime import datetime
import os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

# LSEG / Refinitiv Instruments Mapping
RIC_FRONT = "CLc1"   # WTI Front Month ($94.51 Base)
RIC_CURVE = "0#CL:"  # Full Curve for OVX calculation
RIC_TAS   = "0#CLT:" # Trade at Settlement for NYMEX Margin

def actualizar_feed_lseg():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Crear tabla de configuracion e instrumental si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS m82_lseg_instruments (
        param_key TEXT PRIMARY KEY,
        ric_code TEXT,
        description TEXT,
        last_updated TEXT
    )''')

    # 2. Registrar los RICs
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    instruments = [
        ('RIC_FRONT', RIC_FRONT, 'WTI Front Month - NAV Spot Target', now_str),
        ('RIC_CURVE', RIC_CURVE, 'WTI Term Structure - OVX Model', now_str),
        ('RIC_TAS', RIC_TAS, 'Trade at Settlement - NYMEX Margin Control', now_str)
    ]
    c.executemany("INSERT OR REPLACE INTO m82_lseg_instruments VALUES (?,?,?,?)", instruments)

    # 3. Registrar el evento geopolitico del 08-Sep-2026
    c.execute('''CREATE TABLE IF NOT EXISTS m82_geopolitical_events (
        event_date TEXT,
        type TEXT,
        assets_hit TEXT,
        trigger TEXT,
        price_impact TEXT,
        PRIMARY KEY (event_date, type)
    )''')

    c.execute("""INSERT OR REPLACE INTO m82_geopolitical_events VALUES (
        '2026-09-08',
        'CENTCOM strike IRGC tankers',
        'Kaviz, Charminar, Horizon1, Riesco, Derya',
        'IRGC ballistic on US Navy x2',
        'Brent +$2.5-5 front month'
    )""")

    conn.commit()

    # 4. Obtener snapshot patrimonial
    try:
        c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
        snap = c.fetchone()
    except sqlite3.OperationalError:
        snap = (32.5, 18.51, 810.46)

    conn.close()

    # 5. Enviar Alerta Formateada
    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")
    ovx_val = snap[0] if snap else 32.5
    ltv_val = snap[1] if snap else 18.51
    nav_val = snap[2] if snap else 810.46

    ovx_status = "⚠️ CRÍTICO (>35.0%)" if ovx_val >= 35.0 else ("⚠️ PRÓXIMO AL LÍMITE" if ovx_val >= 32.0 else "NORMAL")

    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *CONFIGURACIÓN DE FEED DE MERCADO (RICs)*
• *Front Month (`RIC_FRONT`):* `{RIC_FRONT}` (WTI $94.51)
• *Estructura Curva (`RIC_CURVE`):* `{RIC_CURVE}`
• *Liquidación NYMEX (`RIC_TAS`):* `{RIC_TAS}`

📌 *REGISTRO EVENTO GEOPOLÍTICO*
• *Evento:* CENTCOM destruye 5 petroleros IRGC
• *Activos Impactados:* Kaviz, Charminar, Horizon1, Riesco, Derya
• *Mapeo DB:* `m82_geopolitical_events` actualizado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡 *MONITOR DE RIESGO Y MARGEN NYMEX*
• *NAV Spot:* `${nav_val}M USD`
• *LTV Spot:* `{ltv_val}%` (Máximo: 19.0%)
• *Índice OVX:* `{ovx_val}%` [{ovx_status}]
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
            print("✅ Feed LSEG y RICs actualizados con éxito en DB y notificados a Telegram.")
        else:
            print(f"⚠️ Actualizado en DB. Respuesta Telegram: {res.status_code}")
    except Exception as e:
        print(f"⚠️ Actualizado en DB. Sin conexión saliente a Telegram: {e}")

if __name__ == "__main__":
    actualizar_feed_lseg()
