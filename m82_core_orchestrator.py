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

# MATRIZ DE DAEMONS INTEGRADOS EN LA INFRAESTRUCTURA PRINCIPAL M82
DAEMONS = [
    # Capa 1: Macro & Risk
    "m82_macro_daemon.py",
    "m82_stress_score.py",
    "m82_scheduler_v9.py",
    
    # Capa 2: Cobertura Top 100
    "m82_valuation_peers_daemon.py",
    "m82_insiders_top100_daemon.py",
    "m82_debt_credit_daemon.py",
    "m82_musk_empire_daemon.py",
    
    # Capa 3: Mercados y Finanzas
    "m82_money_markets_polls_daemon.py",
    "m82_governance_officers_daemon.py",
    "m82_esg_sustainability_daemon.py",
    "m82_crypto_commodities_daemon.py",
    
    # Capa 4: Infraestructura, Salud de Red y Refinitiv Workspace
    "m82_api_health_checker.py",
    "m82_wifi_health_daemon.py",
    "m82_refinitiv_global_chain_daemon.py"
]

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [M82_ORCHESTRATOR] {msg}", flush=True)

def get_font(size):
    possible_fonts = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans.ttf"
    ]
    for path in possible_fonts:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    # 1. Marcos de Esquinas (Brackets)
    b_len, b_pad, b_color, b_w = 40, 40, '#334155', 3
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad - b_len, b_pad), (width - b_pad, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad - b_len, height - b_pad), (width - b_pad, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # 2. Red Malla/Nodos Quantum
    random.seed(row_id + 100)
    nodes = [
        (450, 220), (620, 240), (650, 180), (720, 140), (710, 320),
        (730, 520), (600, 480), (500, 630), (350, 640), (480, 470),
        (200, 580), (250, 780), (400, 760), (500, 820), (750, 790)
    ]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 220:
                draw.line([(x1, y1), (x2, y2)], fill='#101e36', width=2)

    for x, y in nodes:
        draw.ellipse([x-4, y-4, x+4, y+4], fill='#0284c7')

    # Fuentes
    font_sub = get_font(18)
    font_title = get_font(32)
    font_body = get_font(34)
    font_footer = get_font(28)

    # 3. Encabezado
    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-REFINITIV", fill='#64748b', font=font_sub)
    draw.text((60, 95), f"#M82 {str(source).upper()}", fill='#f43f5e', font=font_title)
    draw.line([(60, 145), (740, 145)], fill='#1e293b', width=2)

    # 4. Contenido
    lines = textwrap.wrap(headline, width=32)
    y_text = 220
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=font_body)
        y_text += 48

    # 5. Pie de página
    draw.text((60, 830), "[ AGI QUANTUM VERIFIED ]", fill='#0369a1', font=font_sub)
    draw.text((60, 870), "@MolinaHoldings", fill='#ffffff', font=font_footer)
    draw.text((320, 870), "LLC", fill='#64748b', font=font_footer)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)
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

def check_and_restart_daemons():
    for daemon in DAEMONS:
        daemon_path = os.path.expanduser(f"~/M82/{daemon}")
        if not os.path.exists(daemon_path):
            continue
        cmd = f"pgrep -f {daemon}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        if result.returncode != 0:
            log(f"⚠️ Daemon caído: {daemon}. Reiniciando...")
            subprocess.Popen(["python3", "-u", daemon_path])

def dispatch_pending_signals():
    if not os.path.exists(DB_PATH):
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'AGI_SYNTHESIZED' LIMIT 2")
        rows = cursor.fetchall()

        for row_id, source, headline in rows:
            caption = (
                f"🎯 *#M82 BREAKING STREAM*\n\n"
                f"🔴 *SOURCE: [{str(source).upper()}]*\n\n"
                f"{headline}\n\n"
                f"🏛 @MolinaHoldings LLC"
            )

            img_file = generate_card_image(headline, source, row_id)

            if send_telegram_photo(img_file, caption):
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_TELEGRAM' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"✅ Tarjeta M82 HD enviada ID {row_id}.")

            time.sleep(2)

        conn.close()
    except Exception as e:
        log(f"❌ Error en DB: {e}")

def main():
    log("==========================================")
    log("🚀 AGI CORE ORCHESTRATOR M82 - INTEGRACIÓN TOTAL")
    log("==========================================")

    while True:
        check_and_restart_daemons()
        dispatch_pending_signals()
        time.sleep(4)

if __name__ == "__main__":
    main()
