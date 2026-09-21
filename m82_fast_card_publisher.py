import sqlite3
import time
import os
import requests
import textwrap
import zoneinfo
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/M82/.env"))
TG_TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TG_CHAT_ID = os.getenv("M82_TELEGRAM_CHAT", "-1004335849125")
DB_PATH = os.path.expanduser("~/m82_database.db")
OUTPUT_DIR = os.path.expanduser("~/M82/output_cards")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_ny_timestamp():
    ny_tz = zoneinfo.ZoneInfo("America/New_York")
    return datetime.now(ny_tz).strftime('%H:%M:%S EST')

def generate_m82_card(headline, category, output_path):
    width, height = 1080, 1080
    bg_color = (168, 12, 26)  # Rojo M82
    white = (255, 255, 255)
    
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("serif", 64)
        font_body = ImageFont.truetype("serif", 44)
        font_box = ImageFont.truetype("serif", 40)
        font_footer = ImageFont.truetype("sans-serif", 30)
    except:
        font_title = font_body = font_box = font_footer = ImageFont.load_default()

    # Encabezado
    draw.text((width // 2, 150), "M82 BREAKING STREAM", fill=white, font=font_title, anchor="mm")
    draw.line([(90, 210), (width - 90, 210)], fill=white, width=4)

    # Titular envuelto
    lines = textwrap.wrap(headline, width=32)
    y_text = 320
    for line in lines[:4]:
        draw.text((width // 2, y_text), line, fill=white, font=font_body, anchor="mm")
        y_text += 62

    # Franja Blanca Central (Estilo M82)
    box_top, box_bottom = 680, 790
    draw.rectangle([80, box_top, width - 80, box_bottom], fill=white)
    
    cat_clean = category.replace("_", " ").upper()
    draw.text((width // 2, (box_top + box_bottom) // 2), cat_clean, fill=bg_color, font=font_box, anchor="mm")

    # Pie institucional
    draw.line([(90, 870), (width - 90, 870)], fill=white, width=2)
    draw.text((width // 2, 940), "@MolinaHoldings LLC • Molina Global LLC", fill=white, font=font_footer, anchor="mm")

    img.save(output_path)

def send_telegram_photo(image_path, caption):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            payload = {
                'chat_id': TG_CHAT_ID, 
                'caption': caption,
                'parse_mode': 'HTML'
            }
            files = {'photo': photo}
            res = requests.post(url, data=payload, files=files, timeout=12)
            return res.status_code, res.json()
    except Exception as e:
        return 0, str(e)

def process_queue():
    if not os.path.exists(DB_PATH):
        return False

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, daemon_source, headline 
        FROM m82_multi_stream 
        WHERE status = 'PENDING' OR status IS NULL 
        ORDER BY id ASC LIMIT 1
    """)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False

    row_id, source, headline = row
    ts_ny = get_ny_timestamp()
    
    img_filename = f"m82_card_{row_id}.png"
    img_path = os.path.join(OUTPUT_DIR, img_filename)
    
    # 1. Generar la imagen visual
    generate_m82_card(headline, source, img_path)
    
    # 2. Formatear pie con Hashtags + Tags de Tesis
    caption = (
        f"🚨 <b>M82 BREAKING STREAM</b> ({ts_ny})\n\n"
        f"🔴 [<b>#{source.upper()}</b>]\n{headline}\n\n"
        f"🏛 <b>Molina Holdings LLC & Molina Global LLC</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • All Rights Reserved © 2026</i>\n\n"
        f"#M82 #SOVEREIGN_ESCROW #MolinaHoldings"
    )
    
    status_code, response = send_telegram_photo(img_path, caption)
    
    if status_code == 200 and response.get("ok"):
        cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE id = ?", (row_id,))
        conn.commit()
        conn.close()
        print(f"⚡ [{ts_ny}] TARJETA ENVIADA OK: ID {row_id} | {headline[:30]}...", flush=True)
        
        if os.path.exists(img_path):
            os.remove(img_path)
            
        time.sleep(2.5) # Ritmo acelerado seguro con imágenes
        return True

    elif status_code == 429 or response.get("error_code") == 429:
        retry_after = response.get("parameters", {}).get("retry_after", 15)
        conn.close()
        print(f"⏳ [FLOOD CONTROL] Pausa de Telegram: {retry_after}s...", flush=True)
        time.sleep(retry_after + 2)
        return True

    else:
        cursor.execute("UPDATE m82_multi_stream SET status = 'ERROR' WHERE id = ?", (row_id,))
        conn.commit()
        conn.close()
        print(f"⚠️ Error {status_code}: {response}. Saltando ID {row_id}", flush=True)
        time.sleep(2)
        return True

if __name__ == "__main__":
    print("🚀 [M82 FAST CARD ENGINE] En marcha con tarjetas + hashtags...", flush=True)
    while True:
        try:
            had_work = process_queue()
            if not had_work:
                time.sleep(2.0)
        except Exception as err:
            print(f"⚠️ Error general: {err}", flush=True)
            time.sleep(3.0)
