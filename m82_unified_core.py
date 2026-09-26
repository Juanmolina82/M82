#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, textwrap, gc, math, random, shutil
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.expanduser("~/M82/level3_fusion"))
sys.path.append(os.path.expanduser("~/M82/level4_verify"))
sys.path.append(os.path.expanduser("~/M82/level5_resilience"))

# Importación dinámica de módulos/daemons
import glob
import importlib.util

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] [M82-LITE] {msg}", flush=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

# 1. EJECUCIÓN SECUENCIAL DE DAEMONS (Ahorro masivo de RAM y CPU)
def run_ingestion_daemons():
    daemon_files = glob.glob(os.path.expanduser("~/M82/m82_*.py"))
    for file_path in daemon_files:
        bname = os.path.basename(file_path)
        if bname in ["m82_core_orchestrator.py", "m82_unified_core.py", "m82_db_patch.py"]:
            continue
        try:
            # Cargar y ejecutar módulo dinámicamente si tiene función main/run
            mod_name = bname.replace(".py", "")
            spec = importlib.util.spec_from_file_location(mod_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "fetch_data"):
                mod.fetch_data()
            elif hasattr(mod, "run"):
                mod.run()
        except Exception as e:
            log(f"⚠️ Error leve en daemon {bname}: {e}")

# 2. GENERACIÓN LIGERA DE IMÁGENES
def generate_card(headline, source, confidence_score, evidence_hash):
    img = Image.new('RGB', (800, 1000), color='#070b12')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    draw.rectangle([25, 25, 775, 975], outline='#1e293b', width=2)
    draw.text((50, 50), f"SYSTEM: AGI-CORE // CONF: {confidence_score}%", fill='#22c55e', font=font)
    draw.text((50, 80), f"#M82 [{str(source).upper()}]", fill='#ef4444', font=font)

    lines = textwrap.wrap(headline.title(), width=35)
    y_text = 150
    for line in lines:
        if y_text > 750: break
        draw.text((50, y_text), line, fill='#ffffff', font=font)
        y_text += 30

    draw.text((50, 820), f"HASH: {evidence_hash[:32]}...", fill='#64748b', font=font)
    draw.text((50, 860), "@MolinaHoldings LLC", fill='#f8fafc', font=font)

    img.save(IMG_PATH)
    shutil.copy(IMG_PATH, os.path.join(GALLERY_DIR, f"CARD_{int(time.time())}.png"))
    
    # Liberar memoria de la imagen
    del img, draw
    gc.collect()
    return IMG_PATH

def send_telegram(photo_path, caption):
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"},
                files={'photo': photo}, timeout=10
            )
            return r.status_code == 200
    except Exception:
        return False

# 3. PIPELINE Y CICLO ÚNICO DE TRABAJO
def master_cycle():
    # Paso A: Ejecutar ingestión secuencial
    run_ingestion_daemons()
    
    # Paso B: Procesar señales pendientes en DB
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, daemon_source, unified_summary FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 3")
    rows = cursor.fetchall()

    for row in rows:
        row_id, source, summary = row
        summary = summary or "Nueva actualización detectada por red M82."
        ev_hash = f"hash_{int(time.time())}_{row_id}"
        
        card_img = generate_card(summary, source, 95, ev_hash)
        caption = f"🚨 *#M82 BREAKING*\n🔴 *[{source}]*\n{summary}\n\n🏛 @MolinaHoldings LLC"
        
        if send_telegram(card_img, caption):
            cursor.execute("UPDATE m82_multi_stream SET status = 'PROCESSED' WHERE id = ?", (row_id,))
            conn.commit()
            log(f"✅ Notificación enviada para ID {row_id}")
        
    conn.close()
    gc.collect() # Limpieza forzada de RAM

def main():
    log("🚀 MOTOR UNIFICADO ULTRALIGERO M82 OPERATIVO")
    while True:
        try:
            master_cycle()
        except Exception as e:
            log(f"❌ Error en ciclo: {e}")
        time.sleep(15) # Pausa táctica para no sobrecargar el CPU de Termux

if __name__ == "__main__":
    main()
