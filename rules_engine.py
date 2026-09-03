import json, os

def evaluate_movers_anomaly(metrics):
    alerts = []
    movers = metrics.get("MOVERS_ALERT", {})
    
    for ticker, change in movers.items():
        if change <= -5.0:
            alerts.append({
                "type": "SELL_OFF_ANOMALY",
                "ticker": ticker,
                "change": change,
                "action": f"FLUSH DETECTADO EN {ticker} ({change}%). Revisar soporte técnico."
            })
        elif change >= 5.0:
            alerts.append({
                "type": "RALLY_ANOMALY",
                "ticker": ticker,
                "change": change,
                "action": f"BREAKOUT DETECTADO EN {ticker} (+{change}%)."
            })
            
    return alerts

if __name__ == "__main__":
    metrics_path = os.path.expanduser('~/M82/metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            m = json.load(f)
        results = evaluate_movers_anomaly(m)
        print(f"[RULES ENGINE] Anomalías detectadas en ciclo: {len(results)}")
        for r in results:
            print(f" -> {r['action']}")
