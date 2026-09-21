import os
import time
import sqlite3
import requests
import subprocess
from m82_card_publisher import create_m82_agi_quantum_card

TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
CHAT = os.getenv("M82_TELEGRAM_CHAT", "-1004335849125")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

GALLERY_DIR = os.path.expanduser("~/storage/shared/Pictures/Telegram")
os.makedirs(GALLERY_DIR, exist_ok=True)

def send_telegram_photo(caption, img_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(img_path, 'rb') as photo:
            res = requests.post(
                url, 
                data={'chat_id': CHAT, 'caption': caption, 'parse_mode': 'HTML'}, 
                files={'photo': photo}, 
                timeout=15
            )
            return res.status_code == 200
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}", flush=True)
        return False

def process_stream_ultra_slow():
    if not os.path.exists(DB_PATH):
        return

    row = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1;")
        row = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error leyendo DB: {e}", flush=True)
        time.sleep(5)
        return

    if row:
        row_id, source, headline = row
        tag_clean = source.replace("_", " ") if source else "BREAKING"
        
        img_filename = f"M82_Card_{row_id}.png"
        target_path = os.path.join(GALLERY_DIR, img_filename)
        
        # Generar una sola tarjeta con el formato AGI Quantum
        create_m82_agi_quantum_card(headline, target_path)
        
        try:
            subprocess.run(['termux-media-scan', target_path], stderr=subprocess.DEVNULL)
        except Exception:
            pass

        caption = (
            f"🚨 <b>#M82 BREAKING STREAM</b>\n"
            f"🏷️ <i>[{tag_clean}]</i>\n\n"
            f"<b>{headline}</b>\n\n"
            f"🏛 @MolinaHoldings LLC | AGI Quantum Node\n"
            f"⚖️ Proprietary Financial Stream • 2026"
        )

        if send_telegram_photo(caption, target_path):
            try:
                conn = sqlite3.connect(DB_PATH, timeout=30.0)
                cursor = conn.cursor()
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE id = ?;", (row_id,))
                conn.commit()
                conn.close()
                print(f"⚡ [ENVÍO EXITOSO]: Card #{row_id} enviada. Esperando 10 MINUTOS para la siguiente...", flush=True)
            except Exception as e:
                print(f"⚠️ Error actualizando estado: {e}", flush=True)

            # ⏳ PAUSA DE 10 MINUTOS (600 SEGUNDOS)
            time.sleep(600)
        else:
            print(f"⚠️ Falló el envío. Reintentando en 10s...", flush=True)
            time.sleep(10)
    else:
        time.sleep(10)

if __name__ == "__main__":
    print("🚀 [M82 PUBLISHER]: Modo Ultra Lento Activo (1 tarjeta cada 10 minutos)...", flush=True)
    while True:
        process_stream_ultra_slow()
