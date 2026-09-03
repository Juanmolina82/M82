from http.server import BaseHTTPRequestHandler, HTTPServer
import json, sys
from pathlib import Path
from datetime import datetime, timezone

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return # Desactivar logs por defecto del HTTP server para mantener la consola limpia

    def do_POST(self):
        if self.path == '/m82-context':
            length = int(self.headers.get('content-length', 0))
            data = json.loads(self.rfile.read(length))
            
            # Extraer ticker recibido
            inst = data.get('instrument', {})
            ticker = inst.get('ric') or inst.get('ticker') or inst.get('symbol') if isinstance(inst, dict) else str(inst)
            
            print(f"⚡ [SxS EVENT DETECTED]: Instrumento -> {ticker}")
            
            # Guardar evidencia en la ruta runtime de M82
            runtime_dir = Path.home() / ".M82" / "runtime" / "market"
            runtime_dir.mkdir(parents=True, exist_ok=True)
            
            payload = {
                "source": "LSEG_Workspace_SxS",
                "ticker": ticker,
                "captured_utc": datetime.now(timezone.utc).toISOString(),
                "node": "CARACAS",
                "raw": data
            }
            
            # Archivo de disparo para el escáner v17
            trigger_file = runtime_dir / "latest_sxs_trigger.json"
            with open(trigger_file, 'w') as f:
                json.dump(payload, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","m82":"context queued"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Manejo de CORS Preflight para llamados Fetch desde el navegador
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print("🏛️ [M82 SxS GATEWAY]: Escuchando eventos de LSEG en 127.0.0.1:8081...")
HTTPServer(("127.0.0.1", 8081), Handler).serve_forever()
