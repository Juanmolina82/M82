import os, time, subprocess
from PIL import Image, ImageDraw, ImageFont

GALLERY_DIR = "/sdcard/Pictures/M82_Cards"
os.makedirs(GALLERY_DIR, exist_ok=True)

width, height = 800, 1000
img = Image.new('RGB', (width, height), color='#070b12')
draw = ImageDraw.Draw(img)

draw.rectangle([20, 20, width-20, height-20], outline='#10233b', width=2)
draw.line([(40, 120), (760, 120)], fill='#1f2937', width=1)

font_path = "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf"
if not os.path.exists(font_path):
    font_path = "/data/data/com.termux/files/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

try:
    font_header = ImageFont.truetype(font_path.replace("DejaVuSerif", "DejaVuSans-Bold"), 24)
    font_title = ImageFont.truetype(font_path, 36)
    font_body = ImageFont.truetype(font_path.replace("DejaVuSerif", "DejaVuSans"), 18)
    font_meta = ImageFont.truetype(font_path.replace("DejaVuSerif", "DejaVuSans"), 12)
    font_footer = ImageFont.truetype(font_path.replace("DejaVuSerif", "DejaVuSans-Bold"), 28)
except Exception:
    font_header = font_title = font_body = font_meta = font_footer = ImageFont.load_default()

draw.text((50, 45), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM", fill='#4b5563', font=font_meta)
draw.text((50, 75), "#M82 BREAKING // TRUMP-XI TRUCE TIMELINE", fill='#ef4444', font=font_header)
draw.text((50, 150), "TRUMP-XI TRADE TRUCE", fill='#38bdf8', font=font_title)

timeline_text = [
    "• Feb-Mar 2025: 20% Tariffs + Retaliation on LNG/Autos.",
    "• Apr 2025: Escalation to 125% Tariffs & Rare Earths Cut.",
    "• May 2025: Geneva Pause. Tariff Rollback to 30%.",
    "• Oct 2025: Korea Summit - Soybean/Fentanyl Truce.",
    "• Sep 2026 (NOW): White House Summit. Truce Extended.",
    "",
    "M82 PIVOT: Risk-On 90D Window. Rare Earths & Boeing Unlocked."
]

y_pos = 230
for line in timeline_text:
    draw.text((50, y_pos), line, fill='#e5e7eb', font=font_body)
    y_pos += 38

draw.line([(50, y_pos + 20), (750, y_pos + 20)], fill='#1f2937', width=1)
draw.text((50, 850), "[ AGI QUANTUM VERIFIED // GALLERY SYNCED ]", fill='#2563eb', font=font_meta)
draw.text((50, 885), "@MolinaHoldings LLC", fill='#ffffff', font=font_footer)

file_id = int(time.time())
gallery_path = os.path.join(GALLERY_DIR, f"M82_TRUMP_XI_TRUCE_{file_id}.png")
img.save(gallery_path)

try:
    subprocess.run(["termux-media-scan", gallery_path], check=False)
except Exception:
    pass

print(f"✅ Tarjeta guardada e indexada en Galería: {gallery_path}")
