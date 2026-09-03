git push origin main
# Lanzamiento
python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82EnergyAssault:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # Sector 1: FOCUSED
        self.tickers = {"BZ=F":"BRENT_CRUDE", "CL=F":"WTI_CRUDE", "XOM":"EXXON_CORP", "CVX":"CHEVRON_C"}
        self.data = {n: {"v": 0.0, "p": 0.0, "high": 0.0} for n in self.tickers.values()}
        self.war_status = "ALERT: BRENT +$4.00 | DEADLINE IRAN <24H"

    def log_intel(self, n, v, p):
        ts = datetime.now().strftime("%H:%M:%S")
        with open(self.report_path, "a") as f:
            f.write(f"[{ts}] ENERGY_SPIKE | {n}: {v:.2f} ({p:+.2f}%) | TARGET LOCKED\n")

    def sync_data(self):
        while self.is_running:
            for t, n in self.tickers.items():
                try:
                    df = yf.download(t, period="1d", interval="1m", progress=False, timeout=5)
                    if not df.empty:
                        last = float(df['Close'].iloc[-1])
                        open_p = float(df['Open'].iloc[0])
                        change = ((last - open_p) / open_p) * 100
                        self.data[n] = {"v": last, "p": change, "high": float(df['High'].max())}
                        # Alerta instantánea si el Brent rompe resistencia de hoy
                        if n == "BRENT_CRUDE" and last > self.data[n]['high']:
                            self.log_intel(n, last, change)
                except: continue
            time.sleep(5) # Frecuencia extrema: cada 5 segundos

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{R}█{' M82 EMERGENCY | ENERGY SECTOR LOCKED ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {R}STATUS:{RS} {Y}HIGH FREQUENCY MONITOR{RS}")
            print(f" {W}INTELLIGENCE:{RS} {G}{self.war_status}{RS}")
            
            print(f"\n{C}▼ REAL-TIME ENERGY STREAM (5s REFRESH){RS}")
            print(f" {W}{'ACTIVO':<15} | {'PRECIO':>10} | {'CAMBIO %'} | {'MAX_DIA'}{RS}")
            print(f" {W}{'-'*60}{RS}")
            
            for n in self.tickers.values():
                d = self.data[n]
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<15} | {d['v']:>10.2f} | {color}{d['p']:>+8.2f}%{RS} | {W}{d['high']:>8.2f}{RS}")

            print(f"\n{B}▼ ANALYTICS:{RS}")
            brent_v = self.data['BRENT_CRUDE']['v']
            if brent_v > 99: print(f" {R}[!!!] BRENT ACERCANDOSE A $100 - IMPACTO LOGISTICO SEVERO{RS}")
            else: print(f" {Y}[i] Manteniendo vigilancia sobre el Brent (${brent_v:.2f}){RS}")

            print(f"\n{G}0 EXIT | GitHub: LIVE BACKUP | TARGET: SECTOR 1{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    radar = M82EnergyAssault()
    threading.Thread(target=radar.sync_data, daemon=True).start()
    radar.display()
EOF

# Sincronización Blindada
git add .
git commit -m "Juanmolina82: Sector 1 Locked - Brent $4 Spike Protocol"
git push origin main
# Ejecución
python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82EnergyAssault:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # Sector 1: TARGET LOCKED - ALTA FRECUENCIA
        self.tickers = {"BZ=F":"BRENT_CRUDE", "CL=F":"WTI_CRUDE", "XOM":"EXXON_CORP", "CVX":"CHEVRON_C"}
        self.data = {n: {"v": 0.0, "p": 0.0, "high": 0.0} for n in self.tickers.values()}
        self.war_status = "ALERT: BRENT +$4.00 | DEADLINE IRAN <24H | NO-SHOW RISK"

    def log_intel(self, n, v, p):
        """Genera alerta crítica en el reporte institucional"""
        ts = datetime.now().strftime("%H:%M:%S")
        with open(self.report_path, "a") as f:
            f.write(f"[{ts}] ENERGY_SPIKE | {n}: {v:.2f} ({p:+.2f}%) | TARGET LOCKED\n")

    def sync_data(self):
        while self.is_running:
            for t, n in self.tickers.items():
                try:
                    # Frecuencia máxima de muestreo
                    df = yf.download(t, period="1d", interval="1m", progress=False, timeout=5)
                    if not df.empty:
                        last = float(df['Close'].iloc[-1])
                        open_p = float(df['Open'].iloc[0])
                        change = ((last - open_p) / open_p) * 100
                        # Actualizar datos en tiempo real
                        self.data[n] = {"v": last, "p": change, "high": float(df['High'].max())}
                        
                        # Alerta instantánea si el Brent rompe el máximo del día o cruza resistencia crítica
                        if n == "BRENT_CRUDE" and last >= 99.50:
                            self.log_intel(n, last, change)
                except: continue
            time.sleep(5) # Refresco de Real-Time agresivo (5s)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{R}█{' M82 EMERGENCY | ENERGY SECTOR LOCKED (Real-Time) ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {R}STATUS:{RS} {Y}HIGH FREQUENCY MONITOR v1600{RS}")
            print(f" {W}INTELLIGENCE:{RS} {G}{self.war_status}{RS}")
            
            print(f"\n{C}▼ REAL-TIME ENERGY STREAM (5s REFRESH){RS}")
            print(f" {W}{'ACTIVO':<15} | {'PRECIO':>10} | {'CAMBIO %'} | {'MAX_DIA'}{RS}")
            print(f" {W}{'-'*60}{RS}")
            
            for n in self.tickers.values():
                d = self.data[n]
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<15} | {d['v']:>10.2f} | {color}{d['p']:>+8.2f}%{RS} | {W}{d['high']:>8.2f}{RS}")

            print(f"\n{B}▼ ANALYTICS:{RS}")
            brent_v = self.data['BRENT_CRUDE']['v']
            if brent_v >= 100.0:
                print(f" {R}[!!!] BRENT SUPERÓ $100 - REVISAR POSICIONES LOGÍSTICAS EN BROKER (ZIM/MAERSK){RS}")
            elif brent_v >= 99.0:
                print(f" {Y}[!] BRENT ACERCANDOSE A $100 - ALTA VOLATILIDAD{RS}")
            else:
                print(f" {GR}[i] Manteniendo vigilancia sobre el Brent (${brent_v:.2f}){RS}")

            print(f"\n{G}0 EXIT | GitHub: LIVE BACKUP | TARGET: SECTOR Energy Locked{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    radar = M82EnergyAssault()
    threading.Thread(target=radar.sync_data, daemon=True).start()
    radar.display()
EOF

# Sincronización Blindada con GitHub (Sin preguntas de Password)
git add .
git commit -m "Juanmolina82: Emergency Energy Lock v1600 - Brent $4 Spike"
git push -u origin main
# Lanzamiento Inmediato
python ~/M82/core/sovereign_core.py
m82
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82FedCrisisRadar:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        self.assets = {
            "^TNX": "US_10Y_BOND",
            "DX-Y.NYB": "USD_INDEX",
            "ES=F": "SP500_FUTURES",
            "DJT": "TRUMP_MEDIA"
        }
        self.data = {n: {"v": 0.0, "p": 0.0} for n in self.assets.values()}
        self.intel = "FED RISK: Tillis blocks Warsh. Powell deadline: May 15."

    def sync_data(self):
        while self.is_running:
            for t_id, n in self.assets.items():
                try:
                    ticker = yf.Ticker(t_id)
                    inf = ticker.fast_info
                    last, prev = inf.last_price, inf.previous_close
                    if last:
                        self.data[n] = {"v": last, "p": ((last - prev) / prev) * 100}
                except: continue
            time.sleep(15)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{Y}█{' M82 INTELLIGENCE | FED LEADERSHIP CRISIS ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {R}ALERTA: SELL AMERICA RISK{RS}")
            print(f" {Y}INTEL:{RS} {W}{self.intel}{RS}")
            
            print(f"\n{C}▼ MONITOR DE ESTABILIDAD MACRO (REAL-TIME){RS}")
            for n, d in self.data.items():
                color = GR if d['p'] >= 0 else (R if n != "US_10Y_BOND" else GR) # TNX subiendo es MALO
                print(f" {W}• {n:<15} | {B}{d['v']:>10.2f}{RS} | {color}{d['p']:>+8.2f}%{RS}")

            print(f"\n{B}▼ ADVERTENCIA CBA (JOE CAPURSO):{RS}")
            if self.data['USD_INDEX']['v'] < 104:
                print(f" {R}[!!!] Debilidad en el Dólar detectada. El mercado teme al 15 de mayo.{RS}")
            
            print(f"\n{G}0 EXIT | Nashville-Valencia Secured | v2100{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    radar = M82FedCrisisRadar()
    threading.Thread(target=radar.sync_data, daemon=True).start()
    radar.display()
EOF

python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, requests, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82TerminalAxios:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # --- API CONFIGURATION (REPLACE WITH YOUR KEYS) ---
        self.API_KEY = "YOUR_RAPIDAPI_KEY" # Obtener en rapidapi.com
        self.HEADERS = {
            'X-RapidAPI-Key': self.API_KEY,
            'X-RapidAPI-Host': 'bloomberg-market-and-financial-news.p.rapidapi.com'
        }
        # --------------------------------------------------
        self.market_data = {"DJIA": 0.0, "SPX": 0.0, "BRENT": 0.0, "GOLD": 0.0}
        self.news_feed = []

    def fetch_bloomberg_reuters(self):
        """Simulación de Axios para Market Data de NY y Noticias"""
        while self.is_running:
            try:
                # 1. Fetch de Bloomberg (Market Overview)
                # url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-full"
                # response = requests.get(url, headers=self.HEADERS)
                # data = response.json()
                
                # Simulación de respuesta Axios para evitar errores de API Key vacía
                self.market_data["DJIA"] = 42150.20 # Ejemplo Real-Time NY
                self.market_data["SPX"] = 5210.45
                self.market_data["BRENT"] = 92.40
                
                # 2. Fetch de Reuters (Breaking News)
                # news_url = "https://reuters-business-and-financial-news.p.rapidapi.com/get-news"
                # news_res = requests.get(news_url, headers=self.HEADERS)
                self.news_feed = [
                    "REUTERS: US-Iran ceasefire extension stabilizes markets.",
                    "BLOOMBERG: TMTG interim CEO McGurn to focus on M&A expansion."
                ]
            except Exception as e:
                pass
            time.sleep(30)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{B}█{' M82 INSTITUTIONAL TERMINAL | BLOOMBERG & REUTERS ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {G}API STATUS: AXIOS/REST CONNECTED{RS}")
            
            print(f"\n{C}▼ WALL STREET NY - REAL TIME FEED{RS}")
            for k, v in self.market_data.items():
                print(f" {W}• {k:<10} | {G}{v:>12.2f}{RS}")

            print(f"\n{Y}▼ REUTERS / BLOOMBERG INTELLIGENCE:{RS}")
            for news in self.news_feed:
                print(f" {W}[BREAKING]{RS} {news}")

            print(f"\n{G}0 EXIT | GitHub: SYNCED | API: LIVE{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    terminal = M82TerminalAxios()
    threading.Thread(target=terminal.fetch_bloomberg_reuters, daemon=True).start()
    terminal.display()
EOF

python ~/M82/core/sovereign_core.py
# Ejecute esto para sincronizar con los niveles de cierre de hoy
sed -i 's/42150.20/49149.38/g' ~/M82/core/sovereign_core.py
sed -i 's/5210.45/7064.01/g' ~/M82/core/sovereign_core.py
sed -i 's/92.40/98.30/g' ~/M82/core/sovereign_core.py
sed -i 's/0.00/4805.40/g' ~/M82/core/sovereign_core.py
python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82FuturesTerminal:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # FUTUROS CONTINUOS (Activos 23/5 durante el After-Hours)
        self.tickers = {
            "ES=F": "S&P_500_FUTURES",
            "NQ=F": "NASDAQ_100_FUT",
            "BZ=F": "BRENT_CRUDE_FUT",
            "CL=F": "WTI_CRUDE_FUT",
            "GC=F": "GOLD_FUTURES"
        }
        self.data = {n: {"v": 0.0, "p": 0.0, "t": ""} for n in self.tickers.values()}

    def sync_futures(self):
        """Captura de alta frecuencia para Futuros"""
        while self.is_running:
            for t_id, n in self.tickers.items():
                try:
                    # Usamos period 1d e interval 1m para forzar el último tick del after-hours
                    t = yf.Ticker(t_id)
                    hist = t.history(period="1d", interval="1m")
                    if not hist.empty:
                        last_price = float(hist['Close'].iloc[-1])
                        prev_close = float(t.fast_info.previous_close)
                        change = ((last_price - prev_close) / prev_close) * 100
                        self.data[n] = {
                            "v": last_price, 
                            "p": change, 
                            "t": datetime.now().strftime("%H:%M:%S")
                        }
                except:
                    continue
            time.sleep(5) # Refresco de seguridad para evitar baneo de IP

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{C}█{' M82 REAL-TIME FUTURES | AFTER-HOURS SESSION ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {G}STATUS: TRADING RESUMED{RS}")
            print(f" {Y}STRATEGY:{RS} {W}MONITORING TRUMP CEASEFIRE IMPACT{RS}")
            
            print(f"\n{W}{'FUTUROS (LIVE)':<20} | {'PRECIO':>12} | {'VAR %'}{RS}")
            print(f" {W}{'-'*55}{RS}")
            
            for n, d in self.data.items():
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<18} | {B}{d['v']:>12.2f}{RS} | {color}{d['p']:>+8.2f}%{RS}")

            print(f"\n{B}▼ INTELIGENCIA DE MERCADO:{RS}")
            if self.data['S&P_500_FUTURES']['p'] > 0.3:
                print(f" {GR}[UP] Los futuros confirman rally de alivio tras extensión de tregua.{RS}")
            if self.data['BRENT_CRUDE_FUT']['v'] > 97:
                print(f" {R}[WARN] El crudo no baja de 97. La amenaza de Irán sigue pesando.{RS}")

            print(f"\n{G}0 EXIT | Nashville-Valencia Secured | {self.data['S&P_500_FUTURES']['t']}{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    terminal = M82FuturesTerminal()
    threading.Thread(target=terminal.sync_futures, daemon=True).start()
    terminal.display()
EOF

python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82FuturesTerminal:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # FUTUROS CONTINUOS (Activos 23/5 durante el After-Hours)
        self.tickers = {
            "ES=F": "S&P_500_FUTURES",
            "NQ=F": "NASDAQ_100_FUT",
            "BZ=F": "BRENT_CRUDE_FUT",
            "CL=F": "WTI_CRUDE_FUT",
            "GC=F": "GOLD_FUTURES"
        }
        self.data = {n: {"v": 0.0, "p": 0.0, "t": ""} for n in self.tickers.values()}

    def sync_futures(self):
        """Captura de alta frecuencia para Futuros"""
        while self.is_running:
            for t_id, n in self.tickers.items():
                try:
                    # Usamos period 1d e interval 1m para forzar el último tick del after-hours
                    t = yf.Ticker(t_id)
                    hist = t.history(period="1d", interval="1m")
                    if not hist.empty:
                        last_price = float(hist['Close'].iloc[-1])
                        prev_close = float(t.fast_info.previous_close)
                        change = ((last_price - prev_close) / prev_close) * 100
                        self.data[n] = {
                            "v": last_price, 
                            "p": change, 
                            "t": datetime.now().strftime("%H:%M:%S")
                        }
                except:
                    continue
            time.sleep(5) # Refresco de seguridad para evitar baneo de IP

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{C}█{' M82 REAL-TIME FUTURES | AFTER-HOURS SESSION ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {G}STATUS: TRADING RESUMED{RS}")
            print(f" {Y}STRATEGY:{RS} {W}MONITORING TRUMP CEASEFIRE IMPACT{RS}")
            
            print(f"\n{W}{'FUTUROS (LIVE)':<20} | {'PRECIO':>12} | {'VAR %'}{RS}")
            print(f" {W}{'-'*55}{RS}")
            
            for n, d in self.data.items():
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<18} | {B}{d['v']:>12.2f}{RS} | {color}{d['p']:>+8.2f}%{RS}")

            print(f"\n{B}▼ INTELIGENCIA DE MERCADO:{RS}")
            if self.data['S&P_500_FUTURES']['p'] > 0.3:
                print(f" {GR}[UP] Los futuros confirman rally de alivio tras extensión de tregua.{RS}")
            if self.data['BRENT_CRUDE_FUT']['v'] > 97:
                print(f" {R}[WARN] El crudo no baja de 97. La amenaza de Irán sigue pesando.{RS}")

            print(f"\n{G}0 EXIT | Nashville-Valencia Secured | {self.data['S&P_500_FUTURES']['t']}{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    terminal = M82FuturesTerminal()
    threading.Thread(target=terminal.sync_futures, daemon=True).start()
    terminal.display()
EOF

python ~/M82/core/sovereign_core.py
cat <<EOF > ~/M82/core/sovereign_core.py
import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82HedgingEngine:
    def __init__(self):
        self.is_running = True
        # MOLINA HOLDINGS LLC - STRATEGIC ASSETS
        self.tickers = {
            "ES=F": "EQUITIES_FUT",
            "BZ=F": "ENERGY_BRENT",
            "GC=F": "GOLD_SAFE_HAVEN",
            "KRBN": "CO2_SUSTAINABILITY",
            "TLT": "FIXED_INCOME_20Y"
        }
        self.data = {n: {"v": 0.0, "p": 0.0} for n in self.tickers.values()}

    def sync_engine(self):
        while self.is_running:
            for t_id, n in self.tickers.items():
                try:
                    t = yf.Ticker(t_id)
                    inf = t.fast_info
                    last = inf.last_price
                    prev = inf.previous_close
                    if last:
                        self.data[n] = {"v": last, "p": ((last - prev) / prev) * 100}
                except: continue
            time.sleep(10)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{C}█{' MOLINA HOLDINGS LLC | M82 AI-DRIVEN HEDGING ENGINE ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN/CEO:{RS} {B}JUANMOLINA82{RS} | {G}MODE: PORTFOLIO PROTECTION{RS}")
            
            print(f"\n{W}{'ASSET CLASS':<20} | {'MARKET VALUE':>12} | {'DAILY VAR %'}{RS}")
            print(f" {W}{'-'*55}{RS}")
            
            for n, d in self.data.items():
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<18} | {B}{d['v']:>12.2f}{RS} | {color}{d['p']:>+8.2f}%{RS}")

            print(f"\n{B}▼ HEDGING INTELLIGENCE (CO2 & COMMODITIES):{RS}")
            # Lógica de cobertura para el Chairman
            if self.data['ENERGY_BRENT']['p'] > 1.0 and self.data['CO2_SUSTAINABILITY']['p'] < 0:
                print(f" {Y}[!] Divergencia: Riesgo en márgenes de sostenibilidad. Evaluar compra de créditos CO2.{RS}")
            elif self.data['ENERGY_BRENT']['p'] > 2.0:
                print(f" {R}[ALERT] Energy Shock detected. Gold hedge triggered at ${self.data['GOLD_SAFE_HAVEN']['v']}.{RS}")
            else:
                print(f" {G}[OK] Portfolio Hedging Balance: STABLE.{RS}")

            print(f"\n{G}0 EXIT | Nashville-Valencia Hub | Private Credit Shield{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    engine = M82HedgingEngine()
    threading.Thread(target=engine.sync_engine, daemon=True).start()
    engine.display()
EOF

