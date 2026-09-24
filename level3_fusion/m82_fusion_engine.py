import sqlite3, os, json, time
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
OUTPUT_SIGNAL_PATH = os.path.expanduser("~/M82/m82_fused_signal.json")

class FusionEngine:
    def fetch_pending_signals(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, daemon_source, headline, timestamp FROM m82_multi_stream WHERE status = 'PENDING'")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def process_fusion(self):
        pending = self.fetch_pending_signals()
        if not pending:
            return None

        fusion_payload = {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "fused_signals_count": len(pending),
            "unified_summary": pending[0][2] if len(pending) == 1 else f"FUSIÓN CRÍTICA: Multi-vector ({len(pending)} eventos)."
        }

        with open(OUTPUT_SIGNAL_PATH, "w") as f:
            json.dump(fusion_payload, f, indent=4)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for row in pending:
            cursor.execute("UPDATE m82_multi_stream SET status = 'FUSED' WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()

        return fusion_payload
