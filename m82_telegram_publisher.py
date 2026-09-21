#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import requests

# 1. Configuración de credenciales de Telegram
# Puedes poner tus datos directos entre las comillas si no usas variables de entorno
TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "TU_TOKEN_AQUI")
CHAT_ID = os.getenv("M82_TELEGRAM_CHAT", "TU_CHAT_ID_AQUI")

# Ruta de la base de datos de Termux
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def send_telegram_message(message):
    """Envía un mensaje a la API de Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"[ERROR API TELEGRAM] Código {response.status_code}: {response.text}", flush=True)
            return False
    except Exception as e:
        print(f"[EXCEPCIÓN DE RED] No se pudo conectar a Telegram: {e}", flush=True)
        return False

def process_pending_news():
    """Consulta SQLite y envía las noticias con estado PENDING."""
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] No se encuentra la base de datos en: {DB_PATH}", flush=True)
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Selecciona hasta 5 noticias no enviadas
        cursor.execute("""
            SELECT id, daemon_source, headline 
            from m82_multi_stream 
            WHERE status = 'PENDING' 
            LIMIT 5
        """)
        rows = cursor.fetchall()

        if not rows:
            print("[INFO] Sin noticias pendientes en la cola.", flush=True)

        for row_id, source, headline in rows:
            # Formato de publicación
            msg = (
                f"🚨 *#M82 BREAKING SUMMARY*\n\n"
                f"🔴 *[{source.upper()}]*\n"
                f"{headline}\n\n"
                f"🏛 @MolinaHoldings LLC"
            )

            print(f"[PROCESANDO] Enviando ID {row_id}: {headline[:40]}...", flush=True)

            if send_telegram_message(msg):
                cursor.execute("""
                    UPDATE m82_multi_stream 
                    SET status = 'SENT_TELEGRAM' 
                    WHERE id = ?
                """, (row_id,))
                conn.commit()
                print(f"[EXITO] Noticia ID {row_id} enviada y actualizada.", flush=True)
            else:
                print(f"[FALLO] No se pudo enviar el ID {row_id}. Se reintentará luego.", flush=True)

            time.sleep(2) # Pausa entre envíos para evitar límites de tasa

        conn.close()

    except Exception as e:
        print(f"[ERROR SQLITE] Fallo en la base de datos: {e}", flush=True)

def main():
    print("=== INICIANDO SERVICIO DE PUBLICACIÓN M82 TELEGRAM ===", flush=True)
    if TOKEN == "TU_TOKEN_AQUI" or CHAT_ID == "TU_CHAT_ID_AQUI":
        print("[ADVERTENCIA] Por favor configura el TOKEN y CHAT_ID antes de continuar.", flush=True)

    while True:
        process_pending_news()
        time.sleep(20) # Revisa la base de datos cada 20 segundos

if __name__ == "__main__":
    main()
