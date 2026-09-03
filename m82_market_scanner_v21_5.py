import os, time, requests, asyncio, json
from datetime import datetime, timezone
from collections import defaultdict
from telegram import Bot

TOKEN = os.getenv('M82_BOT_TOKEN')
CHAT_ID = os.getenv('M82_CHAIRMAN_ID')
bot = Bot(token=TOKEN) if TOKEN else None

ALL_TICKERS = [
    "OIH","SLB","HAL","BKR","XLE","USO","CL=F","OXY","CVX","XOM",
    "NVDA","PLTR","VGT","XLK","SMH","QQQ","AVGO","VST","KKR","VRT",
    "RUN","MRVL","SOXX","AMD","MSFT","ITA","VNQ","XLY","XLV","XRT",
    "WMT","AMZN","TSLA","TGT","NQ=F","YM=F","ES=F","DX-Y.NYB","^TNX","^VIX"
]

HEATMAP_PATH = "/data/data/com.termux/files/home/M82/m82_heatmap_last.json"
EVIDENCE_LOG_PATH = "/data/data/com.termux/files/home/M82/m82_evidence_log.json"
last_alert = defaultdict(lambda: 0)

def fetch_data(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        j = r.json()['chart']['result'][0]
        m = j['meta']
        p = m.get('regularMarketPrice', 0)
        prev = m.get('chartPreviousClose', p)
        pct = ((p - prev) / prev * 100) if prev else 0
        hi = m.get('regularMarketDayHigh', p)
        lo = m.get('regularMarketDayLow', p)
        v = j['indicators']['quote'][0].get('volume', [])
        vol = v[-1] if v and v[-1] else 0
        return {"p": p, "pct": pct, "h": hi, "l": lo, "v": vol}
    except Exception as e:
        return None

async def send_telegram(msg):
    if bot and CHAT_ID:
        try:
            await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"Error envío Telegram: {e}")

def save_evidence(prices):
    try:
        payload = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "entity": "Molina Holdings LLC / Molina Global LLC",
            "terminal": "M82 CORE V6",
            "prices": prices
        }
        with open(EVIDENCE_LOG_PATH, "a") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        print(f"Error log evidencia: {e}")

