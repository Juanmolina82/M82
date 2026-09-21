import os, math, random, textwrap
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False, monospace=False):
    if monospace:
        paths = ["/system/fonts/DroidSansMono.ttf", "/system/fonts/NotoSansMono-Regular.ttf"]
    elif bold:
        paths = ["/system/fonts/NotoSerif-Bold.ttf", "/system/fonts/Times-Bold.ttf", "/system/fonts/DroidSans-Bold.ttf"]
    else:
        paths = ["/system/fonts/NotoSerif-Regular.ttf", "/system/fonts/Times.ttf", "/system/fonts/DroidSans.ttf"]
        
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def create_m82_agi_quantum_card(title, output_path):
    output_path = os.path.expanduser(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    W, H = 1080, 1350
    bg_color     = (6, 9, 15)       
    red_alert    = (235, 45, 45)     
    cyan_quantum = (0, 230, 255)    
    white_title  = (248, 250, 252)  
    gray_sub     = (130, 145, 165)  

    img = Image.new("RGB", (W, H), color=bg_color)
    draw = ImageDraw.Draw(img, "RGBA")

    # 1. Malla Cuántica de Fondo
    grid_step = 60
    for x in range(0, W, grid_step):
        draw.line([(x, 0), (x, H)], fill=(0, 230, 255, 8), width=1)
    for y in range(0, H, grid_step):
        draw.line([(0, y)], fill=(0, 230, 255, 8), width=1)

    # 2. Constelación de Nodos
    random.seed(hash(title) % 10000)
    nodes = [(random.randint(60, W-60), random.randint(60, H-60)) for _ in range(28)]
    for i, (nx, ny) in enumerate(nodes):
        draw.ellipse([nx-3, ny-3, nx+3, ny+3], fill=(0, 230, 255, 50))
        for j, (nx2, ny2) in enumerate(nodes[i+1:], i+1):
            dist = math.hypot(nx-nx2, ny-ny2)
            if dist < 210:
                alpha = int((1 - dist/210) * 28)
                draw.line([(nx, ny), (nx2, ny2)], fill=(0, 230, 255, alpha), width=1)

    # 3. Corchetes HUD Cian en las 4 Esquinas
    margin, cl = 35, 35
    for (cx, cy, dx1, dy1, dx2, dy2) in [
        (margin, margin, cl, 0, 0, cl),
        (W-margin, margin, -cl, 0, 0, cl),
        (margin, H-margin, cl, 0, 0, -cl),
        (W-margin, H-margin, -cl, 0, 0, -cl)
    ]:
        draw.line([(cx, cy), (cx+dx1, cy+dy1)], fill=cyan_quantum, width=3)
        draw.line([(cx, cy), (cx+dx2, cy+dy2)], fill=cyan_quantum, width=3)

    # 4. Fuentes
    font_mono_sm  = get_font(22, monospace=True)
    font_head     = get_font(52, bold=True)
    font_title    = get_font(60)
    font_brand    = get_font(44, bold=True)
    font_footer   = get_font(36)

    # 5. Encabezado y Telemetría
    telemetry_str = "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms"
    draw.text((90, 75), telemetry_str, fill=(0, 230, 255, 180), font=font_mono_sm)

    draw.text((90, 125), "#M82 BREAKING STREAM", fill=red_alert, font=font_head)
    draw.line([(90, 195), (W-90, 195)], fill=(0, 230, 255, 60), width=1)

    # 6. Titular Serif Grande
    lines = textwrap.wrap(title, width=27)
    y_text = 410 if len(lines) <= 3 else 340
    for line in lines[:6]:
        draw.text((90, y_text), line, fill=white_title, font=font_title)
        y_text += 85

    # 7. Pie de Página
    draw.line([(90, 1170), (W-90, 1170)], fill=(0, 230, 255, 60), width=1)
    draw.text((90, 1190), "[ AGI QUANTUM VERIFIED ]", fill=(0, 230, 255, 200), font=font_mono_sm)

    x_pos, y_pos = 90, 1230
    draw.text((x_pos, y_pos), "@MolinaHoldings", fill=(255, 255, 255), font=font_brand)
    try:
        brand_width = draw.textlength("@MolinaHoldings", font=font_brand)
    except AttributeError:
        brand_width = font_brand.getsize("@MolinaHoldings")[0]
        
    draw.text((x_pos + brand_width, y_pos + 4), " LLC", fill=gray_sub, font=font_footer)

    img.save(output_path, quality=95)
    return output_path
