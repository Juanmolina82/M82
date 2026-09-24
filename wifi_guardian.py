#!/usr/bin/env python3
import time
import subprocess
import re

ROUTER_IP = "192.168.2.1"

def check_wifi_status():
    try:
        cmd = ["dumpsys", "wifi"]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        
        freq_match = re.search(r'mFrequency=(\d+)', output)
        link_speed_match = re.search(r'mLinkSpeed=(\d+)', output)
        
        freq = int(freq_match.group(1)) if freq_match else None
        speed = int(link_speed_match.group(1)) if link_speed_match else None
        
        return freq, speed
    except Exception:
        return None, None

def force_5g_reconnect():
    print("🚨 Caída a 2.4 GHz detectada. Reenganchando a la banda 5 GHz...", flush=True)
    try:
        subprocess.run(["cmd", "wifi", "set-wifi-enabled", "disabled"], check=False)
        time.sleep(2)
        subprocess.run(["cmd", "wifi", "set-wifi-enabled", "enabled"], check=False)
        print("🔄 Interfaz Wi-Fi reiniciada. Esperando enlace 5 GHz...", flush=True)
        time.sleep(5)
    except Exception as e:
        print(f"❌ Fallo al reconectar: {e}", flush=True)

def main():
    print(f"🛡️ Guardián de Banda M82 Iniciado | Router Target: {ROUTER_IP}", flush=True)
    while True:
        freq, speed = check_wifi_status()
        if freq:
            if freq < 5000:
                print(f"⚠️ Alerta: Conectado a {freq} MHz (2.4 GHz) | Velocidad: {speed} Mbps", flush=True)
                force_5g_reconnect()
            else:
                print(f"✅ Estable en 5 GHz ({freq} MHz) | Enlace: {speed} Mbps", flush=True)
        else:
            print("🔍 Monitoreando interfaz Wi-Fi...", flush=True)
        
        time.sleep(10)

if __name__ == "__main__":
    main()
