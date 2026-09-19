import sqlite3
from datetime import datetime

# Definir la ruta de la base de datos
DB_PATH = "m82_database.db"

def ingest_blk_profile():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # --- Ingesta de Datos Generales (Overview) ---
    c.execute('''CREATE TABLE IF NOT EXISTS m82_blk_profile (
        ticker TEXT PRIMARY KEY,
        company_name TEXT,
        market_cap_m REAL,
        shares_outstanding_m REAL,
        employees INTEGER,
        next_earn_date TEXT,
        last_updated TEXT
    )''')
    
    blk_general = ('BLK.N', 'BLACKROCK, INC.', 102148.06, 149.21, 19800, '13-Oct-2026', '07-Sep-2026')
    
    c.execute("INSERT OR REPLACE INTO m82_blk_profile VALUES (?, ?, ?, ?, ?, ?, ?)", blk_general)
    
    # --- Ingesta de Métricas Financieras (Key Metrics Historical) ---
    c.execute('''CREATE TABLE IF NOT EXISTS m82_blk_metrics (
        ticker TEXT,
        period_end TEXT,
        enterprise_value_m REAL,
        ebitda_m REAL,
        pe_ratio REAL,
        div_yield REAL,
        return_on_equity REAL,
        PRIMARY KEY (ticker, period_end)
    )''')
    
    # Datos extraídos de la sección de Key Metrics Historical
    blk_metrics = [
        ('BLK.N', 'FY 2024', 113426.0, 7881.0, 19.33, 2.50, 14.90),
        ('BLK.N', 'FY 2025', 110904.0, 8312.0, 17.80, 2.70, 15.20)
    ]
    
    c.executemany("INSERT OR REPLACE INTO m82_blk_metrics VALUES (?, ?, ?, ?, ?, ?, ?)", blk_metrics)
    
    conn.commit()
    conn.close()
    print("✅ Ingesta Modular M82: Perfil y Métricas Financieras de BLK.N registradas.")

if __name__ == "__main__":
    ingest_blk_profile()
