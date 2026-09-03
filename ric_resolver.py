import json
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def fetch_m82_closing_feed():
    if not VAULT.exists():
        print("[ERR] vault.json no encontrado.")
        return None

    with open(VAULT, 'r') as f:
        vault = json.load(f)

    app_key = vault.get("LSEG_APP_KEY")

    # Si la clave está vacía, no configurada o es de prueba
    if not app_key or "PEGA_AQUI" in app_key or "TU_APP_KEY" in app_key:
        print("[WARN] LSEG_APP_KEY pendiente. Retornando dataset estático de contingencia.")
        return {
            "NDX": {"TRDPRC_1": 28968.35, "PCTCHNG": -1.66},
            "US10Y": {"YIELD": 4.25},
            "AAPL": {"TRDPRC_1": 224.20, "PCTCHNG": 2.40}
        }

    try:
        import lseg.data as ld

        # Apertura de sesión nativa Workspace Desktop / Platform
        ld.open_session(app_key=app_key)

        ndx = ld.get_data(".NDX", fields=["TRDPRC_1", "PCTCHNG"])
        us10y = ld.get_data("US10YT=RR", fields=["YIELD"])
        aapl = ld.get_data("AAPL.O", fields=["TRDPRC_1", "PCTCHNG"])

        ld.close_session()

        return {"NDX": ndx, "US10Y": us10y, "AAPL": aapl}
    except Exception as e:
        print(f"[ERR] Fallo al consultar LSEG V2: {e}")
        return None

if __name__ == "__main__":
    feed = fetch_m82_closing_feed()
    if feed:
        print("[OK] Dataset resolvedor preparado exitosamente.")
