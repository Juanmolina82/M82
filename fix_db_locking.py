#!/usr/bin/env python3
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def repair_database():
    print("🔧 [M82 REPAIR] Aplicando modo WAL y creando tablas faltantes...")
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    cursor = conn.cursor()

    # 1. Habilitar WAL Mode para escrituras y lecturas concurrentes sin bloqueo
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=30000;")

    # 2. Crear tabla principal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING'
        )
    """)

    # 3. Crear tabla de señales fusionadas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_fused_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            correlation_id TEXT,
            topic TEXT,
            unified_headline TEXT,
            composite_score REAL,
            evidence_chain TEXT,
            status TEXT DEFAULT 'FUSED'
        )
    """)

    # 4. Crear tabla de auditoría forense (soluciona el error 'no such table')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_forensic_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            data_hash TEXT,
            payload TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ [OK] Modo WAL activado y tabla 'm82_forensic_audit' creada correctamente.")

if __name__ == "__main__":
    repair_database()
