import sqlite3
import os
import subprocess
from m82_card_publisher import create_m82_agi_quantum_card

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Rutas seguras mediante el enlace de almacenamiento de Termux
TELEGRAM_DIRS = [
    os.path.expanduser("~/storage/shared/Pictures/Telegram"),
    os.path.expanduser("~/storage/shared/Telegram"),
    "/sdcard/Pictures/Telegram"
]

# Intentar crear solo las rutas donde haya acceso de escritura
valid_dirs = []
for d in TELEGRAM_DIRS:
    try:
        os.makedirs(d, exist_ok=True)
        valid_dirs.append(d)
    except PermissionError:
        pass

if not valid_dirs:
    # Ruta fallback interna si no hay permisos otorgados
    fallback = os.path.expanduser("~/M82/output_cards")
    os.makedirs(fallback, exist_ok=True)
    valid_dirs.append(fallback)

def generate_all_cards_to_telegram():
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró m82_database.db")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, headline FROM m82_multi_stream ORDER BY rowid ASC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No hay registros para procesar.")
        return

    print(f"🚀 Generando {len(rows)} tarjetas directamente...")

    for row_id, headline in rows:
        filename = f"M82_Telegram_Card_{row_id}.png"
        
        for tgt_dir in valid_dirs:
            target_path = os.path.join(tgt_dir, filename)
            
            if not os.path.exists(target_path):
                create_m82_agi_quantum_card(headline, target_path)
                
                try:
                    subprocess.run(['termux-media-scan', target_path], stderr=subprocess.DEVNULL)
                except Exception:
                    pass

        print(f"✅ Tarjeta #{row_id} procesada.")

if __name__ == "__main__":
    generate_all_cards_to_telegram()
