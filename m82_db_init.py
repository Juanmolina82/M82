import sqlite3

def inicializar_m82_db():
    conn = sqlite3.connect("m82_database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS snapshot (
        fecha TEXT, 
        wti_ref REAL, 
        brent_rt REAL, 
        ovx REAL, 
        nav_ifrs REAL, 
        nav_spot REAL, 
        ltv_spot REAL
    )''')
    
    # Insertar datos base de prueba para M82
    c.execute("INSERT INTO snapshot VALUES (datetime('now'), 92.43, 97.5, 32.5, 775.60, 810.46, 18.51)")
    conn.commit()
    conn.close()
    print("✅ Base de datos m82_database.db inicializada correctamente.")

if __name__ == "__main__":
    inicializar_m82_db()
