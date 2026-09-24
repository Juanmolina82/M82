#!/usr/bin/env python3
import time, os, subprocess

print("🚀 [M82 UNIFIED ENGINE] Iniciando motor unificado de bajo consumo...", flush=True)

while True:
    try:
        # 1. Ejecutar evaluador de estrés y block trades
        subprocess.run(["python3", os.path.expanduser("~/M82/m82_stress_score.py")], check=False)
        
        # 2. Despachar alertas
        subprocess.run(["python3", os.path.expanduser("~/M82/m82_high_frequency.py")], check=False)
        
    except Exception as e:
        print(f"⚠️ Error en ciclo: {e}", flush=True)
    
    # Pausa de 15 segundos para no saturar la RAM ni activar el Signal 9 de Android
    time.sleep(15)
