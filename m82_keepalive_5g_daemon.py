#!/usr/bin/env python3
import os, sys, time, subprocess, requests

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [5G-KEEPALIVE] {msg}", flush=True)

def enable_wake_lock():
    try:
        subprocess.run(["termux-wake-lock"], check=False)
        log("🔒 Wake Lock de Termux activado.")
    except Exception as e:
        log(f"⚠️ No se pudo ejecutar termux-wake-lock: {e}")

def keep_connection_alive():
    # 1. Enviar ping ultraligero para sostener la antena activa
    try:
        subprocess.run(["ping", "-c", "2", "-w", "3", "1.1.1.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    # 2. Mantener la sesión HTTP caliente mediante una petición ligera
    try:
        r = requests.get("https://1.1.1.1", timeout=3)
        if r.status_code == 200:
            log("⚡ Enlace 5G/LTE activo y respondiendo correctamente.")
    except Exception as e:
        log(f"⚠️ Intermitencia detectada en red: {e}")

def main():
    enable_wake_lock()
    log("🚀 Daemon 5G Keep-Alive y Estabilización de Red Iniciado.")
    while True:
        keep_connection_alive()
        time.sleep(10) # Intervalo corto para evitar suspensiones de radiofrecuencia

if __name__ == "__main__":
    main()
