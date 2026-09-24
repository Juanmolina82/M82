#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, requests, textwrap, shutil
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.expanduser("~/M82"))
from m82_db import get_connection

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [M82-CORE] {msg}", flush=True)

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    # Red de Nodos Cuánticos M82 (Fondo)
    random.seed(int(row_id) if row_id else 101)
    nodes = [
        (180, 50), (220, 48), (390, 230), (585, 245), (605, 190), (695, 150),
        (700, 300), (915, 425), (720, 500), (785, 785), (808, 695), (920, 670),
        (465, 740), (450, 610), (328, 625), (465, 475), (530, 485), (625, 540),
        (78, 580), (140, 770), (180, 810), (245, 875), (368, 755), (298, 530)
    ]
    
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 230:
                draw.line([(x1, y1), (x2, y2)], fill='#10233b', width=1)

    for x, y in nodes:
        draw.ellipse([x-2, y-2, x+2, y+2], fill='#38bdf8')

    # Marcos de esquina UI
    b_len, b_pad, b_color, b_w = 25, 25, '#374151', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # Cargar Tipografía Serif
    font_paths = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf",
        "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    ]
    
    font_title = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 40)
                font_meta = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 13)
                font_header = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 26)
                font_footer = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 32)
                font_sub = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 22)
                break
            except Exception:
                pass

    if not font_title:
        font_meta = font_header = font_title = font_footer = font_sub = ImageFont.load_default()

    # Encabezados
    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#4b5563', font=font_meta)
    draw.text((60, 95), f"#M82 BREAKING [{str(source).upper()}]", fill='#ef4444', font=font_header)
    draw.line([(60, 140), (740, 140)], fill='#1f2937', width=1)

    # Titular con tipografía Serif
    lines = textwrap.wrap(headline, width=28)
    y_text = 280
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=font_title)
        y_text += 60

    # Footer Oficial
    draw.text((60, 840), "[ AGI QUANTUM VERIFIED ]", fill='#2563eb', font=font_meta)
    brand_text = "@MolinaHoldings"
    draw.text((60, 875), brand_text, fill='#ffffff', font=font_footer)
    
    try:
        bbox = font_footer.getbbox(brand_text)
        brand_width = bbox[2] - bbox[0]
    except AttributeError:
        brand_width = 310

    draw.text((60 + brand_width + 12, 882), "LLC", fill='#6b7280', font=font_sub)

    img.save(IMG_PATH)

    # Backup en la galería de Android
    if row_id:
        gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}.png")
        try:
            shutil.copy(IMG_PATH, gallery_file)
        except Exception:
            pass

    return IMG_PATH

def send_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as p:
            r = requests.post(url, data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}, files={'photo': p}, timeout=12)
            return r.status_code == 200
    except Exception:
        return False

def send_ntfy(source, headline):
    try:
        headers = {
            "Title": f"M82 BREAKING | [{str(source).upper()}]",
            "Priority": "high",
            "Tags": "rotating_light,chart_with_upwards_trend"
        }
        r = requests.post(NTFY_URL, data=headline.encode('utf-8'), headers=headers, timeout=10)
        return r.status_code == 200
    except Exception:
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

        card_path = generate_card_image(headline, source, row_id)
        caption = f"🚨 *#M82 BREAKING STREAM*\n\n🔴 *SOURCE: [{source}]*\n\n{headline}\n\n🏛 @MolinaHoldings LLC"

        tg_ok = send_telegram(card_path, caption)
        time.sleep(3)
        ntfy_ok = send_ntfy(source, headline)

        if tg_ok or ntfy_ok:
            cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE id = ?", (row_id,))
            log(f"✅ Alerta enviada con diseño oficial ID {row_id}")
        else:
            cursor.execute("UPDATE m82_multi_stream SET status = 'FAILED' WHERE id = ?", (row_id,))
            log(f"⚠️ Fallo al despachar ID {row_id}")
        conn.commit()

    conn.close()

def main():
    log("🚀 Orquestador M82 activo con plantilla Quantum Dark fijada.")
    while True:
        try:
            process_queue()
        except Exception as e:
            log(f"Excepción capturada: {e}")
        time.sleep(12)

if __name__ == "__main__":
    main()
