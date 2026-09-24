import os

DAEMONS = [
    ("m82_unga_summit_tracker_daemon.py", "UNGA_NYC_TRACKER", "UNGA OR Trump OR Zelenskyy OR Hormuz"),
    ("m82_refinitiv_global_chain_daemon.py", "REFINITIV_GLOBAL_CHAIN", "ADR OR GDR OR cross-listing arbitrage"),
    ("m82_refinitiv_venues_charts_daemon.py", "REFINITIV_VENUES", "dark pool OR off-exchange volume"),
    ("m82_reuters_breakingviews.py", "REUTERS_BREAKINGVIEWS", "Reuters breakingviews OR M&A deal"),
    ("m82_macro_daemon.py", "MACRO_GLOBAL", "Federal Reserve OR ECB OR Interest Rates"),
    ("m82_scheduler_v9.py", "SCHEDULER_V9", "Central Bank Schedule OR Earnings Calendar"),
    ("m82_crypto_commodities_daemon.py", "CRYPTO_COMMODITIES", "Bitcoin OR Crude Oil OR Gold Futures"),
    ("m82_musk_empire_daemon.py", "MUSK_EMPIRE", "Tesla OR SpaceX OR xAI OR Starlink"),
    ("m82_insiders_top100_daemon.py", "INSIDERS_TOP100", "SEC Form 4 OR Insider Buying OR Insider Selling"),
    ("m82_debt_credit_daemon.py", "DEBT_CREDIT", "High Yield Bonds OR Credit Default Swaps OR Corporate Debt"),
    ("m82_valuation_peers_daemon.py", "VALUATION_PEERS", "Multiple Expansion OR PE Ratio OR EV/EBITDA"),
    ("m82_governance_officers_daemon.py", "GOVERNANCE_OFFICERS", "CEO Resignation OR Board Member Proxy"),
    ("m82_esg_sustainability_daemon.py", "ESG_SUSTAINABILITY", "ESG Rating OR Sustainability Bond"),
    ("m82_lseg_green_economy_daemon.py", "LSEG_GREEN_ECONOMY", "Green Economy Mark OR LSEG GRCS"),
    ("m82_financials_fundamentals_daemon.py", "FINANCIALS_FUNDAMENTALS", "Q3 Earnings OR Balance Sheet OR Revenue Beat"),
    ("m82_estimates_analysts_daemon.py", "ESTIMATES_ANALYSTS", "Analyst Upgrade OR Target Price Cut"),
    ("m82_news_research_daemon.py", "NEWS_RESEARCH", "Equity Research OR Wall Street Note"),
    ("m82_venues_exchanges_daemon.py", "VENUES_EXCHANGES", "NYSE OR Nasdaq OR LSE Market Microstructure"),
    ("m82_orderbook_microstructure_daemon.py", "ORDERBOOK_MICROSTRUCTURE", "Order Book Imbalance OR Spoofing Detection"),
    ("m82_economic_polls_macro_daemon.py", "ECONOMIC_POLLS_MACRO", "CPI Inflation OR Non-Farm Payrolls"),
    ("m82_global_markets_movers_daemon.py", "GLOBAL_MARKETS_MOVERS", "S&P 500 Rally OR Market Selloff"),
    ("m82_top_news_geopolitics_daemon.py", "TOP_NEWS_GEOPOLITICS", "Taiwan Strait OR Middle East Escalation"),
    ("m82_lseg_notebook_daemon.py", "LSEG_NOTEBOOK", "LSEG Workspace OR Refinitiv Eikon Data"),
    ("m82_jupyter_metadata_daemon.py", "JUPYTER_METADATA", "Quant Analysis OR Portfolio Backtest"),
    ("m82_jupyter_kernel_daemon.py", "JUPYTER_KERNEL", "Algorithm Signal Execution"),
    ("m82_bloomberg_terminal_daemon.py", "BLOOMBERG_TERMINAL", "Bloomberg Terminal First Word Alerts"),
    ("m82_private_markets_daemon.py", "PRIVATE_MARKETS", "Venture Capital OR Private Equity Buyout"),
    ("m82_lseg_news_wsj_daemon.py", "LSEG_NEWS_WSJ", "Wall Street Journal Breaking Markets"),
    ("m82_treasury_bonds_daemon.py", "TREASURY_BONDS", "10-Year Yield OR Treasury Auction"),
    ("m82_geopolitics_ai_daemon.py", "GEOPOLITICS_AI", "AI Regulations OR Semiconductor Sanctions"),
    ("m82_market_monitor_daemon.py", "MARKET_MONITOR", "VIX Index OR Market Volatility Spike"),
    ("m82_realtime_wire_daemon.py", "REALTIME_WIRE", "Dow Jones Newswires OR PR Newswire Breaking"),
    ("m82_interactive_brokers_daemon.py", "INTERACTIVE_BROKERS", "IBKR Order Routing OR Margin Rates"),
    ("m82_venezuela_legitimacy_daemon.py", "VENEZUELA_LEGITIMACY", "Citgo Auction OR OFAC Sanctions License OR Chevron Venezuela"),
    ("m82_kpler_flow_predictor.py", "KPLER_FLOW_PREDICTOR", "Oil Tanker Tracking OR Hormuz Strait Flow")
]

template = """#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{tag}] {{msg}}", flush=True)

def insert_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        ''', ('{tag}', headline))
        conn.commit()
        log(f"✅ Señal Capturada: {{headline[:60]}}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error DB: {{e}}")

def scan():
    url = f"https://news.google.com/rss/search?q={query_str}&hl=en-US&gl=US&ceid=US:en"
    try:
        r = requests.get(url, headers={{'User-Agent': 'Mozilla/5.0'}}, timeout=10)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                insert_headline(title.strip())
    except Exception as e:
        log(f"⚠️ Error escaneando feed: {{e}}")

def main():
    init_db()
    log("📡 Daemon en ejecución continua...")
    while True:
        scan()
        time.sleep(180)

if __name__ == "__main__":
    main()
"""

for filename, tag, query in DAEMONS:
    filepath = os.path.expanduser(f"~/M82/{filename}")
    if not os.path.exists(filepath):
        query_formatted = query.replace(" ", "+")
        content = template.format(tag=tag, query_str=query_formatted)
        with open(filepath, "w") as f:
            f.write(content)
        os.chmod(filepath, 0o755)

print("✅ Todos los 35 Daemons fueron estructurados e inicializados.")
