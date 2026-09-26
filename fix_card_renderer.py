import os, sys, textwrap, random, math
from PIL import Image, ImageDraw, ImageFont

IMG_PATH = os.path.expanduser("~/M82/m82_card.png")

def generate_card_image(headline, source="AGI_FUSED_CORE", confidence_score=95, evidence_hash="d48125ffe09dae94"):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    # 1. Red de nodos cibernética de fondo
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

    # 2. Carga segura de fuentes
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
                font_meta = ImageFont.truetype(path, 16)
                font_header = ImageFont.truetype(path, 24)
                font_brand = ImageFont.truetype(path, 32)
                break
            except Exception:
                pass

    if not font_title:
        font_title = font_meta = font_header = font_brand = ImageFont.load_default()

    # 3. Encabezados de M82 Stream
    draw.text((60, 50), f"SYSTEM: AGI-CORE // QUANTUM VERIFIED ({confidence_score}%)", fill='#22c55e', font=font_meta)
    draw.text((60, 85), f"#M82 BREAKING [{str(source).upper()}]", fill='#ef4444', font=font_header)
    draw.line([(60, 125), (740, 125)], fill='#1e293b', width=2)

    # 4. Caja de Texto Principal con Contraste Elevado
    draw.rectangle([50, 160, 750, 750], fill='#0d1527', outline='#1e293b', width=2)

    # Wrap del texto para asegurar visibilidad sin desbordamiento
    formatted_headline = headline.strip()
    lines = textwrap.wrap(formatted_headline, width=28)
    
    y_text = 200
    for line in lines:
        if y_text < 700:  # Evita escribir fuera de la caja
            draw.text((80, y_text), line, fill='#ffffff', font=font_title)
            y_text += 50

    # 5. Pie de página y Firma Cryptográfica
    draw.text((60, 780), f"HASH PROOF: {evidence_hash}", fill='#38bdf8', font=font_meta)
    draw.line([(60, 820), (740, 820)], fill='#1e293b', width=1)
    
    draw.text((60, 850), "@MolinaHoldings LLC", fill='#ffffff', font=font_brand)

    img.save(IMG_PATH)
    print(f"✅ Tarjeta M82 generada y corregida en: {IMG_PATH}")
    return IMG_PATH

if __name__ == "__main__":
    test_headline = "FUSIÓN CRÍTICA: Multi-vector (5 eventos). Citgo License bridge to Nov 5 / Hormuz risk premium / Venezuelan crude production constraints."
    generate_card_image(test_headline)
