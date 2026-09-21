import sqlite3, time, os, requests, textwrap, re
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
    r"\bbitcoin\b": "#Bitcoin",
    r"\bbtc\b": "#BTC",
    r"\bcrypto\b": "#Crypto",
    r"\bopec\b": "#OPEC",
    r"\boil\b": "#Oil",
    r"\bcrude\b": "#Crude",
    r"\bgas\b": "#Gas",
    r"\benergy\b": "#Energy",
    r"\bvenezuela\b": "#Venezuela",
    r"\bbrazil\b": "#Brazil",
    r"\bargentina\b": "#Argentina",
    r"\bchina\b": "#China",
    r"\busa\b": "#USA",
    r"\bfed\b": "#FED",
    r"\bnvidia\b": "#Nvidia",
    r"\bamd\b": "#AMD",
    r"\bgoogle\b": "#Google",
    r"\bmicrosoft\b": "#Microsoft",
    r"\bai\b": "#AI",
    r"\bquantum\b": "#Quantum",
    r"\byields\b": "#Yields",
    r"\bbonds\b": "#Bonds"
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
    """Firma institucional M82 completa con Hashtags y Thesis Tags"""
    tagged = m82_thesis_tag(headline)
    return (
        f"🚨 <b>#M82 BREAKING STREAM</b>\n\n"
        f"🔴 {tagged}\n\n"
        f"🏛 <b>@MolinaHoldings LLC & Molina Global LLC</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • All Rights Reserved © 2026</i>\n"
        f"🔒 <i>Patent Pending / Protected Engine Direct Access</i>"
    )

def get_serif_font(size):
    font_paths = [
        "/system/fonts/Times.ttf",
        "/system/fonts/NotoSerif-Regular.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def create_m82_card(headline, tag_category, output_path):
    width, height = 1080, 1350
    bg_color = (10, 10, 10)
    
    red_header  = (212, 43, 43)
    white_text  = (245, 245, 245)
    green_tag   = (46, 184, 114)
    gray_footer = (120, 120, 120)
    border_gray = (35, 35, 35)

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    draw.rectangle([30, 30, width - 30, height - 30], outline=border_gray, width=2)

    font_head   = get_serif_font(52)
    font_title  = get_serif_font(58)
    font_tag    = get_serif_font(46)
    font_footer = get_serif_font(36)

    # 1. Header
    draw.text((90, 100), "#M82 BREAKING STREAM", fill=red_header, font=font_head)

    # 2. Titular limpia
    clean_headline = re.sub(r'<[^>]*>', '', str(headline)).strip()
    lines = textwrap.wrap(clean_headline, width=28)
    y_text = 320
    for line in lines[:5]:
        draw.text((90, y_text), line, fill=white_text, font=font_title)
        y_text += 80

    # 3. Tag
    clean_tag = tag_category.replace("_", " ").upper()
    draw.text((90, 800), f"Tag: {clean_tag}", fill=green_tag, font=font_tag)

    # 4. Footer Tarjeta
    draw.text((90, 1220), "@MolinaHoldings LLC | PP/PE Direct Access", fill=gray_footer, font=font_footer)

    img.save(output_path, quality=95)

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
        print(f"❌ Error al enviar imagen a Telegram: {e}", flush=True)
        return False

def post_to_x(headline):
    clean_h = apply_hashtags(headline)
    x_text = f"🚨 #M82 BREAKINGSTREAM\n\n🔴 {clean_h[:160]}\n\n🏛 @MolinaHoldings LLC\n⚖️ Proprietary Stream ©2026 🔒 PP/PE"
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
    print("🚀 [M82 ENGINE OFICIAL] Tarjeta Minimalista + Caption con Firma Legal y Hashtags ACTIVE...", flush=True)
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

                img_path = os.path.join(OUTPUT_DIR, f"m82_card_{row_id}.png")
                tag_str = source or "M82 INTEL"
                
                # 1. Generar la tarjeta negra de alta definición
                create_m82_card(headline, tag_str, img_path)
                
                # 2. Generar el caption formateado con la firma completa
                caption = format_caption(headline)

                # 3. Enviar IMAGEN + CAPTION COMPLETO a Telegram
                tg_ok = send_telegram_photo(img_path, caption)
                
                # 4. Publicación en X
                post_to_x(headline)

                if tg_ok:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    print(f"⚡ [DESPACHO OFICIAL COMPLETADO ID {row_id}] {headline[:40]}...", flush=True)
                    if os.path.exists(img_path):
                        os.remove(img_path)
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
