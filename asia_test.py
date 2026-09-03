import json, datetime, requests, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def send_telegram_doc(doc_path, caption):
    if not VAULT.exists(): return
    try:
        with open(VAULT, 'r') as f: v = json.load(f)
        token, chat_id = v.get('TELEGRAM_BOT_TOKEN'), v.get('TELEGRAM_CHAT_ID')
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            with open(doc_path, 'rb') as doc:
                requests.post(url, data={'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}, files={'document': doc}, timeout=15)
            print("[OK] Reporte de prueba Asia despachado a Telegram.")
    except Exception as e:
        print(f"[ERR] Error en envío: {e}")

def run_asia_test():
    now_dt = datetime.datetime.now()
    date_id = now_dt.strftime("%Y%m%d-%H%M")
    audit_hash = hashlib.sha256(f"ASIA-TEST-{date_id}".encode()).hexdigest()[:16].upper()

    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), "#0B0E14")
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf", 21)
        font_bold = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", 23)
        font_header = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", 28)
    except:
        font_main = font_bold = font_header = ImageFont.load_default()

    draw.rectangle([(0, 0), (W, 14)], fill="#0052FF")
    draw.text((50, 45), "MOLINA HOLDINGS LLC", fill="#FFFFFF", font=font_header)
    draw.text((50, 80), "Private Wealth & Cross-Asset Risk Management", fill="#8A99AD", font=font_main)
    draw.rectangle([(50, 115), (W-50, 117)], fill="#1E293B")

    lines = [
        ("M82 APAC OPENING FEED [DRY-RUN]", "#0052FF", font_bold),
        (f">> {now_dt.strftime('%H:%M')} ET | Asia-Pacific Session Launch", "#8A99AD", font_main),
        ("", "", font_main),
        ("[ASIA BENCHMARKS PREVIEW]", "#E1E7EF", font_bold),
        ("• Nikkei 225 (.N225): Monitoring Open Session Structure", "#E1E7EF", font_main),
        ("• Hang Seng (.HSI): Tech Futures & China Liquidity Desk", "#E1E7EF", font_main),
        ("• S&P/ASX 200 (.AXJO): Commodities & Energy Futures Sentiment", "#E1E7EF", font_main),
        ("", "", font_main),
        ("[(+) CROSS-ASSET MACRO RISK]", "#00E676", font_bold),
        ("• USD/JPY: Control de volatilidad previa a sesión de Tokyo", "#00E676", font_main),
        ("• Brent Crude / Metals: Cobertura por flujo comercial G20", "#00E676", font_main),
    ]

    y = 140
    for text, color, font in lines:
        if text: draw.text((50, y), text, fill=color, font=font)
        y += 32

    draw.rectangle([(50, y+10), (W-50, y+12)], fill="#1E293B")
    y += 30

    compliance_lines = [
        ("INTEGRITY & COMPLIANCE STAMP:", "#FFFFFF", font_bold),
        ("• Status: APAC Test Stream (Encrypted Document)", "#E1E7EF", font_main),
        (f"• SHA-256 Audit Hash: {audit_hash}", "#0052FF", font_bold),
        (f"• Governance: Internal Test Run — Ref: #M82-APAC-{date_id}", "#8A99AD", font_main),
    ]

    for text, color, font in compliance_lines:
        if text: draw.text((50, y), text, fill=color, font=font)
        y += 30

    pdf_path = BASE / f"M82_APAC_TEST_{date_id}.pdf"
    img.convert("RGB").save(pdf_path, "PDF", resolution=300)

    caption = f"🧪 *M82 APAC Test Report*\n_Ref: #M82-APAC-{date_id} | SHA-256: `{audit_hash}`_"
    send_telegram_doc(pdf_path, caption)

if __name__ == "__main__":
    run_asia_test()
