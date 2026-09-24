#!/usr/bin/env python3
import os, math, random, textwrap
from PIL import Image, ImageDraw, ImageFont

def generate_exact_m82_card(headline, source, row_id):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#050811')
    draw = ImageDraw.Draw(img)

    # 1. Fondo de Red y Constelaciones
    random.seed(row_id * 101 if isinstance(row_id, int) else 101)
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
            if dist < 240:
                draw.line([(x1, y1), (x2, y2)], fill='#0f2038', width=1)

    for x, y in nodes:
        draw.ellipse([x-2, y-2, x+2, y+2], fill='#38bdf8')

    # 2. Marcadores de esquina (Reticles)
    b_len, b_pad, b_color, b_w = 20, 30, '#1e293b', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # 3. Carga de Fuentes
    def get_font(name, size):
        font_paths = [
            f"/data/data/com.termux/files/usr/share/fonts/TTF/{name}.ttf",
            f"/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/{name}.ttf",
            f"{name}.ttf"
        ]
        for p in font_paths:
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except: pass
        return ImageFont.load_default()

    font_meta   = get_font("DejaVuSans", 13)
    font_header = get_font("DejaVuSans-Bold", 26)
    font_title  = get_font("DejaVuSerif", 38)
    font_brand  = get_font("DejaVuSans-Bold", 32)
    font_sub    = get_font("DejaVuSans", 20)

    # 4. Encabezado
    draw.text((60, 65), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#334155', font=font_meta)
    
    header_text = "#M82 BREAKING "
    source_tag  = f"[{str(source).upper()}]"
    
    draw.text((60, 98), header_text, fill='#ef4444', font=font_header)
    
    try:
        bbox = font_header.getbbox(header_text)
        h_width = bbox[2] - bbox[0]
    except:
        h_width = 210
        
    draw.text((60 + h_width, 98), source_tag, fill='#ef4444', font=font_header)
    draw.line([(60, 145), (740, 145)], fill='#1e293b', width=1)

    # 5. Ajuste Dinámico del Titular (Evita cortes de imagen)
    wrapped_lines = textwrap.wrap(headline, width=25)
    
    if len(wrapped_lines) > 4:
        font_title = get_font("DejaVuSerif", 32)
        wrapped_lines = textwrap.wrap(headline, width=30)

    y_pos = 280
    line_spacing = 54 if len(wrapped_lines) > 4 else 66
    
    for line in wrapped_lines[:5]:
        draw.text((60, y_pos), line, fill='#ffffff', font=font_title)
        y_pos += line_spacing

    # 6. Pie de Página y Firma
    draw.text((60, 825), "[ AGI QUANTUM VERIFIED ]", fill='#1d4ed8', font=font_meta)
    
    brand_main = "@MolinaHoldings"
    draw.text((60, 860), brand_main, fill='#ffffff', font=font_brand)
    
    try:
        b_bbox = font_brand.getbbox(brand_main)
        b_w = b_bbox[2] - b_bbox[0]
    except:
        b_w = 320
        
    draw.text((60 + b_w + 12, 868), "LLC", fill='#64748b', font=font_sub)

    out_path = os.path.expanduser("~/M82/m82_card_preview.png")
    img.save(out_path)
    print(f"✅ Imagen corregida generada con éxito en: {out_path}")

if __name__ == "__main__":
    generate_exact_m82_card("Octopus Renewables H1 2026 Slides: Cash Beats Budget, Nav Falls 5%", "LSEG_GREEN_MARK", 101)
