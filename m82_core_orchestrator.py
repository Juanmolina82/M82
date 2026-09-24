#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, subprocess, requests, textwrap, shutil
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)

def get_best_font(size):
    # Intentar cargar fuentes del sistema Termux
    possible_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    # Nodos Cuánticos (Red Celeste)
    random.seed(101)
    nodes = [
        (180, 250), (220, 248), (390, 430), (585, 445), (605, 390), (695, 350),
        (700, 500), (715, 625), (620, 700), (685, 885), (708, 795), (720, 770),
        (465, 840), (450, 710), (328, 725), (465, 575), (530, 585), (625, 640),
        (108, 680), (140, 870), (180, 910), (245, 975), (368, 855), (298, 630)
    ]
    
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 210:
                draw.line([(x1, y1), (x2, y2)], fill='#0f2035', width=1)

    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#38bdf8')

    # Marcos
    b_len, b_pad, b_color, b_w = 30, 25, '#374151', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # Cargar Fuentes con Tamaños Grandes Garantizados
    f_meta = get_best_font(14)
    f_head = get_best_font(26)
    f_title = get_best_font(40)
    f_foot = get_best_font(32)

    # Dibujar Textos
    draw.text((60, 65), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#4b5563', font=f_meta)
    
    src_clean = str(source).upper().replace("M82_INFRA_TAG: ", "").replace("M82_INFRA_TAG:", "")
    draw.text((60, 100), f"#M82 BREAKING [{src_clean}]", fill='#ef4444', font=f_head)
    draw.line([(60, 145), (740, 145)], fill='#1f2937', width=1)

    # Titular envuelto
    lines = textwrap.wrap(headline, width=28)
    y_text = 280
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=f_title)
        y_text += 60

    draw.text((60, 835), "[ AGI QUANTUM VERIFIED ]", fill='#2563eb', font=f_meta)
    draw.text((60, 870), "@MolinaHoldings LLC", fill='#ffffff', font=f_foot)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    return IMG_PATH

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data=payload, files={'photo': photo}, timeout=15)
            return r.status_code == 200
    except Exception as e:
        return False

def main():
    print("🚀 Motor Gráfico M82 Actualizado con Fuentes del Sistema Android.")
    if not os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 5")
    rows = cursor.fetchall()

    for row_id, source, headline in rows:
        caption = f"🚨 *#M82 BREAKING*\n🔴 *[{str(source).upper()}]*\n{headline}\n\n🏛 @MolinaHoldings LLC"
        img_file = generate_card_image(headline, source, row_id)
        if send_telegram_photo(img_file, caption):
            cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_DISPATCHED' WHERE id = ?", (row_id,))
            conn.commit()
            print(f"✅ Tarjeta corregida despachada para ID {row_id}")
    conn.close()

if __name__ == "__main__":
    main()
