import sqlite3

def registrar_exits_aapl():
    try:
        conn = sqlite3.connect("m82_database.db")
        c = conn.cursor()
        
        # Tabla para salidas de Capital Privado / VC Exits
        c.execute('''CREATE TABLE IF NOT EXISTS m82_pe_vc_exits (
            deal_id TEXT PRIMARY KEY,
            investee_company TEXT,
            exit_date TEXT,
            return_m REAL,
            fund_name TEXT,
            trbc_industry TEXT,
            nation TEXT,
            fund_status TEXT,
            state_region TEXT
        )''')
        
        # Registros de salidas de portafolio Refinitiv (AAPL.O)
        exits = [
            ('19830', 'Anobit Technologies Ltd', '20-Dec-2011', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Active', 'Non-US'),
            ('19202', 'ORBO, Inc.', '20-Jan-2007', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('22536', 'Akamai Technologies, Inc.', '28-Oct-1999', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Massachusetts'),
            ('21838', 'Swiss Media Group Inc.', '27-May-1999', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Defunct', 'California'),
            ('22034', 'Echidna Systems Corp.', '27-Jul-1998', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('21635', 'FUJIFILM Directs, Inc.', '01-May-1998', 22.50, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('21157', 'CRK Technology, Inc.', '14-Sep-1997', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Massachusetts'),
            ('19977', 'Pillar Corporation', '07-Dec-1996', 22.01, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('18134', 'BIOCAD Corporation', '22-Aug-1994', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('21400', 'Small Cap Syndicate, Inc.', '24-Feb-1992', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Texas'),
            ('20108', 'Courier Technology', '24-Nov-1991', 30.00, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'Massachusetts'),
            ('18780', 'NetPower Systems, Inc.', '15-Jul-1991', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('4901', 'Sabroe, Inc.', '04-Jan-1991', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California'),
            ('20254', 'Adobe Systems, Inc.', '10-Apr-1989', None, 'Apple Computer / Strategic...', 'Technology', 'United States', 'Currently Making Investm...', 'California')
        ]
        
        c.executemany("INSERT OR REPLACE INTO m82_pe_vc_exits VALUES (?,?,?,?,?,?,?,?,?)", exits)
        conn.commit()
        conn.close()
        print("✅ Ingesta M82: Módulo de PE/VC Exits actualizado correctamente.")
    except Exception as e:
        print(f"Error en ingesta M82 Exits: {e}")

if __name__ == "__main__":
    registrar_exits_aapl()
