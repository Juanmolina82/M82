import sqlite3, os, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.expanduser("~/m82_database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

test_headlines = [
    "Chevron nears Venezuela deal as US prepares 17-field oil lease",
    "Delcy Rodriguez requests escrow release for payroll",
    "PDVSA Orinoco oil exports surge following new OFAC guidelines"
]

for title in test_headlines:
    h = hashlib.md5(title.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO m82_multi_stream (news_hash, daemon_source, headline, status)
            VALUES (?, 'REUTERS_BREAKING_ONLY', ?, 'PENDING')
        """, (h, title))
        print(f"📥 Evento inyectado a DB: {title}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Ya existía en DB: {title}")

conn.commit()
conn.close()
