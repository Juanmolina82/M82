#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, json, textwrap, random, math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NFT_TOPIC = "m82_breaking_news"
NFT_SERVER = f"https://ntfy.sh/{NFT_TOPIC}"

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")

TARGETS = [
    ("NEW_YORK_DESK", "%22Wall+Street%22+OR+%22NYSE%22+OR+%22Nasdaq%22+OR+%22NY+Fed%22"),
    ("TRUMP_NEWSROOM", "%22Donald+Trump%22+OR+%22Trump+tariffs%22"),
    ("VENEZUELA_DESK", "Citgo+OR+OFAC+OR+Chevron+Venezuela+OR+PDVSA"),
    ("GLOBAL_MACRO", "Federal+Reserve+OR+Crude+Oil+OR+Bonds")
]

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"⚡ [{timestamp}] [M82 ENGINE] {msg}", flush=True)

def generate_network_card(headline, source):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#05080e')
    draw = ImageDraw.Draw(img)

    # Dibuja red cuántica de fondo (nodos y conexiones)
    random.seed(hash(headline) % 10000)
    nodes = [(random.randint(100, 700), random.randint(150, 850)) for _ in range(25)]
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes[i+1:]):
            dist = math.hypot(x1 - x2, y1 - y2)
            if dist < 220:
                alpha_blue = int(180 * (1 - dist / 220))
                draw.line([(x1, y1), (x2, y2)], fill=(15, 60, 110), width=1)

    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#00bfff')

    # Marcos de esquinas estilo HUD
    corner_len = 30
    draw.line([(30, 30), (30 + corner_len, 30)], fill='#1e293b', width=2)
    draw.line([(30, 30), (30, 30 + corner_len)], fill='#1e293b', width=2)
    draw.line([(770, 30), (770 - corner_len, 30)], fill='#1e293b', width=2)
    draw.line([(770, 30), (770, 30 + corner_len)], fill='#1e293b', width=2)
    draw.line([(30, 970), (30 + corner_len, 970)], fill='#1e293b', width=2)
    draw.line([(30, 970), (30, 970 - corner_len)], fill='#1e293b', width=2)
    draw.line([(770, 970), (770 - corner_len, 970)], fill='#1e293b', width=2)
    draw.line([(770, 970), (770, 970 - corner_len)], fill='#1e293b', width=2)

    try:
        font_header = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 26)
        font_sub = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 15)
        font_title = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 40)
        font_footer = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 32)
    except Exception:
        font_header = font_sub = font_title = font_footer = ImageFont.load_default()

    # Puntos superiores decorativos
    draw.ellipse([200, 48, 205, 53], fill='#00bfff')
    draw.ellipse([240, 48, 245, 53], fill='#00bfff')

    # Cabecera
    draw.text((60, 65), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#334155', font=font_sub)
    draw.text((60, 100), f"#M82 BREAKING [{source.upper()}]", fill='#dc2626', font=font_header)
    draw.line([(60, 140), (740, 140)], fill='#0f172a', width=2)

    # Titular principal
    wrapped_lines = textwrap.wrap(f"“{headline}”", width=26)
    y_pos = 280
    for line in wrapped_lines:
        draw.text((60, y_pos), line, fill='#ffffff', font=font_title)
        y_pos += 58

    # Pie de imagen
    draw.text((60, 840), "[ AGI QUANTUM VERIFIED ]", fill='#1e3a8a', font=font_sub)
    draw.text((60, 875), "@MolinaHoldings", fill='#ffffff', font=font_footer)
    draw.text((320, 885), "LLC", fill='#64748b', font=font_sub)

    img.save(IMG_PATH)
    return IMG_PATH

def send_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data=payload, files={'photo': photo}, timeout=10)
            return r.status_code == 200
    except Exception:
        return False

def send_nft(headline, source):
    try:
        headers = {
            "Title": f"M82 BREAKING: [{source.upper()}]",
            "Priority": "high",
            "Tags": "rotating_light,chart_with_upwards_trend"
        }
        r = requests.post(NFT_SERVER, data=headline.encode('utf-8'), headers=headers, timeout=10)
        return r.status_code == 200
    except Exception:
        return False

def process_stream():
    for tag, query in TARGETS:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:2]:
                    title = item.find('title').text.rsplit(" - ", 1)[0].strip()

                    conn = sqlite3.connect(DB_PATH, timeout=5.0)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("""
                            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
                            VALUES (?, ?, 'PROCESSED', CURRENT_TIMESTAMP)
                        """, (tag, title))
                        conn.commit()
                        conn.close()

                        # Generar tarjeta gráfica individual y despachar
                        card = generate_network_card(title, tag)
                        
                        caption = (
                            f"🚨 *#M82 BREAKING LIVE*\n\n"
                            f"🔴 *[{tag}]*\n"
                            f"{title}\n\n"
                            f"🏛 @MolinaHoldings LLC"
                        )

                        tg_ok = send_telegram(card, caption)
                        nft_ok = send_nft(title, tag)

                        log(f"🚀 DESPACHADO Individual -> TG: {tg_ok} | NFT: {nft_ok} | {title[:40]}...")
                        time.sleep(3) # Pausa entre envíos
                    except sqlite3.IntegrityError:
                        conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    log("🔥 Emisora M82 iniciada con diseño cuántico original y despacho por noticia...")
    while True:
        process_stream()
        time.sleep(10)
