#!/usr/bin/env python3
import os, sys, sqlite3, time
from datetime import date

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_transition_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date DATE UNIQUE,
            rigs_active INT,
            termozulia_mw INT,
            diesel_usgc_gal FLOAT,
            escrow_to_regime_pct FLOAT,
            racionamiento_zulia_h INT,
            score_mcm_entry FLOAT,
            status_flag TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def calculate_score(rigs, mw, diesel, escrow_pct, hours_off):
    # 1. Componente Diésel (Urgencia EE.UU.) - Normalizado 0 a 30 pts
    # $6.52 -> Max urgencia (30 pts). $4.00 -> Baja urgencia (10 pts)
    diesel_score = min(30.0, max(5.0, (diesel / 6.52) * 30.0))

    # 2. Componente Operativo (Rigs activos) - Normalizado 0 a 30 pts
    # Target: 6+ rigs sostenidos = 30 pts
    rigs_score = min(30.0, (rigs / 6.0) * 30.0)

    # 3. Componente Red Eléctrica (Termozulia + Racionamiento) - Normalizado 0 a 25 pts
    # Target: 800 MW + <2h racionamiento
    mw_factor = min(15.0, (mw / 800.0) * 15.0)
    stability_factor = min(10.0, max(0.0, (12.0 - hours_off) / 10.0 * 10.0))
    grid_score = mw_factor + stability_factor

    # 4. Componente Transparencia Escrow - Normalizado 0 a 15 pts
    # Menor % directo al régimen = mayor score de transición ordenada
    escrow_score = min(15.0, max(0.0, (100.0 - escrow_pct) / 100.0 * 15.0))

    total_score = round(diesel_score + rigs_score + grid_score + escrow_score, 2)
    return total_score

def update_index(rigs, mw, diesel, escrow_pct, hours_off):
    init_db()
    score = calculate_score(rigs, mw, diesel, escrow_pct, hours_off)
    today = str(date.today())
    
    flag = "DELCY_HOLD"
    if score >= 60.0:
        flag = "TRANSITION_WINDOW_OPEN"
    elif score >= 45.0:
        flag = "PRAGMATIC_CONVERGENCE"

    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO m82_transition_index 
        (record_date, rigs_active, termozulia_mw, diesel_usgc_gal, escrow_to_regime_pct, racionamiento_zulia_h, score_mcm_entry, status_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (today, rigs, mw, diesel, escrow_pct, hours_off, score, flag))
    
    # Inyectar alerta si se cruza el umbral crítico
    if score >= 60.0:
        headline = f"🚨 M82 SIGNAL: Transition Index crossed threshold ({score}/100). Status: {flag}. US Diesel: ${diesel}/gal | Rigs: {rigs} | Termozulia: {mw}MW."
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status)
            VALUES ('M82_TRANSITION_ENGINE', ?, 'PENDING')
        """, (headline,))

    conn.commit()
    conn.close()
    
    print(f"📊 [M82 TRANSITION ENGINE] Fecha: {today} | Score: {score}/100 | Flag: {flag}")

if __name__ == "__main__":
    # Lectura actual de parámetros
    # Rigs: 1 activo (de 11 prometidos), Termozulia: 320MW, Diésel: $6.52, Escrow al régimen: 85%, Racionamiento Zulia: 8h
    update_index(rigs=1, mw=320, diesel=6.52, escrow_pct=85.0, hours_off=8)
