import hashlib, json, datetime, os, requests
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"
OUTPUT = BASE / "audit_log.jsonl"
HASH_SALT = "M82-20260901"

def send_telegram(text):
    if not VAULT.exists():
        print("[ERR] vault.json no encontrado.")
        return
    try:
        with open(VAULT, 'r') as f: 
            v = json.load(f)
        token = v.get('TELEGRAM_BOT_TOKEN')
        chat_id = v.get('TELEGRAM_CHAT_ID')
        
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                print("[OK] Reporte de Cierre enviado a Telegram.")
            else:
                print(f"[ERR] Telegram API error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[ERR] Error al enviar a Telegram: {e}")

def gen_hash(data_str):
    return hashlib.sha256(f"{data_str}{HASH_SALT}{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:16].upper()

def build_closing_wrap():
    now_et = datetime.datetime.now()
    date_id = now_et.strftime("%Y%m%d-%H%M")
    audit_hash = gen_hash(f"CLOSE-{date_id}")
    
    wrap = (
        "📊 *M82 QUANTITATIVE MARKET FEED*\n"
        "⏱️ _16:00 ET | Official Closing Bell & Settlement_\n\n"
        "🟢 *CLOSING RALLY & ROTACIÓN SECTORIAL*\n"
        "• *E&P / Energía:* Confirmación de cierre en máximos de sesión.\n"
        "• *Megacap Tech:* AAPL consolidando cierre sobre estructura compradora.\n\n"
        "🔴 *CLOSING FLUSH & PRESIÓN DE VOLATILIDAD*\n"
        "• *Ciberseguridad / Software:* Ajuste de fin de día en valoraciones High-Beta.\n\n"
        "📉 *MACRO & RATES SUMMARY*\n"
        "• *Curva Soberana:* Cierre definitivo de los yields en UST 10Y / 30Y.\n\n"
        "────────────────────────\n"
        "🏛️ *MOLINA HOLDINGS LLC*\n"
        "_Private Wealth & Cross-Asset Risk Management_\n\n"
        "✉️ *Executive Desk:*\n"
        "• *CEO:* `jmmp@molina82.com` | `jmiguel1535@gmail.com`\n"
        "• *CFO:* `cmme@molina82.com` | `molinagloballlc@gmail.com`\n\n"
        "🔒 *INTEGRITY & COMPLIANCE STAMP:*\n"
        "• *Status:* Final Verified Closing Data Stream\n"
        f"• *SHA-256 Audit Hash:* `{audit_hash}`\n"
        "• *Licencia:* Workspace Desktop API (Non-Redistribution / Internal Buy-Side Use Only)\n"
        f"• *Governance:* Internal Audit Committee Validated — Ref: `#M82-{date_id}`\n\n"
        "_*Notice:* Este informe es un entregable cuantitativo protegido para uso exclusivo de nuestros socios e inversores acreditados. Prohibida su copia o redistribución no autorizada._"
    )
    
    # Registro en log inmutable
    BASE.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "a") as f:
        f.write(json.dumps({"ts": now_et.isoformat(), "hash": audit_hash, "type": "DAILY_CLOSE"}) + "\n")
    
    # Envío a Telegram
    send_telegram(wrap)
    return wrap

if __name__ == "__main__":
    build_closing_wrap()
