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

def generate_quantum_card(headline, output_path):
    # Canvas 1080x1350 (Aspecto Terminal Proporcional)
    width, height = 1080, 1350
    bg_color = (6, 11, 20)       # Azul muy oscuro terminal
    cyan_bright = (0, 242, 254)   # Cian tecnología
    red_m82 = (230, 45, 55)      # Rojo M82
    white = (240, 243, 246)
    gray_sub = (120, 140, 165)
    
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Cargar Fuentes
    try:
        font_mono = ImageFont.truetype("monospace", 22)
        font_header_red = ImageFont.truetype("serif", 54)
        font_headline = ImageFont.truetype("serif", 50)
        font_footer_tag = ImageFont.truetype("monospace", 22)
        font_footer_brand = ImageFont.truetype("serif", 46)
    except:
        font_mono = font_header_red = font_headline = font_footer_tag = font_footer_brand = ImageFont.load_default()

    # 1. Marcos Tácticos Tópicos (Corners)
    c_len = 35
    pad = 50
    # Top Left Corner
    draw.line([(pad, pad), (pad + c_len, pad)], fill=cyan_bright, width=3)
    draw.line([(pad, pad), (pad, pad + c_len)], fill=cyan_bright, width=3)
    # Top Right Corner
    draw.line([(width - pad, pad), (width - pad - c_len, pad)], fill=cyan_bright, width=3)
    draw.line([(width - pad, pad), (width - pad, pad + c_len)], fill=cyan_bright, width=3)
    # Bottom Left Corner
    draw.line([(pad, height - pad), (pad + c_len, height - pad)], fill=cyan_bright, width=3)
    draw.line([(pad, height - pad), (pad, height - pad - c_len)], fill=cyan_bright, width=3)
    # Bottom Right Corner
    draw.line([(width - pad, height - pad), (width - pad - c_len, height - pad)], fill=cyan_bright, width=3)
    draw.line([(width - pad, height - pad), (width - pad, height - pad - c_len)], fill=cyan_bright, width=3)

    # 2. Header System Telemetry
    sys_text = "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms"
    draw.text((90, 80), sys_text, fill=cyan_bright, font=font_mono)

    # 3. #M82 BREAKING STREAM Header (Rojo)
    draw.text((90, 130), "#M82 BREAKING STREAM", fill=red_m82, font=font_header_red)
    draw.line([(90, 200), (width - 90, 200)], fill=(20, 35, 55), width=2)

    # 4. Titular Principal
    lines = textwrap.wrap(headline, width=30)
    y_start = 380
    for line in lines[:6]:
        draw.text((90, y_start), line, fill=white, font=font_headline)
        y_start += 72

    # 5. Bottom Branding
    draw.text((90, height - 170), "[ AGI QUANTUM VERIFIED ]", fill=cyan_bright, font=font_footer_tag)
    
    # Signature: @MolinaHoldings LLC
    draw.text((90, height - 125), "@MolinaHoldings", fill=white, font=font_footer_brand)
    # Medida del texto para acomodar LLC en gris
    draw.text((90 + 410, height - 125), "LLC", fill=gray_sub, font=font_footer_brand)

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
    
    img_filename = f"m82_quantum_{row_id}.png"
    img_path = os.path.join(OUTPUT_DIR, img_filename)
    
    # Generar la imagen Quantum Terminal
    generate_quantum_card(headline, img_path)
    
    # Formatear el pie idéntico a tu plantilla de entrada
    desk_tag = source.replace("_", " ").upper()
    caption = (
        f"🚨 <b>#M82 BREAKING STREAM</b>\n"
        f"🏷️ [<b>{desk_tag}</b>]\n\n"
        f"{headline}\n\n"
        f"🏛 <b>@MolinaHoldings LLC | AGI Quantum Node</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • 2026</i>"
    )
    
    status_code, response = send_telegram_photo(img_path, caption)
    
    if status_code == 200 and response.get("ok"):
        cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE id = ?", (row_id,))
        conn.commit()
        conn.close()
        print(f"⚡ [QUANTUM CARD SENT] ID {row_id} | {headline[:35]}...", flush=True)
        
        if os.path.exists(img_path):
            os.remove(img_path)
            
        time.sleep(2.5) # Ritmo rápido seguro
        return True

    elif status_code == 429 or response.get("error_code") == 429:
        retry_after = response.get("parameters", {}).get("retry_after", 12)
        conn.close()
        print(f"⏳ Rate limit Telegram: {retry_after}s...", flush=True)
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
    print("🚀 [M82 QUANTUM TERMINAL ENGINE] Generador visual activado...", flush=True)
    while True:
        try:
            had_work = process_queue()
            if not had_work:
                time.sleep(2.0)
        except Exception as err:
            print(f"⚠️ Error general: {err}", flush=True)
            time.sleep(3.0)
