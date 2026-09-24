#!/usr/bin/env python3
import os, sys, time, textwrap, requests
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.expanduser("~/M82"))
from m82_db import get_connection

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def get_font(size):
    try:
        return ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", size)
    except Exception:
        return ImageFont.load_default()

def render_card(headline, source):
    img = Image.new('RGB', (800, 1000), color='#070b12')
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "SYSTEM: AGI-CORE // REFINITIV WORKSPACE", fill='#64748b', font=get_font(18))
    draw.text((60, 95), f"#M82 {str(source).upper()}", fill='#f43f5e', font=get_font(32))
    draw.line([(60, 145), (740, 145)], fill='#1e293b', width=2)

    lines = textwrap.wrap(headline, width=30)
    y = 220
    for line in lines:
        draw.text((60, y), line, fill='#ffffff', font=get_font(36))
        y += 52

    draw.text((60, 870), "🏛 @MolinaHoldings LLC", fill='#ffffff', font=get_font(28))
    img.save(IMG_PATH)
    return IMG_PATH

def send_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as p:
            r = requests.post(url, data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}, files={'photo': p}, timeout=12)
            return r.status_code == 200
    except Exception as e:
        log(f"❌ Error enviando a Telegram: {e}")
        return False

def send_ntfy(source, headline):
    try:
        headers = {
            "Title": f"M82 BREAKING | [{str(source).upper()}]",
            "Priority": "high",
            "Tags": "chart_with_downwards_trend,rotating_light"
        }
        r = requests.post(NTFY_URL, data=headline.encode('utf-8'), headers=headers, timeout=10)
        return r.status_code == 200
    except Exception as e:
        log(f"❌ Error en ntfy.sh: {e}")
        return False

def process_queue():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()

    if row:
        row_id, source, headline = row
        cursor.execute("UPDATE m82_multi_stream SET status = 'PROCESSING' WHERE id = ?", (row_id,))
        conn.commit()

        card_path = render_card(headline, source)
        caption = f"🎯 *#M82 BREAKING STREAM*\n\n🔴 *SOURCE: [{source}]*\n\n{headline}\n\n🏛 @MolinaHoldings LLC"

        tg_ok = send_telegram(card_path, caption)
        ntfy_ok = send_ntfy(source, headline)

        if tg_ok or ntfy_ok:
            cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE id = ?", (row_id,))
            log(f"✅ Noticia enviada ID {row_id} (Telegram: {tg_ok} | NTFY: {ntfy_ok})")
        else:
            cursor.execute("UPDATE m82_multi_stream SET status = 'FAILED' WHERE id = ?", (row_id,))
            log(f"⚠️ Fallo al enviar ID {row_id}.")
        conn.commit()

    conn.close()

def main():
    log("🚀 Orquestador M82 Activo.")
    while True:
        process_queue()
        time.sleep(15)

if __name__ == "__main__":
    main()
