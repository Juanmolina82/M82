import sqlite3, time, os, requests, textwrap, re, math, random
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/M82/.env"))
TG_TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TG_CHAT_ID = os.getenv("M82_TELEGRAM_CHAT", "-1004335849125")
X_SECRET = os.getenv("X_CLIENT_SECRET")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
OUTPUT_DIR = os.path.expanduser("~/M82/output_cards")

os.makedirs(OUTPUT_DIR, exist_ok=True)
PAUSA_RITMO = 30.0

KEYWORD_HASHTAGS = {
    r"\bbitcoin\b": "#Bitcoin", r"\bbtc\b": "#BTC", r"\bcrypto\b": "#Crypto",
    r"\bopec\b": "#OPEC", r"\boil\b": "#Oil", r"\bcrude\b": "#Crude",
    r"\bgas\b": "#Gas", r"\benergy\b": "#Energy", r"\bvenezuela\b": "#Venezuela",
    r"\bbrazil\b": "#Brazil", r"\bargentina\b": "#Argentina", r"\bchina\b": "#China",
    r"\busa\b": "#USA", r"\bfed\b": "#FED", r"\bnvidia\b": "#Nvidia",
    r"\bamd\b": "#AMD", r"\bgoogle\b": "#Google", r"\bmicrosoft\b": "#Microsoft",
    r"\bai\b": "#AI", r"\bquantum\b": "#Quantum", r"\byields\b": "#Yields", r"\bbonds\b": "#Bonds"
}

def apply_hashtags(text):
    for pattern, hashtag in KEYWORD_HASHTAGS.items():
        text = re.sub(pattern, hashtag, text, flags=re.IGNORECASE)
    return text

def m82_thesis_tag(headline):
    h = headline.lower()
    tagged_h = apply_hashtags(headline)
    if any(k in h for k in ["bitcoin", "btc", "crypto", "yield", "bond"]):
        return f"{tagged_h}\n⚠️ <b>M82_Q_TAG:</b> Riesgo Short / Evaluar PQC"
    elif any(k in h for k in ["opec", "oil", "crude", "energy", "gas", "power"]):
        return f"{tagged_h}\n⚡ <b>M82_E_TAG:</b> Gap 1,000 TWh / Long Gas-to-Power"
    elif any(k in h for k in ["brazil", "argentina", "real", "peso", "latam", "venezuela"]):
        return f"{tagged_h}\n🌎 <b>M82_GEO_TAG:</b> Base-load PPA / Requiere Escrow 70%"
    elif any(k in h for k in ["defense", "f-35", "china", "sanctions", "semiconductor"]):
        return f"{tagged_h}\n🛡️ <b>M82_SUPPLY_TAG:</b> Control Cadena de Frío & Materiales QPU"
    return tagged_h

def format_caption(headline):
    tagged = m82_thesis_tag(headline)
    return (
        f"🚨 <b>#M82 BREAKING STREAM</b>\n\n"
        f"🔴 {tagged}\n\n"
        f"🏛 <b>@MolinaHoldings LLC & Molina Global LLC</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • All Rights Reserved © 2026</i>\n"
    )

def get_serif_font(size):
    font_paths = [
        "/system/fonts/Times.ttf", "/system/fonts/NotoSerif-Regular.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except: pass
    return ImageFont.load_default()

def get_sans_font(size):
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf", "/system/fonts/Roboto-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except: pass
    return ImageFont.load_default()

def draw_constellation_background(draw, width, height):
    """Genera la malla táctica/red neuronal de nodos y constelaciones tenue"""
    random.seed(82) # Semilla fija para mantener el mismo patrón siempre
    nodes = []
    for _ in range(35):
        nodes.append((random.randint(60, width - 60), random.randint(60, height - 60)))
    
    # Dibujar líneas entre nodos cercanos
    for i, (x1, y1) in enumerate(nodes):
        for x2, y2 in nodes[i+1:]:
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 220:
                alpha_val = int(25 * (1 - dist / 220))
                draw.line([(x1, y1), (x2, y2)], fill=(20, 55, 80), width=1)

    # Dibujar nodos de luz
    for x, y in nodes:
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(40, 110, 140))

