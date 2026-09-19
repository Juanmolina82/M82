import sqlite3

def cargar_todas_las_inversiones():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    
    # Crear estructura de tabla para el registro de Private Equity / Venture Capital
    c.execute('''CREATE TABLE IF NOT EXISTS m82_pe_vc_investments (
        deal_id TEXT PRIMARY KEY,
        investee_company TEXT,
        invest_date TEXT,
        amount_usd_m REAL,
        fund_name TEXT,
        trbc_industry TEXT,
        stage TEXT,
        status TEXT,
        nation TEXT,
        region TEXT
    )''')
    
    # Registros completos de la pantalla Refinitiv
    investments = [
        ('340091804001', 'Anobit Technologies', '19-Nov-2010', 10.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Acquisition', 'United States', 'Israel'),
        ('340090801001', 'ORBO, Inc.', '20-Jan-2007', 41.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Active', 'United States', 'California'),
        ('340090617001', 'Flashpoint Technology', '27-Oct-1999', 27.00, 'Apple Computer, Inc.', 'Basic Materials', 'Expansion', 'Active', 'United States', 'New Hampshire'),
        ('340090331002', 'Akamai Technologies', '14-May-1999', 10.12, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Alert Public', 'United States', 'Massachusetts'),
        ('340090175001', 'Swiss Media Group Inc.', '21-Dec-1998', 3.00, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Active', 'United States', 'California'),
        ('340090008001', 'Pillar Corporation', '21-Oct-1997', 2.00, 'Apple Computer, Inc.', 'Technology', 'Later Stage', 'Acquisition', 'United States', 'California'),
        ('340089839002', 'BIOCAD Corporation', '22-Aug-1997', 1.50, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Merger', 'United States', 'California'),
        ('340089832002', 'ORBO Technology, Inc.', '21-Oct-1991', 1.50, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Acquisition', 'United States', 'Massachusetts'),
        ('340089828005', 'Courier Technology', '01-Mar-1989', 6.00, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Active', 'United States', 'California'),
        ('340089824008', 'FUJIFILM Directs, Inc.', '01-May-1988', 2.14, 'Apple Computer, Inc.', 'Technology', 'Expansion', 'Acquisition', 'United States', 'California'),
        ('340089819003', 'NetPower Systems, Inc.', '01-Feb-1987', 12.00, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Active', 'United States', 'California'),
        ('340089815003', 'DIGITAL FIX, Inc.', '21-Apr-1986', 3.50, 'Apple Computer, Inc.', 'Industrials', 'Expansion', 'Acquisition', 'United States', 'California'),
        ('340089808001', 'CRK Technology, Inc.', '01-Jan-1986', 0.30, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Acquisition', 'United States', 'Massachusetts'),
        ('340089803005', 'Sabroe, Inc.', '01-May-1985', 12.25, 'Apple Computer, Inc.', 'Technology', 'Later Stage', 'Merger', 'United States', 'California'),
        ('340089798008', 'Echidna Systems Co.', '01-Feb-1985', 24.50, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Alert Public', 'United States', 'California'),
        ('340089791002', 'Small Cap Syndicate', '24-Feb-1984', 4.55, 'Apple Computer, Inc.', 'Technology', 'Early Stage', 'Alert Public', 'United States', 'Texas'),
        ('340089785002', 'Minos Industries Corp.', '01-Jan-1984', 3.35, 'Apple Computer, Inc.', 'Technology', 'Early Stage', 'Defunct', 'United States', 'California'),
        ('340089779001', 'Porsche/Acht, Inc.', '01-Feb-1983', 0.72, 'Apple Computer, Inc.', 'Technology', 'Seed', 'Active', 'United States', 'California'),
        ('340089765001', 'Adobe Systems, Inc.', '01-Aug-1982', 2.50, 'Apple Computer, Inc.', 'Technology', 'Early Stage', 'Alert Public', 'United States', 'California')
    ]
    
    c.executemany("INSERT OR REPLACE INTO m82_pe_vc_investments VALUES (?,?,?,?,?,?,?,?,?,?)", investments)
    conn.commit()
    conn.close()
    print("✅ Ingesta M82 exitosa: Tabla 'm82_pe_vc_investments' poblada con todos los datos de Refinitiv.")

if __name__ == "__main__":
    cargar_todas_las_inversiones()
