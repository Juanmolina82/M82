import json, os
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def fetch_lseg_data():
    if not VAULT.exists():
        print("[ERR] vault.json no encontrado.")
        return None
        
    with open(VAULT, 'r') as f:
        vault = json.load(f)
        
    app_key = vault.get("LSEG_APP_KEY")
    user = vault.get("LSEG_USERNAME")
    password = vault.get("LSEG_PASSWORD")
    
    if not app_key or "TU_APP_KEY" in app_key:
        print("[WARN] LSEG_APP_KEY no configurada. Utilizando metrics.json en fallback.")
        return None

    # Inicialización del SDK refinitiv-data / lseg-data
    try:
        import refinitiv.data as rd
        rd.open_platform_session(
            app_key=app_key,
            grant=rd.session.platform.GrantPassword(username=user, password=password)
        )
        print("[OK] Sesión LSEG Workspace autenticada correctamente.")
        
        # Ejemplo de extracción para el .NDX
        df = rd.get_data(['.NDX'], ['CF_LAST', 'PCTCHNG'])
        rd.close_session()
        return df
    except Exception as e:
        print(f"[ERR] Fallo en conexión LSEG: {e}")
        return None

if __name__ == "__main__":
    fetch_lseg_data()
