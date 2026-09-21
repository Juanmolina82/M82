import sqlite3
import time
import os
import requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHLURDPus66Y1hSgDKbwGC5zdN6DdufP3Y"
TG_CHAT_ID = "-1004335849125"

def test_telegram_connection():
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": "🚨 **TEST CONEXIÓN M82**: El bot está activo y conectado al canal."
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        res = r.json()
        if res.get("ok"):
            print("✅ Conexión con Telegram EXITOSA. El mensaje de prueba fue entregado.")
        else:
            print(f"❌ Error de Telegram API: {res.get('description')} (Código: {res.get('error_code')})")
    except Exception as e:
        print(f"❌ Error de red conectando a Telegram: {e}")

def process_stream():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY rowid ASC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        row_id, source, headline = row
        # Se envía en texto plano sin parse_mode para evitar fallos por caracteres especiales
        msg = f"🚨 #M82 BREAKING STREAM\n\n🔴 {headline}\n[{source}]\n\n👤 @MolinaHoldings LLC"
        
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {"chat_id": TG_CHAT_ID, "text": msg}
        
        try:
            r = requests.post(url, json=payload, timeout=10)
            res = r.json()
            if res.get("ok"):
                print(f"⚡ [TELEGRAM OK] Enviado: {headline[:40]}...")
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE rowid = ?", (row_id,))
                conn.commit()
            else:
                print(f"⚠️ Rechazado por Telegram: {res.get('description')}")
        except Exception as e:
            print(f"❌ Error de envío: {e}")
    else:
        print("ℹ️ No hay registros en estado PENDING en la base de datos.")
    
    conn.close()

if __name__ == "__main__":
    print("🔍 Probrando envío a Telegram...")
    test_telegram_connection()
    print("🚀 Iniciando ciclo de envío (15s de intervalo)...")
    while True:
        process_stream()
        time.sleep(15)
