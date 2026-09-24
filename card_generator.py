#!/usr/bin/env python3
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

def generate_m82_card(headline, category="M82 BREAKING STREAM", source_tag="@MolinaHoldings LLC", output_path=None):
    # Dimensiones estándar para redes / feeds (1080x1080 HD)
    W, H = 1080, 1080
    
    # Colores profesionales
    BG_COLOR = (15, 20, 28)       # Azul oscuro profesional
    ACCENT_COLOR = (230, 57, 70)   # Rojo alerta corporativo
    TEXT_MAIN = (255, 255, 255)    # Blanco puro
    TEXT_MUTED = (160, 174, 192)  # Gris claro

    img = Image.new("RGB", (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuentes del sistema o por defecto
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_body = ImageFont.truetype("DejaVuSans-Bold.ttf", 52)
        font_tag = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        font_header = font_body = font_tag = ImageFont.load_default()

    # 1. Borde superior de acento
    draw.rectangle([(0, 0), (W, 16)], fill=ACCENT_COLOR)

    # 2. Encabezado / Categoría
    draw.text((60, 80), category.upper(), font=font_header, fill=ACCENT_COLOR)
    draw.line([(60, 140), (W - 60, 140)], fill=(40, 50, 65), width=2)

    # 3. Ajuste de texto del titular (Word Wrap adecuado)
    wrapped_lines = textwrap.wrap(headline, width=32)
    
    # Calcular centrado vertical para el texto
    line_height = 68
    total_text_height = len(wrapped_lines) * line_height
    start_y = (H - total_text_height) // 2

    for i, line in enumerate(wrapped_lines):
        y = start_y + (i * line_height)
        draw.text((60, y), line, font=font_body, fill=TEXT_MAIN)

    # 4. Pie de imagen / Fuente
    draw.line([(60, H - 140), (W - 60, H - 140)], fill=(40, 50, 65), width=2)
    draw.text((60, H - 100), source_tag, font=font_tag, fill=TEXT_MUTED)

    # Guardar la imagen limpia
    if not output_path:
        output_dir = os.path.expanduser("~/M82/cards")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "m82_clean_card.png")

    img.save(output_path, quality=95)
    print(f"✅ Tarjeta corregida generada en: {output_path}")
    return output_path

if __name__ == "__main__":
    test_headline = "Pound Sterling Price News and Forecast: GBP/USD loses its footing as BoE hold meets Fed hike"
    generate_m82_card(test_headline)
