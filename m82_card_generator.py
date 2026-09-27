#!/usr/bin/env python3
import os, time, textwrap, math, random, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont

IMG_PATH = os.path.expanduser("~/M82/m82_card_refinitiv.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

def build_hud_card():
    os.makedirs(GALLERY_DIR, exist_ok=True)
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Red neural táctica
    random.seed(82)
    nodes = [(random.randint(50, 750), random.randint(50, 950)) for _ in range(20)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 180:
                draw.line([(x1, y1), (x2, y2)], fill='#0f172a', width=1)

    # Marco
    draw.rectangle([25, 25, width-25, height-25], outline='#1e293b', width=2)

    # Texto principal
    draw.text((50, 45), "SYSTEM: AGI-CORE // REFINITIV MACRO FUSION", fill='#22c55e', font=font)
    draw.text((50, 75), "#M82 [REFINITIV / ORMUZ / VE-ZULIA]", fill='#ef4444', font=font)
    draw.line([(50, 115), (750, 115)], fill='#334155', width=2)

    draw.text((50, 135), "BRENT: $104.10 | WTI: $97.40 | DUBAI: $110.12", fill='#38bdf8', font=font)
    
    headline = "Tension en Ormuz (-38% flujo) compensada por auge del Hemisferio Occidental (John Kemp/NABEP). Deficit de 3,226 MW en Zulia impulsa consumo forzado de diesel."
    lines = textwrap.wrap(headline, width=35)
    
    y_text = 180
    for line in lines:
        draw.text((50, y_text), line, fill='#f8fafc', font=font)
        y_text += 25

    # Bloque de métricas
    draw.rectangle([50, 680, 750, 810], fill='#0f172a', outline='#334155', width=1)
    draw.text((70, 700), "• Flujo Real Ormuz: 6.98M bpd (Vs 20.7M bpd pre-guerra)", fill='#f1f5f9', font=font)
    draw.text((70, 730), "• Deficit Electrico VE: 3,226 MW (Deficit Zulia: 1,000 MW)", fill='#f1f5f9', font=font)
    draw.text((70, 760), "• Estructura de Mercado: Backwardation Extrema + Crack Spreads", fill='#f1f5f9', font=font)

    # Hash y Firma
    evidence_hash = "cbe9f6457aeccedbafa8c3299e0e2f7531c43d8c140532501717cc19fe4803a8"
    draw.line([(50, 840), (750, 840)], fill='#1e293b', width=1)
    draw.text((50, 860), f"SHA256: {evidence_hash[:36]}...", fill='#64748b', font=font)
    draw.text((50, 900), "@MolinaHoldings LLC // Macro-Quant OSINT", fill='#f8fafc', font=font)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_REFINITIV_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)
    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    print(f"🖼️ Tarjeta guardada en galería: {gallery_file}")

if __name__ == "__main__":
    build_hud_card()
