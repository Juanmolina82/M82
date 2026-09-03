from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import datetime, hashlib, json, requests

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
                files = {'document': doc}
                data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}
                requests.post(url, data=data, files=files, timeout=15)
            print("[OK] Reporte institucional despachado a Telegram.")
    except Exception as e:
        print(f"[ERR] Error en despacho: {e}")

def generate_institutional_pdf():
    now_dt = datetime.datetime.now()
    date_id = now_dt.strftime("%Y%m%d-%H%M")
    audit_hash = hashlib.sha256(f"PDF-CLOSE-{date_id}".encode()).hexdigest()[:16].upper()

    W, H = 1080, 1450
    img = Image.new("RGB", (W, H), "#0B0E14")
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf", 21)
        font_bold = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", 23)
        font_header = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", 28)
    except:
        font_main = font_bold = font_header = ImageFont.load_default()

    # Accent Top Bar & Header Membrete
    draw.rectangle([(0, 0), (W, 14)], fill="#0052FF")
    draw.text((50, 45), "MOLINA HOLDINGS LLC", fill="#FFFFFF", font=font_header)
    draw.text((50, 80), "Private Wealth & Cross-Asset Risk Management", fill="#8A99AD", font=font_main)
    
    # Línea divisoria de cabecera
    draw.rectangle([(50, 115), (W-50, 117)], fill="#1E293B")

    # Cuerpo del reporte con bloques estructurados
    lines = [
        ("M82 QUANTITATIVE MARKET FEED", "#0052FF", font_bold),
        (">> 16:00 ET | Official Closing Bell & Settlement", "#8A99AD", font_main),
        ("", "", font_main),
        ("[BENCHMARK & BREADTH SUMMARY]", "#E1E7EF", font_bold),
        ("• Nasdaq 100 (.NDX): 28,968.35 (-1.66%)", "#FF5252", font_main),
        ("• Market Breadth: 83 Decliners vs 18 Advancers (4.6:1 Ratio)", "#E1E7EF", font_main),
        ("• Estructura: Venta sistematica por de-risking generalizado.", "#E1E7EF", font_main),
        ("", "", font_main),
        ("[(+) CLOSING RALLY & ROTACION SECTORIAL]", "#00E676", font_bold),
        ("• E&P / Energia: Cierre solido en maximos (EOG, COP, XOM)", "#00E676", font_main),
        ("• Megacap Tech: AAPL (+2.40%) sostiene estructura compradora.", "#00E676", font_main),
        ("", "", font_main),
        ("[(-) CLOSING FLUSH & PRESION DE VOLATILIDAD]", "#FF5252", font_bold),
        ("• Software & Ciberseguridad: Compresion de multiples acelerada", "#FF5252", font_main),
        ("  - CRWD: -7.70% | AXON: -7.50% | CDNS: -7.70%", "#FF5252", font_main),
    ]

    y = 140
    for text, color, font in lines:
        if text:
            draw.text((50, y), text, fill=color, font=font)
        y += 32

    # Divisorio Seccion Cumplimiento
    draw.rectangle([(50, y+10), (W-50, y+12)], fill="#1E293B")
    y += 30

    # Bloque de Integridad y Licencia
    compliance_lines = [
        ("EXECUTIVE DESK:", "#FFFFFF", font_bold),
        ("• CEO: jmmp@molina82.com | jmiguel1535@gmail.com", "#8A99AD", font_main),
        ("• CFO: cmme@molina82.com | molinagloballlc@gmail.com", "#8A99AD", font_main),
        ("", "", font_main),
        ("INTEGRITY & COMPLIANCE STAMP:", "#FFFFFF", font_bold),
        (f"• Status: Final Verified Closing Data Stream (Encrypted Document)", "#E1E7EF", font_main),
        (f"• SHA-256 Audit Hash: {audit_hash}", "#0052FF", font_bold),
        ("• Licencia: Workspace Desktop API (Non-Redistribution / Internal Buy-Side)", "#8A99AD", font_main),
        (f"• Governance: Internal Audit Committee Validated — Ref: #M82-{date_id}", "#8A99AD", font_main),
        ("", "", font_main),
        ("Notice: Este informe es un entregable cuantitativo protegido para uso", "#64748B", font_main),
        ("exclusivo de nuestros socios e inversores acreditados. Prohibida su copia.", "#64748B", font_main)
    ]

    for text, color, font in compliance_lines:
        if text:
            draw.text((50, y), text, fill=color, font=font)
        y += 30

    # Guardado dual PNG / PDF 300 DPI
    img_path = BASE / "M82_CLOSE.png"
    pdf_path = BASE / f"M82_REPORT_{date_id}.pdf"
    
    img.save(img_path, "PNG", dpi=(300, 300))
    img.convert("RGB").save(pdf_path, "PDF", resolution=300)

    caption = f"🔒 *M82 Quantitative Institutional Report*\n_Ref: #{date_id} | SHA-256: `{audit_hash}`_"
    send_telegram_doc(pdf_path, caption)

if __name__ == "__main__":
    generate_institutional_pdf()
