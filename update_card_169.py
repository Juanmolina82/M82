import os

orchestrator_path = os.path.expanduser("~/M82/m82_core_orchestrator.py")

new_orchestrator_content = '''#!/usr/bin/env python3
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
    # Formato 16:9 HD Optimizado para Telegram (1200x675)
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), color='#070c14')
    draw = ImageDraw.Draw(img)

    # Nodos sutiles de fondo
    random.seed(101)
    nodes = [(random.randint(50, 1150), random.randint(50, 625)) for _ in range(20)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 200:
                draw.line([(x1, y1), (x2, y2)], fill='#101f33', width=1)

    # Fuentes pesadas HD
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    
    font_title = font_meta = font_header = font_brand = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 36)
                font_meta = ImageFont.truetype(path, 18)
                font_header = ImageFont.truetype(path, 26)
                font_brand = ImageFont.truetype(path, 30)
                break
            except Exception:
                pass

    if not font_title:
        font_title = font_meta = font_header = font_brand = ImageFont.load_default()

    # Encabezado Neón High-Visibility
    draw.text((50, 35), "SYSTEM: AGI-CORE // QUANTUM VERIFIED", fill='#00f5d4', font=font_meta)
    draw.text((50, 65), f"#M82 BREAKING [{str(source).upper()}]", fill='#ff2a5f', font=font_header)
    draw.line([(50, 105), (1150, 105)], fill='#1e293b', width=2)

    # Caja de texto principal de alto contraste
    draw.rectangle([40, 125, 1160, 545], fill='#0d1829', outline='#00b4d8', width=2)

    # Ajuste de líneas a 52 caracteres para el ancho 1200px
    formatted_headline = headline.strip()
    lines = textwrap.wrap(formatted_headline, width=50)
    
    y_text = 160
    for line in lines:
        if y_text < 500:
            draw.text((70, y_text), line, fill='#ffffff', font=font_title)
            y_text += 52

    # Footer
    draw.text((50, 570), f"HASH PROOF: {int(time.time())}xM82", fill='#00b4d8', font=font_meta)
    draw.line([(50, 600), (1150, 600)], fill='#1e293b', width=1)
    draw.text((50, 615), "@MolinaHoldings LLC", fill='#ffffff', font=font_brand)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    log(f"📸 Tarjeta 16:9 HD guardada: {gallery_file}")
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

            log(f"🎨 Generando tarjeta 16:9 ID {row_id}...")
            img_file = generate_card_image(headline, source, row_id)

            send_ntfy_alert(source, headline)

            if send_telegram_photo(img_file, caption):
                cursor.execute("UPDATE m82_multi_stream SET status = 'SENT_DISPATCHED' WHERE id = ?", (row_id,))
                conn.commit()
                log(f"✅ Tarjeta y alertas despachadas para ID {row_id}.")
            else:
                log(f"⚠️ Reintentando despacho para ID {row_id}...")

        conn.close()
    except Exception as e:
        log(f"❌ Error DB: {e}")

def main():
    log("==========================================")
    log("🚀 ORQUESTADOR CORE QUANTUM M82 (16:9 HD) ONLINE")
    log("==========================================")

    while True:
        check_and_restart_daemons()
        dispatch_pending_signals()
        time.sleep(10)

if __name__ == "__main__":
    main()
'''

with open(orchestrator_path, "w") as f:
    f.write(new_orchestrator_content)

print("✅ Orquestador M82 actualizado a 16:9 HD de alta visibilidad.")
