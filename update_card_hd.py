import re

orchestrator_path = "/root/M82/m82_core_orchestrator.py"
if not os.path.exists(orchestrator_path):
    orchestrator_path = os.path.expanduser("~/M82/m82_core_orchestrator.py")

new_generate_card_code = '''def generate_card_image(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#050811')
    draw = ImageDraw.Draw(img)

    # Red de nodos de fondo
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
                draw.line([(x1, y1), (x2, y2)], fill='#0d1b2a', width=1)

    for x, y in nodes:
        draw.ellipse([x-2, y-2, x+2, y+2], fill='#00b4d8')

    # Carga de fuentes HD con tamaño incrementado
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    
    font_title = font_meta = font_header = font_brand = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 42)
                font_meta = ImageFont.truetype(path, 16)
                font_header = ImageFont.truetype(path, 26)
                font_brand = ImageFont.truetype(path, 34)
                break
            except Exception:
                pass

    if not font_title:
        font_title = font_meta = font_header = font_brand = ImageFont.load_default()

    # Encabezados de M82
    draw.text((50, 45), "SYSTEM: AGI-CORE // QUANTUM VERIFIED (95%)", fill='#00f5d4', font=font_meta)
    draw.text((50, 75), f"#M82 BREAKING [{str(source).upper()}]", fill='#ff0055', font=font_header)
    draw.line([(50, 115), (750, 115)], fill='#1e293b', width=2)

    # Caja Contenedora HD de Alto Contraste
    draw.rectangle([40, 140, 760, 780], fill='#0b1326', outline='#00b4d8', width=2)

    # Formateo y Renderizado de Texto Principal
    formatted_headline = headline.strip()
    lines = textwrap.wrap(formatted_headline, width=32)
    
    y_text = 180
    for line in lines:
        if y_text < 730:
            draw.text((65, y_text), line, fill='#ffffff', font=font_title)
            y_text += 58

    # Pie de página y Firma
    draw.text((50, 810), f"HASH PROOF: {int(time.time())}xM82", fill='#00b4d8', font=font_meta)
    draw.line([(50, 840), (750, 840)], fill='#1e293b', width=1)
    draw.text((50, 870), "@MolinaHoldings LLC", fill='#ffffff', font=font_brand)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{row_id}_{int(time.time())}.png")
    shutil.copy(IMG_PATH, gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    log(f"📸 Tarjeta HD guardada en Galería: {gallery_file}")
    return IMG_PATH'''

