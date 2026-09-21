import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_condensed_digest(limit=3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT headline FROM m82_multi_stream WHERE status='PENDING' ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ No hay noticias pendientes en la base de datos.")
        return

    text = "🚨 #M82 BREAKING SUMMARY\n\n"
    for i, row in enumerate(rows, 1):
        # Limpia el titular para no saturar caracteres
        clean_headline = row[0].strip()
        text += f"{i}️⃣ {clean_headline}\n"
    
    text += "\n🏛 @MolinaHoldings LLC"
    
    print("\n" + "="*40)
    print("📋 COPIA ESTE TEXTO COMPACTO PARA X:")
    print("="*40 + "\n")
    print(text)
    print("\n" + "="*40)

if __name__ == "__main__":
    get_condensed_digest()
