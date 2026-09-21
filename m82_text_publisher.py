import sqlite3
import time
import os
import requests
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(os.path.expanduser("~/M82/.env"))
TG_TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TG_CHAT_ID = os.getenv("M82_TELEGRAM_CHAT", "-1004335849125")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# TIEMPO ENTRE PUBLICACIONES (Ritmo fluido y pausado)
PAUSA_SEGUNDOS = 30.0

def clean_text(text):
    if not text:
        return ""
    # Eliminar etiquetas HTML residuál
    clean = re.sub(r'<[^>]*>', '', str(text)).strip()
    return clean

def format_corporate_message(headline, desk_source):
    clean_headline = clean_text(headline)
    desk_clean = desk_source.replace("_", " ").upper()
    
    # FORMATO INSTITUCIONAL / CORPORATIVO (Texto Puro)
    msg = (
        f"🚨 <b>M82 BREAKING STREAM</b> [{desk_clean}]\n\n"
        f"🔴 {clean_headline}\n\n"
        f"🏛 <b>Molina Holdings LLC & Molina Global LLC</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • All Rights Reserved © 2026</i>\n\n"
        f"#M82 @MolinaHoldings"
    )
    return msg

def send_telegram_message(message_text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()
        if data.get("ok"):
            return True, "SUCCESS"
        elif data.get("error_code") == 429:
            retry_after = data.get("parameters", {}).get("retry_after", 10)
            return False, f"RATE_LIMIT:{retry_after}"
        else:
            return False, f"ERROR:{data.get('description')}"
    except Exception as e:
        return False, f"EXCEPTION:{e}"

def main_loop():
    print(f"🚀 [M82 CORPORATE ENGINE] Publicador de texto activo (Ritmo: {PAUSA_SEGUNDOS}s)...", flush=True)
    
    while True:
        try:
            if not os.path.exists(DB_PATH):
                time.sleep(5)
                continue

            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cursor = conn.cursor()
            
            # Buscar 1 noticia pendiente
            cursor.execute("""
                SELECT rowid, daemon_source, headline 
                from m82_multi_stream 
                WHERE status = 'PENDING' OR status IS NULL 
                ORDER BY rowid ASC LIMIT 1
            """)
            row = cursor.fetchone()
            
            if row:
                row_id, source, headline = row
                
                if not headline:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SKIPPED' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    conn.close()
                    continue

                formatted_msg = format_corporate_message(headline, source or "FINANCIAL_STREAM")
                success, status_msg = send_telegram_message(formatted_msg)
                
                if success:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    print(f"⚡ [ENVIADO ID {row_id}] {headline[:45]}...", flush=True)
                    conn.close()
                    time.sleep(PAUSA_SEGUNDOS)
                elif "RATE_LIMIT" in status_msg:
                    wait_time = int(status_msg.split(":")[1])
                    print(f"⏳ Telegram Rate Limit. Pausando {wait_time}s...", flush=True)
                    conn.close()
                    time.sleep(wait_time)
                else:
                    print(f"❌ Error al enviar ID {row_id}: {status_msg}", flush=True)
                    cursor.execute("UPDATE m82_multi_stream SET status = 'FAILED' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    conn.close()
                    time.sleep(5)
            else:
                conn.close()
                time.sleep(10)

        except Exception as e:
            print(f"⚠️ Error en bucle principal: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
