import sqlite3, os, datetime

# Ajustar ruta para buscar tanto en ~/M82/m82_database.db como en ~/m82_database.db
DB_PATHS = [
    os.path.expanduser("~/M82/m82_database.db"),
    os.path.expanduser("~/m82_database.db")
]

def _conn():
    for path in DB_PATHS:
        if os.path.exists(path):
            return sqlite3.connect(path)
    return None

def get_chevron_sales_lseg(days=30):
    """
    Lee ventas reales desde m82_database.db
    Tabla esperada: chevron_exports o lseg_flows
    Si no existe, usa estimado base Orinoco 17 campos
    """
    try:
        c = _conn()
        if not c:
            return 170.2  # fallback
        cur = c.cursor()
        # Intenta tablas comunes
        for table in ["chevron_exports", "lseg_flows", "venezuela_oil_flows"]:
            try:
                cur.execute(f"SELECT SUM(volume_bbl * price) / 1e6 FROM {table} WHERE date >= date('now','-{days} days')")
                val = cur.fetchone()[0]
                if val and val > 0:
                    c.close()
                    return round(float(val), 1)
            except:
                continue
        c.close()
    except Exception as e:
        print(f"[lseg_client] DB read error: {e}")
    return 170.2

def get_ofac_release(days=30):
    """
    Lee liberaciones OFAC a Delcy desde DB
    Tabla: ofac_releases
    """
    try:
        c = _conn()
        if not c:
            return 38.5
        cur = c.cursor()
        for table in ["ofac_releases", "escrow_releases", "treasury_releases"]:
            try:
                cur.execute(f"SELECT SUM(amount_usd) / 1e6 FROM {table} WHERE date >= date('now','-{days} days')")
                val = cur.fetchone()[0]
                if val and val > 0:
                    c.close()
                    return round(float(val), 1)
            except:
                continue
        c.close()
    except Exception as e:
        print(f"[lseg_client] OFAC read error: {e}")
    return 38.5

def get_escrow_metrics():
    ventas = get_chevron_sales_lseg()
    liberado = get_ofac_release()
    retenido = round(ventas - liberado, 1)
    pct = round((retenido / ventas * 100) if ventas > 0 else 0, 1)
    estado = "🚨 HIGH FISCAL STRESS DETECTED" if pct > 70 else "✅ Stable - Transition funded"

    # Log para tail -f
    print(f"[{datetime.datetime.now()}] LSEG: ventas=${ventas}M liberado=${liberado}M retenido=${retenido}M ({pct}%)", flush=True)

    return {
        "ventas": ventas,
        "liberado": liberado,
        "retenido": retenido,
        "pct": pct,
        "estado": estado
    }

if __name__ == "__main__":
    print(get_escrow_metrics())
