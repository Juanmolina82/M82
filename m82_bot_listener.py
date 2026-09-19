import os
import time
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

env_path = Path.home() / ".m82_secrets" / "m82.env"
load_dotenv(dotenv_path=env_path, override=True)

TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TG_TOKEN}"
STATE_FILE = Path.home() / "M82" / "last_state.json"

CATEGORIES = {
    "📈 EQUITY INDICES": [".SPX", ".DJI", ".NDX", ".VIX", ".FTSE", ".GDAXI", ".N225", ".BVSP"],
    "🏛 10Y YIELDS": ["US10YT=RR", "DE10YT=RR", "JP10YT=RR", "GB10YT=RR"],
    "💱 FX SPOTS": ["EUR=", "GBP=", "JPY=", "CHF=", "BRL=", "RUB="],
    "🛢 COMMODITIES": ["LCOc1", "CLc1", "NGc1", "XAU=", "XAG=", "HGc1"]
}

def send_message(chat_id, text, parse_mode="Markdown"):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[ERROR SEND] {e}")

def fetch_macro_matrix(filter_cat=None):
    try:
        if not STATE_FILE.exists():
            return "⚠️ *Esperando datos del ciclo de ingesta LSEG...*"

        with open(STATE_FILE, "r") as f:
            state = json.load(f)

        basket_data = state.get("basket", {})
        msg = "⚡ *M82 GLOBAL MACRO MONITOR* ⚡\n"
        msg += "`Fuente: LSEG Workspace / RDP REST Direct Feed`\n\n"

        for cat_name, tickers in CATEGORIES.items():
            if filter_cat and filter_cat not in cat_name:
                continue
                
            msg += f"*{cat_name}*\n```text\n"
            cat_rows = []
            for t in tickers:
                if t in basket_data:
                    info = basket_data[t]
                    cat_rows.append({
                        "ASSET": t.replace("=RR", "").replace("=", ""),
                        "LAST": f"{float(info.get('last', 0.0)):.2f}",
                        "PCT": f"{float(info.get('pct', 0.0)):+.2f}%"
                    })
            if cat_rows:
                df_cat = pd.DataFrame(cat_rows)
                msg += df_cat.to_string(index=False) + "\n"
            msg += "```\n"

        return msg
    except Exception as e:
        return f"❌ Error generando matriz macro: {e}"

def handle_updates():
    offset = 0
    print("[BOT LISTENER] Escuchando Telegram (M82 Macro Integrated)...")
    while True:
        try:
            url = f"{API_URL}/getUpdates?offset={offset}&timeout=5"
            res = requests.get(url, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                for result in data.get("result", []):
                    offset = result["update_id"] + 1
                    message = result.get("message", {})
                    text = message.get("text", "").strip().lower()
                    chat_id = message.get("chat", {}).get("id")

                    if not chat_id or not text:
                        continue

                    if text in ["/reporte", "/macro", "reporte"]:
                        send_message(chat_id, fetch_macro_matrix())
                    elif text in ["/fx", "fx"]:
                        send_message(chat_id, fetch_macro_matrix(filter_cat="FX"))
                    elif text in ["/yields", "yields", "/bonos"]:
                        send_message(chat_id, fetch_macro_matrix(filter_cat="YIELDS"))
                    elif text in ["/status", "status"]:
                        send_message(chat_id, "🟢 *NODO M82 EN LÍNEA* | Ingesta LSEG Workspace + Macro Grid Activa")
        except Exception:
            time.sleep(3)

if __name__ == "__main__":
    handle_updates()
