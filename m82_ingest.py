import os
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.home() / ".m82_secrets" / "m82.env"
load_dotenv(dotenv_path=env_path, override=True)

APP_KEY = os.getenv("LSEG_APP_KEY")
USERNAME = os.getenv("LSEG_USERNAME")
PASSWORD = os.getenv("LSEG_PASSWORD")
STATE_FILE = Path.home() / "M82" / "last_state.json"

TICKERS = ["XLE", "OIH", "RIG", "VAL", "BORR.OL", "XOM", "CVX", "GEV.N", "XAU="]

def get_rdp_token():
    url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "grant_type": "password",
        "takeExclusiveSignOnControl": "true",
        "client_id": APP_KEY
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        res = requests.post(url, data=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json().get("access_token")
    except Exception as e:
        print(f"[AUTH EXCEPTION] {e}")
    return None

def fetch_lseg_quotes(token):
    tickers_str = ",".join(TICKERS)
    url = f"https://api.refinitiv.com/data/environmental-financial-demographics/v1/quotes?universe={tickers_str}&fields=CF_LAST,PCTCHNG"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"[FETCH ERROR] {e}")
    return None

def run_pipeline():
    print("[INIT] Ingestor LSEG RDP con Commodity Gate...")
    token = get_rdp_token()
    token_time = time.time()

    while True:
        try:
            if not token or (time.time() - token_time > 1200):
                token = get_rdp_token()
                token_time = time.time()

            if token:
                raw_data = fetch_lseg_quotes(token)
                if raw_data and "data" in raw_data:
                    basket = {}
                    pcts = []
                    for row in raw_data["data"]:
                        symbol = row[0].split(".")[0].replace("=", "")
                        last_p = float(row[1]) if row[1] is not None else 0.0
                        pct = float(row[2]) if row[2] is not None else 0.0

                        basket[symbol] = {
                            "last": round(last_p, 2),
                            "pct": round(pct, 2)
                        }
                        if symbol != "XAU":
                            pcts.append(pct)

                    avg_pct = sum(pcts) / len(pcts) if pcts else 0.0

                    state_data = {
                        "last_timestamp": time.time(),
                        "last_avg_pct": round(avg_pct, 2),
                        "basket": basket
                    }

                    with open(STATE_FILE, "w") as f:
                        json.dump(state_data, f, indent=2)

                    print(f"[INGEST SUCCESS] Gold & Basket sincronizados.")
        except Exception as e:
            print(f"[PIPELINE ERROR] {e}")

        time.sleep(60)

if __name__ == "__main__":
    run_pipeline()
