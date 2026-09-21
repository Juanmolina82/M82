#!/usr/bin/env python3
import sqlite3, time, os, random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

DAEMON_SAMPLES = {
    "MACRO": ["US 10Y Yield Surges to 4.25% Following Fed Policy Update", "CPI Inflation Rate Adjusts to 2.8% YoY", "ECB Signals Rate Pause Amid Growth Concerns"],
    "SCHEDULER_V9": ["Cron Job Execution Completed: Task ID #9982", "Batch Engine Synchronization Successful", "Scheduled Pipeline Execution Completed"],
    "CRYPTO_COMMODITIES": ["Bitcoin Breakthrough: Replaces $68,500 Resistance Level", "Brent Crude Oil Holds $82/bbl Amid Supply Constraints", "Gold Spot Reaches New All-Time High"],
    "MUSK_EMPIRE": ["Tesla FSD Supervised V12.5 Deployed Globally", "SpaceX Starship Prepares for Orbital Test Flight", "xAI Launches Grok-2 Enterprise API Services"],
    "INSIDERS_TOP100": ["NVIDIA CEO Sells $15M in Planned Form 4 Filing", "Apple Board Member Acquires 50,000 Shares", "Microsoft Officer Executes Stock Option Rights"],
    "DEBT_CREDIT": ["Corporate Bond Spreads Tighten by 12 bps", "Moody's Revises Banking Sector Outlook to Stable", "High-Yield Debt Issuance Reaches Record High"],
    "VALUATION_PEERS": ["Tech Sector Forward P/E Ratio Rebalances to 24.5x", "EV/EBITDA Multiples Shift across S&P 500 Peers", "Discounted Cash Flow Model Revaluates Top 100"],
    "GOVERNANCE_OFFICERS": ["Board Approves Share Buyback Authorization of $10B", "New Chief Risk Officer Appointed at Major Bank", "Proxy Statement Highlights New Executive Compensation"],
    "ESG_SUSTAINABILITY": ["ESG Fund Inflows Rise by 18% Quarter-over-Quarter", "EU Taxonomies Standardized for Green Bonds", "Carbon Offset Credit Pricing Adjusts to Market Demand"],
    "FINANCIALS_FUNDAMENTALS": ["Q3 Revenue Surpasses Guidance by 8.4%", "Operating Margin Expands 150 bps Year-over-Year", "Free Cash Flow Conversion Reaches Record 92%"],
    "ESTIMATES_ANALYSTS": ["Goldman Sachs Upgrades AAPL to Conviction Buy", "Morgan Stanley Adjusts Price Target on NVDA to $150", "Consensus EPS Revision Index Moves Positive"],
    "NEWS_RESEARCH": ["Institutional Equity Research Highlights AI Value Chain", "Quant Desk Issues Tactical Market Allocation Report", "Sell-Side Analyst Sentiment Turns Bullish on Chips"],
    "VENUES_EXCHANGES": ["NYSE Order Matching Latency Reduced to Sub-Microsecond", "Nasdaq Dark Pool Volume Captures 14% Market Share", "Cboe Volatility Index Options Volume Hits Peak"],
    "ORDERBOOK_MICROSTRUCTURE": ["Order Book Liquidity Depth Spreads 2 bps Across Top Tickers", "High-Frequency Sweep Triggered Across Equities", "Bid-Ask Spread Compression Observed in Tech Stocks"],
    "ECONOMIC_POLLS_MACRO": ["University of Michigan Consumer Sentiment Hits 78.5", "ISM Manufacturing PMI Expands to 51.2", "Non-Farm Payroll Poll Consensus Settles at 180k"],
    "GLOBAL_MARKETS_MOVERS": ["Nikkei 225 Advances 1.8% Led by Semiconductor Stocks", "European Stoxx 600 Gains Momentum on Tech Surge", "Emerging Markets Index Outperforms S&P 500"],
    "TOP_NEWS_GEOPOLITICS": ["Trade Negotiations Resume Between Major Economies", "Energy Pipeline Agreement Signed in Central Europe", "Geopolitical Tension Eases Across Eastern Trade Routes"],
    "LSEG_NOTEBOOK": ["Refinitiv DataStream API Execution: Code 200 OK", "LSEG Quantitative Code Analytics Completed", "Notebook Kernel Processing Completed for Market Dataset"],
    "JUPYTER_METADATA": ["Notebook Metadata Schema Validated for Workspace", "Kernel Variable State Exported to Database", "Jupyter Pipeline Execution Checkpoint Saved"],
    "JUPYTER_KERNEL": ["Python 3.11 Kernel Idle Status Confirmed", "Async Execution Thread Finished in 42ms", "Memory Allocated: 256MB / Buffer Cleared"],
    "BLOOMBERG_TERMINAL": ["Bloomberg Terminal B-PIPE Feed Online", "PORT Risk Analytics Processing Portfolio Benchmark", "WCRP World Currency Rates Real-time Broadcast Active"],
    "PRIVATE_MARKETS": ["Preqin Report: Private Equity Dry Powder Hits $2.1T", "Infrastructure Fund Closes $5B Global Energy Deal", "Private Credit Direct Lending Rates Adjust Upward"],
    "LSEG_NEWS_WSJ": ["WSJ Pro: Institutional Funds Increase Tech Exposure", "Reuters Breakingviews: M&A Valuations Stabilize", "Central Bank Liquidity Operations Expand Balance Sheet"]
}

def fire_distinct_burst():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    total = 0
    
    for tag, headlines in DAEMON_SAMPLES.items():
        for headline in headlines:
            cursor.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (tag, headline))
            total += 1

    conn.commit()
    conn.close()
    print(f"✅ ¡RÁFAGA DIVERSIFICADA COMPLETADA! {total} mensajes únicos insertados (3 por cada uno de los 23 daemons).")

if __name__ == "__main__":
    fire_distinct_burst()
