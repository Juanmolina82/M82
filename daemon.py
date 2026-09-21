import time, json, hashlib, os, datetime, requests
from pathlib import Path

BASE = Path.home() / "M82"
METRICS = BASE / "metrics.json"
AUDIT = BASE / "logs/audit.log"
PIDFILE = BASE / "pid.txt"
VAULT = BASE / "vault.json"

metrics = {
  "AMZN": {"price": 255.14, "dma50": 251.96, "signal": "TESTING_50DMA"},
  "AAPL": {"price": 255.80, "pe_fy27": 30.5, "weight_spx": 7.9},
  "UST": {"10Y": 4.75, "30Y": 5.2423, "spread": 0.4923},
  "SPX": {"level": 7610, "support": 7610},
  "VEN": {"bid": 51.75, "mid": 52.25, "ev": 13.0},
  "WTI": {"price": 87.0}
}

def send_telegram(text):
    if not VAULT.exists(): return
    try:
        with open(VAULT, 'r') as f: v = json.load(f)
        token = v.get('TELEGRAM_BOT_TOKEN')
        chat_id = v.get('TELEGRAM_CHAT_ID')
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}, timeout=5)
    except Exception: pass

def log(msg):
    ts = datetime.datetime.utcnow().isoformat()
    line = f"{ts} | {msg}"
    print(line)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT, "a") as f:
        f.write(line + "\n")
    sha = hashlib.sha256(line.encode()).hexdigest()[:12]
    with open(AUDIT, "a") as f:
        f.write(f"SIG:{sha}\n")

def alert_push(title, content, tts=""):
    os.system(f'termux-notification --title "{title}" --content "{content}" --priority high')
    if tts:
        os.system(f'termux-tts-speak "{tts}"')
    tg_msg = f"🚨 *{title}*\n\n{content}"
    send_telegram(tg_msg)
    log(f"ALERT {title}: {content}")

def check_conditions():
    if metrics["AAPL"]["price"] >= 260 and metrics["UST"]["30Y"] >= 5.30:
        alert_push("M82 TOP SIGNAL", "AAPL 260+ vs US30Y 5.30% - Venta megacap", "Distribution top Apple versus long bond")

    if metrics["AMZN"]["price"] < metrics["AMZN"]["dma50"]:
        alert_push("M82 DEFENSIVE ROTATION", f"AMZN {metrics['AMZN']['price']} < 50DMA {metrics['AMZN']['dma50']}", "AMZN breakdown fifty DMA")

    with open(METRICS, "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    log(f"DAEMON START PID {os.getpid()} CORE-V6")
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()))

    while True:
        try:
            check_conditions()
            time.sleep(300)
        except Exception as e:
            log(f"ERROR {e}")
            time.sleep(60)
