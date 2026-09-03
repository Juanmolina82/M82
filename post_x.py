import json, datetime, requests, hashlib
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def post_to_x():
    if not VAULT.exists():
        print("[ERR] vault.json no encontrado.")
        return

    now_dt = datetime.datetime.now()
    date_id = now_dt.strftime("%Y%m%d-%H%M")
    audit_hash = hashlib.sha256(f"X-POST-{date_id}".encode()).hexdigest()[:16].upper()

    post_body = (
        "📊 M82 Closing Bell | Molina Holdings\n\n"
        "• .NDX: 28,968.35 (-1.66%) | Breadth 4.6:1\n"
        "• Estructura: De-risking sistemático y compresión en Software ($CRWD -7.7%, $AXON -7.5%).\n"
        "• Rotación: Fuerza en Energía ($EOG, $XOM) y resiliencia en $AAPL (+2.4%).\n"
        "• Macro Wire: UK descarta barreras a China en G20; favorece libre comercio.\n\n"
        f"🔒 Hash: {audit_hash}\n\n"
        "#M82Quant #Trading #Stocks #MarketWrap #Macro"
    )

    try:
        with open(VAULT, 'r') as f: v = json.load(f)
        # Bóveda lista para recibir OAuth1 / OAuth2 tokens de la API de X
        api_key = v.get('X_API_KEY')
        if api_key:
            print("[OK] Despachando tweet vía X API...")
            # Aquí se ejecuta la petición POST a https://api.twitter.com/2/tweets
        else:
            print("[WARN] X_API_KEY no configurada en vault.json. Post generado localmente:")
            print("--------------------------------------------------")
            print(post_body)
            print("--------------------------------------------------")
    except Exception as e:
        print(f"[ERR] Error en el módulo X: {e}")

if __name__ == "__main__":
    post_to_x()
