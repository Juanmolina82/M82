import json, time, hashlib, os, datetime, requests
from pathlib import Path

BASE = Path.home() / "M82"
AUDIT = BASE / "logs/audit.log"
VAULT = BASE / "vault.json"

def send_telegram_alert(asset_type, ticker, headline, impact_score, action_summary):
    if not VAULT.exists(): return
    with open(VAULT, 'r') as f: v = json.load(f)
    token = v.get('TELEGRAM_BOT_TOKEN')
    chat_id = v.get('TELEGRAM_CHAT_ID')
    
    # Formato visual adaptable según activo
    icons = {
        "EQUITY": "📈", "BOND": "📜", "COMMODITY": "🛢️", 
        "ETF": "📊", "CONTRACT": "📑", "FX": "💱"
    }
    icon = icons.get(asset_type.upper(), "⚡")
    
    msg = f"{icon} *M82 REAL-TIME FEED | {asset_type.upper()}*\n" \
          f"• *Ticker/Asset:* `{ticker}`\n" \
          f"• *Impacto:* `{impact_score}/10`\n" \
          f"• *Headline:* {headline}\n" \
          f"• *Acción:* _{action_summary}_\n\n" \
          f"⏱️ _{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}_"
          
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': msg, 'parse_mode': 'Markdown'}, timeout=5)

def log_event(ticker, headline):
    ts = datetime.datetime.utcnow().isoformat()
    raw = f"{ts} | {ticker} | {headline}"
    sha = hashlib.sha256(raw.encode()).hexdigest()[:12]
    
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT, "a") as f:
        f.write(f"{raw} | SIG:{sha}\n")

def process_incoming_news(payload):
    """
    Recibe payloads estructurados desde cualquier feed (LSEG, Webhooks, Python APIs)
    """
    asset_type = payload.get("asset_type", "EQUITY")
    ticker = payload.get("ticker", "GENERIC")
    headline = payload.get("headline", "Sin información")
    impact_score = payload.get("impact", 5)
    action = payload.get("action", "MONITOR")

    # 1. Auditoría SHA-256
    log_event(ticker, headline)
    
    # 2. Despacho directo a Telegram si supera el umbral de impacto
    if impact_score >= 6:
        send_telegram_alert(asset_type, ticker, headline, impact_score, action)

if __name__ == "__main__":
    # Ejemplo de prueba de ingesta multiactivo
    test_payload = {
        "asset_type": "BOND",
        "ticker": "VEN 2027",
        "headline": "Oferta de compra en firme sobre colateral refinación",
        "impact": 9,
        "action": "REBALANCE_LONG_CARRY"
    }
    process_incoming_news(test_payload)
    print("[OK] Evento multiactivo procesado y despachado.")
