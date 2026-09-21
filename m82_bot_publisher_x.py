import time, os, sqlite3, requests, re
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/M82/.env"))
TG_TOKEN = os.getenv("M82_TELEGRAM_TOKEN")
TG_CHAT = os.getenv("M82_TELEGRAM_CHAT")
X_SECRET = os.getenv("X_CLIENT_SECRET")
X_ID = os.getenv("X_CLIENT_ID")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

PAUSA_RITMO = 30.0

def clean_text(text):
    if not text: return ""
    return re.sub(r'<[^>]*>', '', str(text)).strip()

def format_telegram_msg(headline, desk):
    desk_clean = desk.replace("_", " ").upper()
    return (
        f"🚨 <b>M82 BREAKING STREAM</b> [{desk_clean}]\n\n"
        f"🔴 {clean_text(headline)}\n\n"
        f"🏛 <b>Molina Holdings LLC & Molina Global LLC</b>\n"
        f"⚖️ <i>Proprietary Financial Stream • All Rights Reserved © 2026</i>\n\n"
        f"#M82 @MolinaHoldings"
    )

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json().get("ok", False)
    except Exception as e:
        print(f"❌ Error Telegram: {e}", flush=True)
        return False

def post_to_x(headline):
    # Formateo compacto para X (Límite 280 caracteres)
    x_text = f"🚨 #M82 BREAKING: {clean_text(headline)[:180]}\n\n🏛 Molina Holdings LLC\n#M82 $FIN"
    
    # Intento de envío a API v2 de X
    url = "https://api.x.com/2/tweets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {X_SECRET}"  # Intento con Secret / Bearer
    }
    payload = {"text": x_text}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 201:
            print("🐤 [X / TWITTER OK] Post publicado con éxito.", flush=True)
            return True
        elif r.status_code in [402, 403]:
            print("⚠️ [X / TWITTER] Requiere saldo/créditos en console.x.com. Omitiendo envío a X...", flush=True)
            return False
        else:
            print(f"⚠️ [X API Status {r.status_code}]: {r.text[:100]}", flush=True)
            return False
    except Exception as e:
        print(f"⚠️ Exception X API: {e}", flush=True)
        return False

def main_loop():
    print("🚀 [M82 DUAL PUBLISHER] Servidor iniciado (Telegram Active | X Hybrid Standby)...", flush=True)
    while True:
        try:
            if not os.path.exists(DB_PATH):
                time.sleep(5)
                continue

            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT rowid, daemon_source, headline 
                FROM m82_multi_stream 
                WHERE status = 'PENDING' OR status IS NULL 
                ORDER BY rowid ASC LIMIT 1
            """)
            row = cursor.fetchone()
            
            if row:
                row_id, source, headline = row
                if not headline:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SKIPPED' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    conn.close()
                    continue

                tg_msg = format_telegram_msg(headline, source or "GLOBAL_STREAM")
                
                # 1. Despacho obligatorio a Telegram
                tg_ok = send_telegram(tg_msg)
                
                # 2. Despacho a X (Si falla por créditos, no interrumpe el flujo)
                post_to_x(headline)

                if tg_ok:
                    cursor.execute("UPDATE m82_multi_stream SET status = 'SENT' WHERE rowid = ?", (row_id,))
                    conn.commit()
                    print(f"⚡ [DESPACHO EXITOSO ID {row_id}] {headline[:40]}...", flush=True)
                else:
                    print(f"❌ Reintentando ID {row_id} en próximo ciclo...", flush=True)
                    
                conn.close()
                time.sleep(PAUSA_RITMO)
            else:
                conn.close()
                time.sleep(10)

        except Exception as e:
            print(f"⚠️ Loop Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
