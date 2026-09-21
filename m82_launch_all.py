#!/usr/bin/env python3
import time
import subprocess
from m82_daemon_factory import RSS_MAP

def run_all():
    print("🌐 [M82 FACTORY] Iniciando barrido completo de demonios principales...", flush=True)
    for daemon_name in RSS_MAP.keys():
        try:
            print(f"📡 Ejecutando demonio: {daemon_name}", flush=True)
            subprocess.run(["python3", "/data/data/com.termux/files/home/M82/m82_daemon_factory.py", daemon_name], timeout=20)
        except Exception as e:
            print(f"⚠️ Error en {daemon_name}: {e}", flush=True)

if __name__ == "__main__":
    while True:
        run_all()
        time.sleep(300) # Barrido cada 5 minutos
