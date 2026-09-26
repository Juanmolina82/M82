#!/usr/bin/env python3
import sqlite3, os, hashlib, json, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def register_fused_signal():
    payload = {
        "signal_id": "CORR_VE_ORMUZ_2026_09",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "primary_vectors": {
            "ORMUZ_VECTOR": {
                "diplomatic_offer": "Araghchi 7-day plan (UNGA NY)",
                "effective_flow": "6.98M bpd (-38% vs pre-war)",
                "narrative_buffer": "40M bbl escorted volume news-flash",
                "market_reaction": "Brent pullback to $98.37"
            },
            "VENEZUELA_VECTOR": {
                "entity": "NABEP / Pentagon OSC",
                "function": "Non-traditional supply injection bypass"
            }
        },
        "l3_correlation_logic": "Double supply shock mitigation attempt. High volatility risk: if diplomatical MoU fails (similar to June collapse), immediate bullish repricing expected in middle distillates (Diesel).",
        "l4_verification_status": "PASSED_THRESHOLD_85"
    }

    raw_data = json.dumps(payload, sort_keys=True)
    evidence_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla m82_fused_signals si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_fused_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_code TEXT,
            unified_summary TEXT,
            data_hash TEXT,
            status TEXT DEFAULT 'PROCESSED',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    summary = "CORRELACIÓN L3: Oferta diplomática Ormuz (Araghchi/UNGA) + SPV NABEP VE. Riesgo de volatilidad asimétrica en diésel."

    cursor.execute(
        "INSERT INTO m82_fused_signals (signal_code, unified_summary, data_hash) VALUES (?, ?, ?)",
        (payload["signal_id"], summary, evidence_hash)
    )
    
    # Registrar auditoría L5
    cursor.execute(
        "INSERT INTO m82_forensic_audit (event_type, data_hash) VALUES (?, ?)",
        (f"FUSED_SIGNAL: {payload['signal_id']}", evidence_hash)
    )

    conn.commit()
    conn.close()

    print(f"✅ Señal fusionada ORMUZ-VE asentada en m82_fused_signals.")
    print(f"🔐 SHA-256 Hash: {evidence_hash}")

if __name__ == "__main__":
    register_fused_signal()
