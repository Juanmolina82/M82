#!/usr/bin/env python3
import os, sys, time, sqlite3, subprocess, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [M82-UNIFIED] {msg}", flush=True)

def run_task(script_name):
    path = os.path.expanduser(f"~/M82/{script_name}")
    if os.path.exists(path):
        try:
            # Se ejecuta secuencialmente (un proceso a la vez) para no saturar Android
            subprocess.run(["python3", path], check=False, timeout=30)
        except Exception as e:
            log(f"⚠️ Error en {script_name}: {e}")

def main():
    log("🚀 Motor Unificado M82 Iniciado (Modo Anti-Colapso / 1 solo proceso maestro).")
    
    # Lista de tareas a correr en secuencia limpia
    tasks = [
        "m82_refinitiv_ws.py",
        "m82_unga_summit_tracker_daemon.py",
        "m82_wifi_health_daemon.py",
        "m82_core_orchestrator.py"
    ]

    while True:
        for task in tasks:
            run_task(task)
            time.sleep(2) # Pausa ligera entre tareas
            
        time.sleep(10) # Reposo del motor antes de la siguiente vuelta

if __name__ == "__main__":
    main()
