#!/usr/bin/env python3
import sqlite3, os, json, hashlib, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def execute_l3_fusion():
    payload = {
        "event_code": "M82_L3_GEOMACRO_FUSION_2026_09",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "market_snapshot": {
            "brent_ice": 104.10,
            "wti_nymex": 97.40,
            "dubai_dme": 110.12,
            "brent_wti_spread": 6.70,
            "structure": "EXTREME_BACKWARDATION"
        },
        "vectors": {
            "ormuz_strait": {"effective_flow_mbpd": 6.98, "deficit_pct": -38.0},
            "western_hemisphere": {"thesis": "John Kemp / Refinitiv", "driver": "US+VE Inflows"},
            "zulia_thermal_demand": {"national_electric_deficit_mw": 3226, "recovery_eta": "2027"}
        }
    }

    raw_str = json.dumps(payload, sort_keys=True)
    evidence_hash = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 60000;")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_fused_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_code TEXT,
            unified_summary TEXT,
            payload_json TEXT,
            data_hash TEXT,
            status TEXT DEFAULT 'PROCESSED',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    summary = "M82 L3 FUSIÓN: Brent $104.10 / WTI $97.40. Tensión Ormuz (-38% flujo) compensada por Hemisferio Occidental (John Kemp/NABEP) y presionada por consumo térmico Zulia."

    cursor.execute("""
        INSERT INTO m82_fused_signals (signal_code, unified_summary, payload_json, data_hash)
        VALUES (?, ?, ?, ?)
    """, (payload["event_code"], summary, raw_str, evidence_hash))

    conn.commit()
    conn.close()

    print(f"✅ Fusión L3 completada. Hash SHA-256: {evidence_hash}")

if __name__ == "__main__":
    execute_l3_fusion()