def create_m82_agi_quantum_card(headline, output_path):
    width, height = 1080, 1350
    bg_color = (3, 6, 12)  # Azul noche profundo Cyber AGI
    
    cyan_sys    = (45, 145, 185)   # Cian táctico
    red_header  = (212, 43, 43)    # Rojo #M82
    white_text  = (245, 245, 245)  # Blanco titular
    white_corners = (220, 220, 220)# Esquinas plateadas
    gray_footer = (120, 130, 145)  # Gris azulado
    line_cyan   = (15, 40, 60)     # División fina

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Dibujar red neuronal de constelaciones de fondo
    draw_constellation_background(draw, width, height)

    font_title  = get_serif_font(58)
    font_footer_s = get_serif_font(36)
    font_sys    = get_sans_font(20)
    font_head   = get_sans_font(46)
    font_bold   = get_sans_font(44)

    # 2. ESQUINAS TÁCTICAS BLANCAS/PLATEADAS (┌ ┐ y └ ┘)
    pad = 35
    cl = 32
    # Arriba-Izquierda
    draw.line([(pad, pad), (pad + cl, pad)], fill=white_corners, width=2)
    draw.line([(pad, pad), (pad, pad + cl)], fill=white_corners, width=2)
    # Arriba-Derecha
    draw.line([(width - pad, pad), (width - pad - cl, pad)], fill=white_corners, width=2)
    draw.line([(width - pad, pad), (width - pad, pad + cl)], fill=white_corners, width=2)
    # Abajo-Izquierda
    draw.line([(pad, height - pad), (pad + cl, height - pad)], fill=white_corners, width=2)
    draw.line([(pad, height - pad), (pad, height - pad - cl)], fill=white_corners, width=2)
    # Abajo-Derecha
    draw.line([(width - pad, height - pad), (width - pad - cl, height - pad)], fill=white_corners, width=2)
    draw.line([(width - pad, height - pad), (width - pad, height - pad - cl)], fill=white_corners, width=2)

    # 3. TELEMETRÍA SUPERIOR CIAN
    sys_text = "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms"
    draw.text((85, 80), sys_text, fill=cyan_sys, font=font_sys)

    # 4. ENCABEZADO Y LÍNEA DIVISORIA FINA
    draw.text((85, 125), "#M82 BREAKING STREAM", fill=red_header, font=font_head)
    draw.line([(85, 190), (width - 85, 190)], fill=line_cyan, width=1)

    # 5. TITULAR PRINCIPAL (SERIF)
    clean_headline = re.sub(r'<[^>]*>', '', str(headline)).strip()
    lines = textwrap.wrap(clean_headline, width=28)
    y_text = 400
    for line in lines[:5]:
        draw.text((85, y_text), line, fill=white_text, font=font_title)
        y_text += 85

    # 6. SELLO INFERIOR Y MARCA
    draw.line([(85, 1140), (width - 85, 1140)], fill=line_cyan, width=1)
    draw.text((85, 1165), "[ AGI QUANTUM VERIFIED ]", fill=cyan_sys, font=font_sys)
    
    draw.text((85, 1210), "@MolinaHoldings", fill=white_text, font=font_bold)
    try:
        w_bold = font_bold.getlength("@MolinaHoldings ")
    except:
        w_bold = 380
    draw.text((85 + w_bold, 1218), "LLC", fill=gray_footer, font=font_footer_s)

    img.save(output_path, quality=95)
    
    # Copia instantánea a la Galería de Android
    gallery_dir = "/sdcard/Pictures/M82_Cards"
    os.makedirs(gallery_dir, exist_ok=True)
    gallery_path = os.path.join(gallery_dir, os.path.basename(output_path))
    img.save(gallery_path, quality=95)
    
    # Notificar a Android para refrescar la Galería al instante
    os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{gallery_path} >/dev/null 2>&1")

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
            res = requests.post(url, data=payload, files=files, timeout=15)
            return res.json().get("ok", False)
    except Exception as e:
        print(f"❌ Error Telegram: {e}", flush=True)
        return False

def post_to_x(headline):
    clean_h = apply_hashtags(headline)
    x_text = f"🚨 #M82 BREAKING STREAM\n\n🔴 {clean_h[:160]}\n\n🏛 @MolinaHoldings LLC\n⚖️ Proprietary Stream ©2026 🔒 PP/PE"
    url = "https://api.x.com/2/tweets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {X_SECRET}"
    }
    try:
        r = requests.post(url, json={"text": x_text}, headers=headers, timeout=10)
        if r.status_code == 201:
            print("🐤 [X / TWITTER OK] Post publicado.", flush=True)
        elif r.status_code in [402, 403]:
            print("⚠️ [X / TWITTER] Sin créditos ($0.00). Omitiendo...", flush=True)
    except Exception as e:
        print(f"⚠️ Exception X API: {e}", flush=True)

def main_loop():
    print("🚀 [M82 AGI QUANTUM EXACT] Generando gráficos idénticos a la plantilla...", flush=True)
    while True:
        try:
            if not os.path.exists(DB_PATH):
                time.sleep(5)
                continue

            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT rowid, daemon_source, headline 
                FROM m82_multi_stream 
                WHERE status = 'PENDING' OR status IS NULL 
                ORDER BY rowid ASC LIMIT 1
            """)
            row = cursor.fetchone()
            
            if row:
                row_id, source, headline = row
                if not headline:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SKIPPED' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    conn.close()
                    continue

                img_path = os.path.join(OUTPUT_DIR, f"m82_agi_quantum_{row_id}.png")
                
                create_m82_agi_quantum_card(headline, img_path)
                
                caption = format_caption(headline)
                tg_ok = send_telegram_photo(img_path, caption)
                post_to_x(headline)

                if tg_ok:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    print(f"⚡ [DESPACHO AGI QUANTUM ID {row_id}] {headline[:40]}...", flush=True)
                    # Imagen preservada en Galería
                else:
                    print(f"❌ Reintentando ID {row_id} en próximo ciclo...", flush=True)
                    
                conn.close()
                time.sleep(PAUSA_RITMO)
            else:
                conn.close()
                time.sleep(10)

        except Exception as e:
            print(f"⚠️ Loop Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
