#!/usr/bin/env python3
# M82 V60.3 AGI :: X-COMPLIANT DISPATCHER 240 CHAR HARD CAP
# Nodo Charallave L4/L5 Edge | CUSTODIA PASIVA 0.30x LOCK

import os, sys, time, json, sqlite3, requests, textwrap, re
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
VAULT_PATH = os.path.join(M82_DIR, ".m82_vault.json")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"
IMG_PATH = os.path.join(M82_DIR, "m82_card_latest.png")
os.makedirs(GALLERY_DIR, exist_ok=True)
os.makedirs(M82_DIR, exist_ok=True)

# CARGA VAULT
def load_vault():
    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH) as f:
            return json.load(f)
    return {"token": "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4", "chat_id": "-1004335849125"}

VAULT = load_vault()
TOKEN = VAULT.get("token")
CHAT_ID = VAULT.get("chat_id")

def parse_lseg_event(event_data):
    if isinstance(event_data, str):
        raw_text = event_data
        wire_time = datetime.now(timezone.utc).strftime("%H:%M:%S")
    else:
        raw_text = event_data.get('story') or event_data.get('headline') or event_data.get('text') or ''
        wire_time = event_data.get('timestamp') or datetime.now(timezone.utc).strftime("%H:%M:%S")

    cleaned = raw_text.replace("High speed wire update.", "").replace("[M82]", "").strip()
    cleaned = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', '', cleaned).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)

    if not cleaned or len(cleaned) < 5 or "Dynamic signal update" in cleaned:
        return None

    headline_short = cleaned[:85] if len(cleaned) > 85 else cleaned
    h_lower = cleaned.lower()

    if any(k in h_lower for k in ["crude","oil","brent","wti","tanker","vlcc","faja","freight","maritime"]):
        desk, thesis = "MARITIME", "Faja / Freight Export Flow"
    elif any(k in h_lower for k in ["treasury","tlt","yield","rikg","bond","auction","fed","rate","cpi"]):
        desk, thesis = "TREASURY", "Ajuste Curva & Duracion"
    elif any(k in h_lower for k in ["jpm","bac","xlf","bank","sec","compliance","laundering"]):
        desk, thesis = "BANKING", "Financials Basket Compliance"
    elif any(k in h_lower for k in ["arm","apple","openai","asml","semi","chip","tech","ai","hardware","vla","abstraction"]):
        desk, thesis = "TECH_AI", "Semiconductors & AI Valuation"
    elif any(k in h_lower for k in ["houthi","strike","missile","war","sanction","china","geopol","defense"]):
        desk, thesis = "GEOPOL", "Geopol Friction & Supply"
    else:
        desk, thesis = "MACRO", "Macro Pulse Scan"

    return {"desk": desk[:12], "timestamp": wire_time, "headline": headline_short, "thesis": thesis[:35]}

def format_x_telemetry(lseg):
    card = (
        f"⚡ #M82 VIVA 60S :: {lseg['timestamp']} ET\n"
        f"🏛 [{lseg['desk']}] {lseg['headline']}\n"
        f"🎯 {lseg['thesis']}\n"
        f"🔒 CUSTODIA PASIVA — CPI 08:30 ET\n"
        f"#M82TOP"
    )
    if len(card) > 240:
        over = len(card) - 240
        trimmed = lseg['headline'][:max(10, len(lseg['headline'])-over-3)] + "..."
        card = (
            f"⚡ #M82 VIVA 60S :: {lseg['timestamp']} ET\n"
            f"🏛 [{lseg['desk']}] {trimmed}\n"
            f"🎯 {lseg['thesis']}\n"
            f"🔒 CUSTODIA PASIVA — CPI 08:30 ET\n"
            f"#M82TOP"
        )
    return card

def get_font(size):
    for p in ["/system/fonts/Roboto-Bold.ttf","/system/fonts/DroidSans-Bold.ttf","/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def render_master_card(parsed):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#0b0f19')
    draw = ImageDraw.Draw(img)
    font_meta, font_sub, font_header, font_main, font_footer = get_font(24), get_font(28), get_font(36), get_font(42), get_font(32)
    draw.rectangle([25,25,width-25,height-25], outline='#1e293b', width=2)
    draw.rectangle([35,35,width-35,110], fill='#0f172a')
    draw.text((60,50), "M82 SOVEREIGN MONITOR // V60.3 X-READY", fill='#38bdf8', font=font_meta)
    draw.text((60,78), f"LSEG WIRE // {parsed['desk']}", fill='#94a3b8', font=font_meta)
    draw.line([(35,110),(width-35,110)], fill='#0284c7', width=3)
    draw.text((60,220), "🚨 BREAKING WIRE TELEMETRY", fill='#ef4444', font=font_header)
    lines = textwrap.wrap(parsed['headline'], width=30)
    y=310
    for line in lines[:10]:
        draw.text((60,y), line, fill='#ffffff', font=font_main)
        y+=60
    draw.rectangle([35,height-120,width-35,height-35], fill='#0f172a')
    draw.text((60,height-100), f"[ THESIS: {parsed['thesis']} ]", fill='#38bdf8', font=font_meta)
    draw.text((60,height-65), "🏛 @MolinaHoldings | Sovereign Node", fill='#f8fafc', font=font_footer)
    img.save(IMG_PATH)
    try: shutil.copy(IMG_PATH, os.path.join(GALLERY_DIR, f"M82_{parsed['desk']}_{int(time.time())}.png"))
    except: pass
    return IMG_PATH

def dispatch_single_photo(source, raw_headline, rec_id):
    parsed = parse_lseg_event(raw_headline)
    if not parsed: return True
    img_file = render_master_card(parsed)
    caption = format_x_telemetry(parsed)
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(img_file, 'rb') as photo:
            r = requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo}, timeout=15)
            if r.status_code == 200:
                print(f"✅ [200 OK] [{parsed['desk']}] ({len(caption)}c) ID {rec_id} | {parsed['headline'][:50]}")
                return True
            elif r.status_code == 429:
                print("⚠️ 429 Rate Limit, 10s sleep")
                time.sleep(10)
            else:
                print(f"⚠️ {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"⚠️ EXC: {e}")
    return False

def flush_all_pending():
    if not os.path.exists(DB_PATH): return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status='PENDING' ORDER BY id ASC;")
    rows = c.fetchall()
    if rows:
        print(f"🚀 [FLUSH V60.3 X-Ready] {len(rows)} eventos")
        for rec_id, source, headline in rows:
            if "High speed wire update" in headline and len(headline) < 40:
                c.execute("UPDATE m82_multi_stream SET status='DISCARDED' WHERE id=?", (rec_id,))
                conn.commit()
                continue
            if dispatch_single_photo(source, headline, rec_id):
                c.execute("UPDATE m82_multi_stream SET status='DISPATCHED' WHERE id=?", (rec_id,))
                conn.commit()
                time.sleep(3.5)
    conn.close()

if __name__ == "__main__":
    print("🚀 [M82 V60.3 X-Ready Engine] Loop 10s | 240c hard cap | #M82TOP")
    while True:
        try: flush_all_pending()
        except Exception as e: print(f"⚠️ Loop: {e}")
        time.sleep(10)
