import sqlite3

def registrar_deals_aapl():
    try:
        conn = sqlite3.connect("m82_database.db")
        c = conn.cursor()
        
        # Tabla M&A / Private Equity
        c.execute('''CREATE TABLE IF NOT EXISTS m82_deals (
            deal_id TEXT PRIMARY KEY,
            investee_company TEXT,
            invest_date TEXT,
            amount_usd_m REAL,
            fund_name TEXT,
            trbc_industry TEXT,
            stage TEXT,
            status TEXT,
            region TEXT
        )''')
        
        # Registro histórico extraído de Refinitiv Workspace
        deals = [
            ('340091804001', 'Anobit Technologies', '19-Nov-2010', 10.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Acquisition', 'California'),
            ('340090801001', 'ORBO, Inc.', '20-Jan-2007', 41.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Active', 'United States'),
            ('340090617001', 'Flashpoint Technology', '27-Oct-1999', 27.00, 'Apple Computer, Inc.', 'Basic Materials', 'Expansion', 'Active', 'New Hampshire'),
            ('340090331002', 'Akamai Technologies', '14-May-1999', 10.12, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Alert Public', 'Massachusetts'),
            ('340090175001', 'Swiss Media Group Inc.', '21-Dec-1998', 3.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Active', 'California'),
            ('340090008001', 'Pillar Corporation', '21-Oct-1997', 2.00, 'Apple Computer, Inc.', 'Technology', 'Later Stage', 'Acquisition', 'California'),
            ('340089839002', 'BIOCAD Corporation', '22-Aug-1997', 1.50, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Merger', 'California'),
            ('340089832002', 'Adobe Systems, Inc.', '01-Aug-1985', 2.50, 'Apple Computer, Inc.', 'Technology', 'Early Stage', 'Alert Public', 'California')
        ]
        
        c.executemany("INSERT OR REPLACE INTO m82_deals VALUES (?,?,?,?,?,?,?,?,?)", deals)
        conn.commit()
        conn.close()
        print("✅ Ingesta M82: Historial de Deals registrado correctamente.")
    except Exception as e:
        print(f"Error en ingesta de deals M82: {e}")

if __name__ == "__main__":
    registrar_deals_aapl()
