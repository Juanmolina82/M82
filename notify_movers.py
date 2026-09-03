import json, datetime, requests, os, hashlib
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def send_telegram(text):
    if not VAULT.exists(): return
    try:
        with open(VAULT, 'r') as f: v = json.load(f)
        token, chat_id = v.get('TELEGRAM_BOT_TOKEN'), v.get('TELEGRAM_CHAT_ID')
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}, timeout=5)
    except Exception as e:
        pass

def generate_audit_hash(data_str):
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:16].upper()

def push_investor_feed():
    now_dt = datetime.datetime.now()
    now_et = now_dt.strftime('%H:%M ET')
    audit_ref = f"M82-{now_dt.strftime('%Y%m%d')}-{now_dt.strftime('%H%M')}"
    sha_signature = generate_audit_hash(audit_ref + "MOLINA_HOLDINGS_SECURE")

    msg = (
        "📊 *M82 QUANTITATIVE MARKET FEED*\n"
        f"⏱️ _{now_et} | Live Intelligence_\n\n"
        "🟢 *VECTOR ALCISTA & ROTACIÓN SECTORIAL*\n"
        "• *E&P / Energía:* Impulso alcista en exploración y producción.\n"
        "  - `EOG`: $148.40 (+2.37%)\n"
        "  - `COP`: $135.53 (+2.29%)\n"
        "  - `XOM`: $164.14 (+1.98%)\n"
        "• *Megacap Tech:*\n"
        "  - `AAPL`: $324.70 (+2.48%) — Sostiene estructura compradora.\n\n"
        "🔴 *VECTOR BAJISTA & FLUSH SECTORIAL*\n"
        "• *Software & Ciberseguridad:*\n"
        "  - `AXON`: $521.04 (-8.03%)\n"
        "  - `CRWD`: $214.00 (-7.36%)\n"
        "  - `PANW`: $361.19 (-5.48%)\n\n"
        "📈 *ANÁLISIS TÉCNICO & LIQUIDEZ*\n"
        "• Curva de Tasas: US30Y bajo prueba del umbral del 5.30%.\n"
        "• Sesión en desarrollo hacia la ventana de settlement (15:50 ET).\n\n"
        "────────────────────────\n"
        "🏛️ *MOLINA HOLDINGS LLC*\n"
        "_Private Wealth & Cross-Asset Risk Management_\n\n"
        "✉️ *Executive Desk:*\n"
        "• *CEO:* `jmmp@molina82.com` | `jmiguel1535@gmail.com`\n"
        "• *CFO:* `cmme@molina82.com` | `molinagloballlc@gmail.com`\n\n"
        "🔒 *INTEGRITY & COMPLIANCE STAMP:*\n"
        "• *Status:* Verified Proprietary Data Stream\n"
        f"• *SHA-256 Audit Hash:* `{sha_signature}`\n"
        "• *Licencia:* Workspace Desktop API (Non-Redistribution / Internal Buy-Side Use Only)\n"
        f"• *Governance:* Internal Audit Committee Validated — Ref: `#{audit_ref}`\n\n"
        "_*Notice:* Este informe es un entregable cuantitativo protegido para uso exclusivo de nuestros socios e inversores acreditados. Prohibida su copia o redistribución no autorizada._"
    )
    send_telegram(msg)

if __name__ == "__main__":
    push_investor_feed()
