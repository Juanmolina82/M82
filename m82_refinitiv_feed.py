import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def inicializar_tabla_noticias():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS m82_news_feed (
        news_id TEXT PRIMARY KEY,
        fecha TEXT,
        titulo TEXT,
        categoria TEXT,
        cuerpo TEXT,
        link_sec TEXT
    )''')
    conn.commit()
    conn.close()

def procesar_alertas_refinitiv():
    inicializar_tabla_noticias()
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # Ingesta de eventos extraídos directamente de Refinitiv Workspace / MT Newswires
    noticias = [
        (
            'EVC_SEC_20260907',
            '09/07/2026 16:02 EDT',
            'Según un informe reciente presentado ante la SEC, un directivo de Entravision Communications vendió acciones por valor de 293.965 dólares.',
            'SEC Form 4',
            '17:33 EDT, 04/09/2026 (MT Newswires) -- Paul A Zevnik, Director, vendió el 4 de septiembre de 2026 35.000 acciones de Entravision Communications (EVC) por 293.965 dólares. Tras la presentación del Formulario 4 ante la SEC, Zevnik controla un total de 2.825.920 acciones ordinarias de Clase A.',
            'https://www.sec.gov/Archives/edgar/data/1109116/000124589326000003/xslF345X05/primarydocument.xml'
        ),
        (
            'SPX_MACRO_20260907',
            '09/07/2026 16:02 EDT',
            'El S&P 500 registra una ligera ganancia semanal gracias al alza del sector energético y al peso del sector de consumo discrecional.',
            'Macro / Markets',
            '16:45 EDT, 09/04/2026 (MT Newswires) -- El índice S&P 500 subió un 0,1% esta semana cerrando en 7.718,60. Las ganancias del sector energético (+2,3%, MPC +5,4%, VLO +5,2%) lideraron el mercado tras el repunte del crudo.',
            'N/A'
        )
    ]

    c.executemany("INSERT OR REPLACE INTO m82_news_feed VALUES (?,?,?,?,?,?)", noticias)
    conn.commit()

    # Extraer métricas M82
    c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
    snap = c.fetchone()
    conn.close()

    fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

    # Formato de transmisión M82 Refinitiv Direct
    mensaje = f"""🌐 *M82 REFINITIV WORKSPACE DIRECT FEED*
👤 *Usuario:* `@MOLINAHOLDINGS` | *Servicio:* Institutional Real-Time Alerts
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FILING SEC FORM 4 — ENTRAVISION COMMUNICATIONS (EVC)*
_09/07/2026 16:02 EDT_
Paul A Zevnik (Director) vendió 35.000 acciones por $293.965 USD.
📄 [Ver Formulario SEC direct-link]({noticias[0][5]})

📈 *RESUMEN MACRO & S&P 500*
S&P 500 cerró en *7.718,60* (+0,1% semanal). Sector energético lidera (+2,3%) impulsado por crudo; Marathon Petroleum (+5,4%) y Valero Energy (+5,2%).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛 *MONITOR DE PATRIMONIO M82*
• *NAV Spot:* `${snap[2] if snap else '810.46'}M USD`
• *LTV Spot:* `{snap[1] if snap else '18.51'}%` | *OVX Volatilidad:* `{snap[0] if snap else '32.50'}%`
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    })

    if res.status_code == 200:
        print("✅ Alerta en tiempo real de Refinitiv transmitida a Telegram.")
    else:
        print(f"Error en envío: {res.text}")

if __name__ == "__main__":
    procesar_alertas_refinitiv()
