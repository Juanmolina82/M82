import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.home() / ".m82_secrets" / "m82.env"
load_dotenv(dotenv_path=env_path, override=True)

WC_API_KEY = os.getenv("WORLDCHECK_API_KEY")
WC_API_SECRET = os.getenv("WORLDCHECK_API_SECRET")
WC_URL = os.getenv("WORLDCHECK_URL", "https://api-worldcheck.refinitiv.com/v2/cases/screeningRequest")

def run_screening(name_to_screen):
    if not WC_API_KEY:
        print("[WORLDCHECK ERROR] Falta WORLDCHECK_API_KEY en .m82_secrets")
        return None

    payload = {
        "groupId": os.getenv("WORLDCHECK_GROUP_ID", "default"),
        "entityType": "INDIVIDUAL",
        "name": name_to_screen
    }
    
    headers = {
        "Authorization": f"Bearer {WC_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(WC_URL, json=payload, headers=headers, timeout=10)
        if res.status_code in [200, 201]:
            print(f"[WORLDCHECK SUCCESS] Screening ejecutado para: {name_to_screen}")
            return res.json()
        print(f"[WORLDCHECK ERROR] Status: {res.status_code} | Msg: {res.text}")
    except Exception as e:
        print(f"[WORLDCHECK EXCEPTION] {e}")
    return None

if __name__ == "__main__":
    print("[INIT] Módulo de Compliance / World-Check Activo en M82.")
    # Mantener proceso vivo para PM2
    import time
    while True:
        time.sleep(3600)
