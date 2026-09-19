import sqlite3
import os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def fix_ric_tas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Actualización del RIC madre exacto sin espacios
    c.execute("""
        UPDATE m82_lseg_instruments 
        SET ric_code = '0#CLT:' 
        WHERE param_key = 'RIC_TAS'
    """)
    
    conn.commit()
    conn.close()
    print("✅ RIC madre de TAS corregido a '0#CLT:' en m82_database.db")

if __name__ == "__main__":
    fix_ric_tas()
