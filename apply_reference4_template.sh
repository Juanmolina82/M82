#!/usr/bin/env bash

cat << 'ORCH_EOF' > ~/M82/m82_core_orchestrator.py
#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, subprocess, requests, textwrap, shutil
from PIL import Image, ImageDraw, ImageFont

try:
    subprocess.run(["termux-wake-lock"], check=False)
except Exception:
    pass

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)

DAEMONS = [
    "m82_unga_summit_tracker_daemon.py",
    "m82_options_smart_money_daemon.py",
    "m82_macro_daemon.py",
    "m82_scheduler_v9.py",
    "m82_reuters_breakingviews.py"
]

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [CORE-ORCHESTRATOR] {msg}", flush=True)

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    # Nodos y red neuronal de fondo
    random.seed(101)
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

    # Esquinas tácticas HUD (Brackets)
    b_len, b_pad, b_color, b_w = 25, 25, '#374151', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # Carga de fuentes Serif estilo editorial
    font_paths = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf",
        "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "DejaVuSerif.ttf"
    ]
    
    font_title = font_meta = font_header = font_footer = font_sub = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 48)
                font_meta = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 15)
                font_header = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 28)
                font_footer = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 36)
                font_sub = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 24)
                break
            except Exception:
                pass

    if not font_title:
        font_meta = font_header = font_title = font_footer = font_sub = ImageFont.load_default()

    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#38bdf8', font=font_meta)
    draw.text((60, 95), "#M82 BREAKING STREAM", fill='#ef4444', font=font_header)
    draw.line([(60, 140), (740, 140)], fill='#1f2937', width=1)

    formatted_headline = headline.strip()
    lines = textwrap.wrap(formatted_headline, width=26)
    
    y_text = 280
    for line in lines:
        if y_text < 780:
            draw.text((60, y_text), line, fill='#ffffff', font=font_title)
            y_text += 68

    draw.text((60, 840), "[ AGI QUANTUM VERIFIED ]", fill='#38bdf8', font=font_meta)
    brand_text = "@MolinaHoldings"
    draw.text((60, 875), brand_text, fill='#ffffff', font=font_footer)
    
    try:
        bbox = font_footer.getbbox(brand_text)
        brand_width = bbox[2] - bbox[0]
    except Exception:
        brand_width = 320

    draw.text((60 + brand_width + 12, 885), "LLC", fill='#6b7280', font=font_sub)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    log(f"📸 Tarjeta estilo 4ª imagen guardada: {gallery_file}")
    return IMG_PATH

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data=payload, files={'photo': photo}, timeout=15)
            return r.status_code == 200
    except Exception as e:
        log(f"❌ Error Telegram: {e}")
        return False

def send_ntfy_alert(source, headline):
    try:
        headers = {
            "Title": f"M82 [{source.upper()}]".encode('utf-8').decode('latin-1'),
            "Priority": "high",
            "Tags": "warning,chart_with_upwards_trend"
        }
        requests.post(
            NTFY_URL,
            data=headline.encode('utf-8'),
            headers=headers,
            timeout=10
        )
    except Exception as e:
        log(f"⚠️ Error Ntfy: {e}")

def check_and_restart_daemons():
    for daemon in DAEMONS:
        daemon_path = os.path.expanduser(f"~/M82/{daemon}")
        if not os.path.exists(daemon_path):
            continue
        cmd = f"pgrep -f {daemon}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        if result.returncode != 0:
            log(f"⚠️ [ALERTA] Daemon caído: {daemon}. Reiniciando...")
            subprocess.Popen(["python3", "-u", daemon_path])

def dispatch_pending_signals():
    if not os.path.exists(DB_PATH):
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, daemon_source, headline 
            FROM m82_multi_stream 
            WHERE status = 'PENDING' 
            LIMIT 1
        """)
        row = cursor.fetchone()

        if row:
            row_id, source, headline = row
            caption = (
                f"🚨 *#M82 BREAKING SUMMARY*\n\n"
                f"🔴 *[{str(source).upper()}]*\n"
                f"{headline}\n\n"
                f"🏛 @MolinaHoldings LLC"
            )

            log(f"🎨 Generando tarjeta ID {row_id} estilo 4ª imagen...")
            img_file = generate_card_image(headline, source, row_id)

            send_ntfy_alert(source, headline)

            if send_telegram_photo(img_file, caption):
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_DISPATCHED' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"✅ Tarjeta y alertas despachadas correctamente para ID {row_id}.")
            else:
                log(f"⚠️ Reintentando despacho para ID {row_id}...")

        conn.close()
    except Exception as e:
        log(f"❌ Error DB: {e}")

def main():
    log("==========================================")
    log("🚀 ORQUESTADOR CORE QUANTUM M82 RESTAURADO ONLINE")
    log("==========================================")

    while True:
        check_and_restart_daemons()
        dispatch_pending_signals()
        time.sleep(10)

if __name__ == "__main__":
    main()
ORCH_EOF

chmod +x ~/M82/m82_core_orchestrator.py
pkill -f "m82_" && bash ~/M82/start_m82.sh
