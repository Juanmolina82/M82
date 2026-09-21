from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_m82_card(headline, category, output_path):
    # Dimensiones estilo cuadrado Instagram/Twitter (1080x1080)
    width, height = 1080, 1080
    bg_color = (168, 12, 26)  # Rojo oscuro institucional
    white = (255, 255, 255)
    
    # Crear lienzo base
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Cargar fuentes del sistema o usar default si no se encuentran
    try:
        font_title = ImageFont.truetype("serif", 75)
        font_body = ImageFont.truetype("serif", 50)
        font_box = ImageFont.truetype("serif", 48)
        font_footer = ImageFont.truetype("sans-serif", 35)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_box = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # 1. Encabezado Título
    title_text = "MARKET ALERT"
    draw.text((width // 2, 180), title_text, fill=white, font=font_title, anchor="mm")
    
    # Línea separadora decorativa
    draw.line([(120, 240), (width - 120, 240)], fill=white, width=4)

    # 2. Titular Principal (Ajuste de texto/Word wrap)
    lines = textwrap.wrap(headline, width=28)
    y_text = 340
    for line in lines[:4]: # Máximo 4 líneas
        draw.text((width // 2, y_text), line, fill=white, font=font_body, anchor="mm")
        y_text += 65

    # 3. Franja Blanca inferior (Estilo Americano)
    box_top = 700
    box_bottom = 810
    box_left = 100
    box_right = width - 100
    
    # Dibujar la caja blanca
    draw.rectangle([box_left, box_top, box_right, box_bottom], fill=white)
    
    # Texto dentro de la caja blanca (Categoría)
    category_text = category.upper()
    draw.text((width // 2, (box_top + box_bottom) // 2), category_text, fill=bg_color, font=font_box, anchor="mm")

    # 4. Pie de página (Footer)
    footer_text = "alerts & insights: @MolinaHoldings LLC"
    draw.text((width // 2, 960), footer_text, fill=white, font=font_footer, anchor="mm")

    # Guardar imagen resultante
    img.save(output_path)
    print(f"🖼️ Tarjeta generada exitosamente en: {output_path}")

if __name__ == "__main__":
    # Prueba del generador con datos de la ingesta
    test_headline = "Panama Canal stress shows the real shipping squeeze may still be ahead"
    test_category = "COMMODITIES & LOGISTICS"
    os.makedirs(os.path.expanduser("~/M82/output_cards"), exist_ok=True)
    create_m82_card(test_headline, test_category, os.path.expanduser("~/M82/output_cards/test_alert.png"))
