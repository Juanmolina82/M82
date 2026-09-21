import sqlite3
import os
import subprocess
from m82_card_publisher import create_m82_agi_quantum_card

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Directorio nativo de la Galería de fotos de Android
GALLERY_DIR = "/sdcard/DCIM/M82_Cards"
os.makedirs(GALLERY_DIR, exist_ok=True)

def export_latest_to_gallery():
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró la base de datos.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, headline FROM m82_multi_stream ORDER BY rowid DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("⚠️ No se encontraron registros.")
        return

    row_id, headline = row
    target_img_path = os.path.join(GALLERY_DIR, f"M82_Card_{row_id}.png")

    # 1. Generar la imagen en alta resolución dentro de DCIM
    create_m82_agi_quantum_card(headline, target_img_path)

    # 2. Forzar actualización inmediata en la Galería de Android
    try:
        subprocess.run(['termux-media-scan', target_img_path], stderr=subprocess.DEVNULL)
    except Exception:
        pass

    print("===================================================================")
    print("      🖼️  TARJETA GUARDADA EN LA GALERÍA DEL TELÉFONO              ")
    print("===================================================================")
    print(f"📁 Ruta: {target_img_path}")
    print("✨ Ya la puedes seleccionar directamente en Twitter/X o WhatsApp.")
    print("===================================================================")

if __name__ == "__main__":
    export_latest_to_gallery()
