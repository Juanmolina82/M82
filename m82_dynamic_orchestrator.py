#!/usr/bin/env python3
import os, sys, time, glob, subprocess, sqlite3

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
BACKUP_DIR = os.path.join(M82_DIR, "backups")

os.makedirs(BACKUP_DIR, exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [M82-GUARD] {msg}", flush=True)

def backup_database():
    if os.path.exists(DB_PATH):
        try:
            backup_file = os.path.join(BACKUP_DIR, f"m82_db_backup_{int(time.time())}.db")
            conn = sqlite3.connect(DB_PATH)
            backup_conn = sqlite3.connect(backup_file)
            conn.backup(backup_conn)
            backup_conn.close()
            conn.close()
            log(f"💾 Base de datos respaldada correctamente en: {backup_file}")
            
            # Limpiar backups antiguos (conservar los últimos 10)
            backups = sorted(glob.glob(os.path.join(BACKUP_DIR, "m82_db_backup_*.db")))
            if len(backups) > 10:
                for old in backups[:-10]:
                    os.remove(old)
        except Exception as e:
            log(f"⚠️ Error al crear respaldo de BD: {e}")

def get_all_daemons():
    # Detecta automáticamente cualquier script Python que termine en _daemon.py o _v9.py
    patterns = [os.path.join(M82_DIR, "*_daemon.py"), os.path.join(M82_DIR, "*_scheduler_*.py")]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
    return sorted(list(set(files)))

def check_and_maintain_daemons():
    daemons = get_all_daemons()
    log(f"🔍 Escaneando infraestructura... {len(daemons)} demonios detectados.")
    
    for daemon_path in daemons:
        daemon_name = os.path.basename(daemon_path)
        
        # Verificar si el demonio está corriendo
        cmd = f"pgrep -f {daemon_name}"
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        
        if res.returncode != 0:
            log(f"⚡ [AUTO-RECOVERY] Levantando demonio: {daemon_name}")
            subprocess.Popen(["python3", "-u", daemon_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    log("==================================================")
    log("🛡️ SISTEMA DE PROTECCIÓN Y PERSISTENCIA M82 ACTIVO")
    log("==================================================")
    
    # Activar Wake Lock
    try:
        subprocess.run(["termux-wake-lock"], check=False)
        log("🔒 Termux Wake Lock Asegurado.")
    except Exception:
        pass

    backup_database()
    
    while True:
        check_and_maintain_daemons()
        time.sleep(10)

if __name__ == "__main__":
    main()
