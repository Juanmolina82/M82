import sqlite3
import requests

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "1020305418"

def desplegar_plataforma_m82():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()

    # Tabla Snapshot
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        fecha TEXT PRIMARY KEY, wti_ref REAL, brent_rt REAL, ovx REAL,
        nav_ifrs REAL, nav_spot REAL, ltv_spot REAL)''')

    # Tabla Refinitiv ESG Metrics
    c.execute('''CREATE TABLE IF NOT EXISTS refinitiv_metrics (
        ticker TEXT PRIMARY KEY, fecha TEXT, esg_score REAL, esg_plus REAL,
        green_rev_pct REAL, governance_score REAL)''')

    # Tabla PE/VC Investments
    c.execute('''CREATE TABLE IF NOT EXISTS m82_pe_vc_investments (
        deal_id TEXT PRIMARY KEY, investee_company TEXT, invest_date TEXT,
        amount_usd_m REAL, fund_name TEXT, trbc_industry TEXT, stage TEXT,
        status TEXT, nation TEXT, region TEXT)''')

    # Tabla PE/VC Exits
    c.execute('''CREATE TABLE IF NOT EXISTS m82_pe_vc_exits (
        deal_id TEXT PRIMARY KEY, investee_company TEXT, exit_date TEXT,
        return_m REAL, fund_name TEXT, trbc_industry TEXT, nation TEXT,
        fund_status TEXT, state_region TEXT)''')

    # Registros Base
    c.execute("INSERT OR REPLACE INTO snapshot VALUES (datetime('now'), 92.43, 97.50, 32.50, 775.60, 810.46, 18.51)")
    c.execute("INSERT OR REPLACE INTO refinitiv_metrics VALUES ('AAPL.O', datetime('now'), 3.4, 3.3, 3.3, 4.0)")

    # Ingesta de Exits Refinitiv
    exits = [
        ('19830', 'Anobit Technologies Ltd', '20-Dec-2011', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Active', 'Non-US'),
        ('19202', 'ORBO, Inc.', '20-Jan-2007', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
        ('22536', 'Akamai Technologies, Inc.', '28-Oct-1999', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Massachusetts'),
        ('21838', 'Swiss Media Group Inc.', '27-May-1999', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Defunct', 'California'),
        ('21635', 'FUJIFILM Directs, Inc.', '01-May-1998', 22.50, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
        ('19977', 'Pillar Corporation', '07-Dec-1996', 22.01, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
        ('20108', 'Courier Technology', '24-Nov-1991', 30.00, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Massachusetts')
    ]
    c.executemany("INSERT OR REPLACE INTO m82_pe_vc_exits VALUES (?,?,?,?,?,?,?,?,?)", exits)

    conn.commit()
    conn.close()
    print("✅ Plataforma M82 integrada e inicializada con éxito.")

if __name__ == "__main__":
    desplegar_plataforma_m82()