async def generate_mega_report(prices):
    hm_txt = "Sin datos de Heatmap"
    try:
        if os.path.exists(HEATMAP_PATH):
            with open(HEATMAP_PATH, "r") as f:
                data = json.load(f)
                hm_map = data.get("map", {})
                if hm_map:
                    hm_txt = ", ".join([f"{k}: {v:+.2f}%" for k, v in hm_map.items()])
    except Exception:
        pass

    now_vet = datetime.now().strftime('%d/%m/%Y %H:%M VET')
    
    wti = prices.get('CL=F', {"p": 0.0, "pct": 0.0})
    oih = prices.get('OIH', {"p": 0.0, "pct": 0.0})
    xle = prices.get('XLE', {"p": 0.0, "pct": 0.0})
    spread = oih["pct"] - xle["pct"]

    nq = prices.get('NQ=F', {"p": 0.0, "pct": 0.0, "h": 0.0, "l": 0.0, "v": 0})
    ym = prices.get('YM=F', {"p": 0.0, "pct": 0.0})
    es = prices.get('ES=F', {"p": 0.0, "pct": 0.0})
    vix = prices.get('^VIX', {"p": 0.0, "pct": 0.0})
    dxy = prices.get('DX-Y.NYB', {"p": 0.0})
    tnx = prices.get('^TNX', {"p": 0.0})

    longs = sorted([(k, v) for k, v in prices.items() if k in ["NVDA","PLTR","VGT","XLK","SMH","QQQ","AVGO","MRVL","RUN"]], key=lambda x: x[1]['pct'], reverse=True)[:5]
    shorts = sorted([(k, v) for k, v in prices.items() if k in ["ITA","VNQ","XLY","XLV","XRT","WMT","AMZN","TSLA","TGT"]], key=lambda x: x[1]['pct'])[:5]

    txt = f"🏛️ *MOLINA HOLDINGS LLC / MOLINA GLOBAL LLC*\n"
    txt += f"📡 *M82 CORE V6 — MACRO INTELLIGENCE TERMINAL*\n"
    txt += f"⏱️ {now_vet} | Caracas Operating Node\n"
    txt += "────────────────────────────────────\n"
    txt += "💥 *GEOINTEL (BLOOMBERG): VENEZUELA WEIGHS OPEC EXIT*\n"
    txt += "• US Oil Stake Talks Active | Free Market Supply Realignment\n"
    txt += "────────────────────────────────────\n"
    txt += f"🏛️ POLICY: DXY {dxy['p']:.2f} | 10Y {tnx['p']:.2f}% | VIX {vix['p']:.2f}\n"
    txt += "────────────────────────────────────\n"
    txt += "⚡ *FUTURES (INDICATIVE DATA):*\n"
    txt += f"• NQ {nq['p']:.2f} {'🟢' if nq['pct']>0 else '🔴'} {nq['pct']:+.2f}% | H:{nq['h']:.2f} L:{nq['l']:.2f}\n"
    txt += f"• ES {es['p']:.2f} {es['pct']:+.2f}% | YM {ym['p']:.0f} {ym['pct']:+.2f}%\n"
    txt += f"🛢️ WTI ${wti['p']:.2f} {wti['pct']:+.2f}%\n"
    txt += "────────────────────────────────────\n"
    txt += f"🦅 *ENERGY & OFAC MAP:*\n{hm_txt}\n"
    for sym in ["OIH","SLB","HAL","BKR","XLE","USO","CVX","OXY","XOM"]:
        if sym in prices:
            txt += f"• {sym}: ${prices[sym]['p']:.2f} ({prices[sym]['pct']:+.2f}%)\n"
    txt += f"⚡ SPREAD OIH-XLE: {spread:+.2f}% {'🚨 ROTACIÓN SERVICIOS' if spread>=2.0 else ''}\n"
    txt += "────────────────────────────────────\n"
    txt += "🔋 *POWER TRIANGLE HELIX JV:*\n"
    for sym in ["VST","NVDA","KKR","VRT"]:
        if sym in prices:
            txt += f"{sym} ${prices[sym]['p']:.2f} ({prices[sym]['pct']:+.2f}%) | "
    txt += "\n────────────────────────────────────\n"
    txt += "🔥 *TOP LONG (RESEARCH):*\n"
    for s, d in longs:
        txt += f"• {s}: {d['pct']:+.2f}% | ${d['p']:.2f}\n"
    txt += "\n📉 *BOTTOM SHORT (RESEARCH):*\n"
    for s, d in shorts:
        txt += f"• {s}: {d['pct']:+.2f}% | ${d['p']:.2f}\n"
    txt += "════════════════════════════════════\n"
    txt += "M82 CORE V6 • CARACAS OPERATING NODE\n"
    txt += "_Informational research only. No trade execution or investment advice._"

    await send_telegram(txt)
    save_evidence(prices)

async def main_loop():
    await send_telegram("⚡ *M82 CORE V6 ONLINE*\nCaracas Operating Node activo. Bypass SSL removido, conexión TLS segura establecida.")
    cache = {}
    for s in ALL_TICKERS:
        d = fetch_data(s)
        if d:
            cache[s] = d
        await asyncio.sleep(0.15)
    
    if cache:
        await generate_mega_report(cache)
    
    last_hourly = time.time()
    while True:
        now = time.time()
        for s in ALL_TICKERS:
            d = fetch_data(s)
            if not d:
                continue
            cache[s] = d
            if now - last_alert[s] < 400:
                continue
            
            ev = None
            if s == "CL=F" and abs(d['pct']) >= 2.0:
                ev = f"🛢️ ALERTA WTI PETRÓLEO {d['pct']:+.2f}% (Bloomberg OPEC Event)"
            if s in ["CVX", "OXY", "SLB", "HAL"] and d['pct'] >= 3.0:
                ev = f"🚀 IMPULSO ENERGÍA {s} {d['pct']:+.2f}%"
            if s == "NQ=F" and d['p'] < 29500 and d['p'] > 0:
                ev = "🚨 NQ SOPORTE PERDIDO"
                
            if ev:
                last_alert[s] = now
                await send_telegram(f"⏱ {datetime.now().strftime('%H:%M:%S')} *{s}* ${d['p']:.2f} ({d['pct']:+.2f}%)\n{ev}\n\n_Informational alert - Non-executable_")
        
        if now - last_hourly >= 3600:
            last_hourly = now
            if cache:
                await generate_mega_report(cache)
                
        await asyncio.sleep(35)

if __name__ == '__main__':
    asyncio.run(main_loop())
