#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, subprocess, requests, textwrap, shutil
from PIL import Image, ImageDraw, ImageFont

try:
    subprocess.run(["termux-wake-lock"], check=False)
except Exception:
    pass

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)

# Lista de Daemons individuales + Lanzador de la Fábrica RSS
DAEMONS = [
    "m82_refinitiv_watchlist_daemon.py",
    "m82_refinitiv_banking_daemon.py",
    "m82_keepalive_5g_daemon.py",
    "m82_launch_all.py",
    "m82_macro_daemon.py",
    "m82_scheduler_v9.py",
    "m82_crypto_commodities_daemon.py",
    "m82_musk_empire_daemon.py",
    "m82_insiders_top100_daemon.py",
    "m82_debt_credit_daemon.py",
    "m82_valuation_peers_daemon.py",
    "m82_governance_officers_daemon.py",
    "m82_esg_sustainability_daemon.py",
    "m82_refinitiv_venues_charts_daemon.py",
    "m82_commodities_topnews_daemon.py",
    "m82_us_me_energy_fund_daemon.py",
    "m82_financials_fundamentals_daemon.py",
    "m82_estimates_analysts_daemon.py",
    "m82_news_research_daemon.py"
]

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

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

    b_len, b_pad, b_color, b_w = 25, 25, '#374151', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    font_paths = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf",
        "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "DejaVuSerif.ttf"
    ]
    
    font_title = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 42)
                font_meta = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 13)
                font_header = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 26)
                font_footer = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans-Bold"), 32)
                font_sub = ImageFont.truetype(path.replace("DejaVuSerif", "DejaVuSans"), 22)
                break
            except Exception:
                pass

    if not font_title:
        font_meta = font_header = font_title = font_footer = font_sub = ImageFont.load_default()

    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#4b5563', font=font_meta)
    draw.text((60, 95), "#M82 BREAKING STREAM", fill='#ef4444', font=font_header)
    draw.line([(60, 140), (740, 140)], fill='#1f2937', width=1)

    formatted_headline = headline.title()
    lines = textwrap.wrap(formatted_headline, width=28)
    y_text = 300
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=font_title)
        y_text += 62

    draw.text((60, 840), "[ AGI QUANTUM VERIFIED ]", fill='#2563eb', font=font_meta)
    brand_text = "@MolinaHoldings"
    draw.text((60, 875), brand_text, fill='#ffffff', font=font_footer)
    
    try:
        bbox = font_footer.getbbox(brand_text)
        brand_width = bbox[2] - bbox[0]
    except AttributeError:
        brand_width = draw.textlength(brand_text, font=font_footer) if hasattr(draw, 'textlength') else 310

    draw.text((60 + brand_width + 12, 882), "LLC", fill='#6b7280', font=font_sub)

    img.save(IMG_PATH)

    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    log(f"📸 Tarjeta guardada en Galería: {gallery_file}")
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
        log(f"❌ Error enviando a Telegram: {e}")
        return False

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
            LIMIT 3
        """)
        rows = cursor.fetchall()

        for row_id, source, headline in rows:
            caption = (
                f"🚨 *#M82 BREAKING SUMMARY*\n\n"
                f"🔴 *[{str(source).upper()}]*\n"
                f"{headline}\n\n"
                f"🏛 @MolinaHoldings LLC"
            )

            log(f"🎨 Generando tarjeta ID {row_id}...")
            img_file = generate_card_image(headline, source, row_id)

            if send_telegram_photo(img_file, caption):
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_TELEGRAM' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"✅ Tarjeta despachada ID {row_id}.")
            else:
                log(f"⚠️ Falló el envío ID {row_id}.")

            time.sleep(3)

        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def main():
    log("==========================================")
    log("🚀 INFRAESTRUCTURA M82 INTEGRADA CON FÁBRICA DE DAEMONS Y RSS")
    log("==========================================")

    while True:
        check_and_restart_daemons()
        dispatch_pending_signals()
        time.sleep(15)

if __name__ == "__main__":
    main()
