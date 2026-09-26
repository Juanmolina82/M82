import sqlite3, os, subprocess

db_path = os.path.expanduser("~/M82/m82_database.db")

print("🔧 Aplicando WAL y aumentando el timeout de colisiones...")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Activar el modo WAL para permitir lecturas y escrituras concurrentes
        cursor.execute("PRAGMA journal_mode=WAL;")
        journal_mode = cursor.fetchone()[0]
        
        # Aumentar tiempo de espera por bloqueo a 30.000 ms (30 segundos)
        cursor.execute("PRAGMA busy_timeout=30000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        
        conn.commit()
        conn.close()
        print(f"✅ Configuración exitosa. Modo Journal: {journal_mode}")
    except Exception as e:
        print(f"❌ Error al configurar SQLite: {e}")
else:
    print("⚠️ Base de datos no encontrada. Se inicializará en la primera escritura.")
