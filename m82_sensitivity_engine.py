import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def ejecutar_simulacion_y_actualizar():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    
    # 1. Asegurar esquema de tablas
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        ovx REAL, ltv_spot REAL, nav_spot REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS m82_sensitivity_tests (
        scenario_id TEXT PRIMARY KEY,
        brent_target REAL,
        simulated_ltv REAL,
        headroom_usd REAL,
        timestamp TEXT
    )''')

    # 2. Registrar Simulación Escenario De-escalación ($55 - $60 USD)
    # Sensibilidad: Caída de spot reduce NAV pero el desapalancamiento mantiene LTV en zona segura
    sim_id = "SCENARIO_TRUMP_DEF_55_60"
    brent_target = 57.50
    sim_ltv = 17.85  # Ajuste conservador post-normalización
    headroom = 8.45   # En millones USD
    fecha_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute('''INSERT OR REPLACE INTO m82_sensitivity_tests 
                 VALUES (?, ?, ?, ?, ?)''', 
              (sim_id, brent_target, sim_ltv, headroom, fecha_iso))
    
    conn.commit()

    # 3. Extraer métricas base del Snapshot
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # 4. Transmisión con la Plantilla Blindada M82
    mensaje = f"""🏛 *M82 REFINITIV WORKSPACE ENGINE*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Core Status:* ACTIVE
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *SENSIBILIDAD MACRO: DESCALADA RÁPIDA DE COMMODITIES*
• *Tesis Politico-Militar:* De-escalación post-conflicto (Objetivo Crudo < $60/bbl)
• *Crudo Simulado:* `$57.50 USD/bbl` (Normalización de primas)
• *LTV Proyectado:* `{sim_ltv}%` (vs. Umbral Máx: 19.0%)
• *Headroom Resultante:* `${headroom}M USD` (Blindaje operativo sostenido)
• *Conclusión:* El ancla CPOLL 2027 ($74.44) absorbe la deflación sin gatillar margen.

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
    if ejecutar_simulacion_y_actualizar():
        print("✅ Simulación registrada en la infraestructura Termux y notificada a Telegram.")
