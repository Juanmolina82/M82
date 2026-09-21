import sqlite3
import requests

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

LIMITE_OVX = 35.0
LIMITE_LTV = 19.0

def verificar_m82():
    try:
        conn = sqlite3.connect("m82_database.db")
        c = conn.cursor()
        c.execute("SELECT ovx, ltv_spot FROM snapshot ORDER BY rowid DESC LIMIT 1")
        row = c.fetchone()
        conn.close()

        if not row:
            print("M82: Sin registros recientes en snapshot.")
            return

        ovx_actual, ltv_actual = row
        alertas = []

        if ovx_actual and ovx_actual > LIMITE_OVX:
            alertas.append(f"⚠️ *M82 VOLATILIDAD*: OVX al {ovx_actual}%")
        if ltv_actual and ltv_actual > LIMITE_LTV:
            alertas.append(f"🚨 *M82 LTV*: LTV Spot al {ltv_actual}%")

        if not alertas:
            alertas.append("✅ *MONITOREO M82 (@MOLINAHOLDINGS)*: Motores en rango normal.")

        for msg in alertas:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
            print("Alerta M82 procesada correctamente.")
    except Exception as e:
        print(f"Error M82: {e}")

if __name__ == "__main__":
    verificar_m82()
