#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, textwrap
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

# Configuración del servidor NFT / Ntfy Push
NFT_TOPIC = "m82_breaking_news"  # Reemplaza con tu tópico de Ntfy/NFT si es diferente
NFT_SERVER = f"https://ntfy.sh/{NFT_TOPIC}"

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [M82_ORCHESTRATOR] {msg}", flush=True)

def get_font(size):
    try:
        return ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", size)
    except Exception:
        return ImageFont.load_default()

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-REFINITIV", fill='#64748b', font=get_font(18))
    draw.text((60, 95), f"#M82 {str(source).upper()}", fill='#f43f5e', font=get_font(32))
    draw.line([(60, 145), (740, 145)], fill='#1e293b', width=2)

    lines = textwrap.wrap(headline, width=32)
    y_text = 220
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=get_font(34))
        y_text += 48

    draw.text((60, 870), "@MolinaHoldings LLC", fill='#ffffff', font=get_font(28))

    img.save(IMG_PATH)
    return IMG_PATH

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data=payload, files={'photo': photo}, timeout=15)
            return r.status_code == 200
    except Exception as e:
        log(f"❌ Error enviando a Telegram: {e}")
        return False

def send_nft_notification(headline, source):
    """Envía la notificación push al canal/servidor NFT (Ntfy)."""
    try:
        headers = {
            "Title": f"M82 Alert: [{str(source).upper()}]",
            "Priority": "high",
            "Tags": "rotating_light,chart_with_upwards_trend"
        }
        r = requests.post(NFT_SERVER, data=headline.encode('utf-8'), headers=headers, timeout=10)
        if r.status_code == 200:
            log(f"🔔 Notificación NFT enviada con éxito ({NFT_TOPIC}).")
            return True
        else:
            log(f"⚠️ Error en respuesta NFT: Status {r.status_code}")
            return False
    except Exception as e:
        log(f"❌ Error enviando notificación NFT: {e}")
        return False

def dispatch_pending_signals():
    if not os.path.exists(DB_PATH):
        return

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, daemon_source, headline 
            FROM m82_multi_stream 
            WHERE status IN ('PENDING', 'AGI_SYNTHESIZED') 
            ORDER BY id ASC 
            LIMIT 1
        """)
        row = cursor.fetchone()

        if row:
            row_id, source, headline = row

            cursor.execute("UPDATE m82_multi_stream SET status = 'PROCESSING' WHERE id = ?", (row_id,))
            conn.commit()

            caption = f"🎯 *#M82 BREAKING STREAM*\n\n🔴 *SOURCE: [{str(source).upper()}]*\n\n{headline}\n\n🏛 @MolinaHoldings LLC"
            img_file = generate_card_image(headline, source, row_id)

            # Envío dual: Telegram + NFT
            tg_success = send_telegram_photo(img_file, caption)
            nft_success = send_nft_notification(headline, source)

            if tg_success or nft_success:
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_SUCCESS' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"✅ Noticia ID {row_id} procesada (TG: {tg_success} | NFT: {nft_success}): {headline[:40]}...")
            else:
                cursor.execute("UPDATE m82_multi_stream SET status = 'FAILED' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"⚠️ Fallo general de envío para ID {row_id}.")

        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def main():
    log("🚀 Orquestador M82 Activo (Modo Dual Telegram + NFT).")
    while True:
        dispatch_pending_signals()
        time.sleep(5)

if __name__ == "__main__":
    main()
