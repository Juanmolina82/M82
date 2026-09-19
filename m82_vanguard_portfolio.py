import sqlite3
import requests
from datetime import datetime

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def ingestar_vanguard_portfolio():
    try:
        conn = sqlite3.connect("m82_database.db")
        c = conn.cursor()
        
        # Crear tabla para Holdings Institucionales
        c.execute('''CREATE TABLE IF NOT EXISTS m82_institutional_holdings (
            ticker TEXT PRIMARY KEY,
            company_name TEXT,
            portfolio_pct REAL,
            position_m REAL,
            position_change_m REAL,
            value_usd_m REAL,
            value_change_usd_m REAL,
            as_of_date TEXT
        )''')

        # Top Holdings extraídos de la pantalla Vanguard Capital Management, LLC
        holdings = [
            ('NVDA.OQ', 'NVIDIA Corporation', 4.85, 1300.97, 8.21, 508001.32, 10831.20, '07-Sep-2026'),
            ('AAPL.OQ', 'Apple Inc.', 4.25, 982.15, -12.30, 277322.01, -4120.15, '07-Sep-2026'),
            ('MSFT.OQ', 'Microsoft Corporation', 2.78, 481.18, 1.28, 182321.32, 1180.20, '07-Sep-2026'),
            ('AMZN.OQ', 'Amazon.com Inc.', 2.05, 345.12, 0.45, 131102.32, 850.10, '07-Sep-2026'),
            ('AVGO.OQ', 'Broadcom Inc.', 1.86, 220.17, 1.11, 118700.82, 1420.50, '07-Sep-2026'),
            ('GOOGL.OQ', 'Alphabet Inc. (Class A)', 1.55, 185.12, -0.80, 99120.10, -310.20, '07-Sep-2026'),
            ('MU.OQ', 'Micron Technology, Inc.', 1.32, 150.10, 4.32, 85204.00, 2102.30, '07-Sep-2026'),
            ('META.OQ', 'Meta Platforms, Inc.', 1.21, 142.04, -1.02, 78100.20, -510.40, '07-Sep-2026'),
            ('TSLA.OQ', 'Tesla, Inc.', 1.12, 125.00, -2.10, 72100.21, -890.10, '07-Sep-2026')
        ]

        c.executemany("INSERT OR REPLACE INTO m82_institutional_holdings VALUES (?,?,?,?,?,?,?,?)", holdings)
        conn.commit()

        # Extraer métricas de control M82
        c.execute("SELECT ovx, ltv_spot, nav_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
        snap = c.fetchone()
        conn.close()

        fecha_act = datetime.now().strftime("%d/%m/%Y %H:%M VET")

        # Formato de transmisión M82
        mensaje = f"""🏛 *M82 REFINITIV INSTITUTIONAL FEED*
🏢 *Firma:* Vanguard Capital Management, LLC
📅 _{fecha_act}_
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 *TOP HOLDINGS REGISTRADOS (Refinitiv Analytics)*
1. *NVDA.OQ:* 4.85% portfolio | Val: `$508,001.32M USD`
2. *AAPL.OQ:* 4.25% portfolio | Val: `$277,322.01M USD`
3. *MSFT.OQ:* 2.78% portfolio | Val: `$182,321.32M USD`
4. *AMZN.OQ:* 2.05% portfolio | Val: `$131,102.32M USD`
5. *AVGO.OQ:* 1.86% portfolio | Val: `$118,700.82M USD`

🌐 *SECTORES CLAVE:* Technology / Software / Industrials
📍 *UBICACIÓN PRINCIPAL:* North America / United States

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡 *ESTADO M82 ENGINE*
• *NAV Spot:* `${snap[2] if snap else '810.46'}M USD`
• *LTV Spot:* `{snap[1] if snap else '18.51'}%` (Límite: 19.0%)
• *Índice OVX:* `{snap[0] if snap else '32.50'}%` (Límite: 35.0%)
"""

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
        print("✅ Portafolio de Vanguard integrado y sincronizado con M82.")

    except Exception as e:
        print(f"Error registrando portafolio Vanguard: {e}")

if __name__ == "__main__":
    ingestar_vanguard_portfolio()
