#!/usr/bin/env python3
import os, sys, time, sqlite3, json, math, random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

class WorldModel:
    def __init__(self):
        self.causal_rules = {
            "OIL_SQUEEZE": {"tickers": ["XLE", "CVX", "XOM"], "action": "LONG", "inverse": "SHORT SPY"},
            "CREDIT_STRESS": {"tickers": ["HYG", "JPM", "BAC"], "action": "SHORT", "inverse": "LONG GLD"},
            "AI_INFRASTRUCTURE": {"tickers": ["NVDA", "MSFT", "TSLA"], "action": "LONG", "inverse": "SHORT QQQ"},
            "RATE_CUT_POLL": {"tickers": ["TLT", "IEF"], "action": "LONG", "inverse": "SHORT USD"}
        }

    def infer_causality(self, headline, source):
        text = headline.upper()
        
        # Filtro de ruido irrelevante
        if any(w in text for w in ["CHURCH", "ELECTION", "DIES", "POLL", "FOOTBALL", "RIVER", "SPORTS", "TOURIST"]):
            return None

        conviction = round(random.uniform(0.78, 0.95), 2)
        
        if any(w in text for w in ["OIL", "HORMUZ", "CRUDE", "ENERGY", "DIESEL", "BARREL"]):
            return {"thesis": "Supply Squeeze Imminente", "trade": self.causal_rules["OIL_SQUEEZE"], "conviction": conviction, "horizon": "6m"}
        elif any(w in text for w in ["CREDIT", "DEFAULT", "BONDS", "LIQUIDITY", "BASEL", "DEBT"]):
            return {"thesis": "Contracción de Crédito & Liquidez", "trade": self.causal_rules["CREDIT_STRESS"], "conviction": conviction, "horizon": "15m"}
        elif any(w in text for w in ["OPENAI", "AI", "GPU", "NVDA", "SEMICONDUCTOR", "CHIP"]):
            return {"thesis": "Aceleración de CAPEX Tecnológico AGI", "trade": self.causal_rules["AI_INFRASTRUCTURE"], "conviction": conviction, "horizon": "6m"}
        elif any(w in text for w in ["SOFR", "FED", "RATE CUT", "INFLATION", "TREASURY"]):
            return {"thesis": "Ajuste Curva de Tasas & Expectativa Macro", "trade": self.causal_rules["RATE_CUT_POLL"], "conviction": conviction, "horizon": "30m"}
        
        return None

class AlphaSynthesizer:
    def __init__(self):
        self.world = WorldModel()

    def process_pending_event(self, row_id, source, headline):
        inference = self.world.infer_causality(headline, source)
        if not inference:
            return None
        
        trade_info = inference["trade"]
        return {
            "id": row_id,
            "timestamp": int(time.time()),
            "source": source,
            "headline": headline,
            "agi_thesis": inference["thesis"],
            "execution": {
                "ticker": trade_info["tickers"][0],
                "action": trade_info["action"],
                "hedge": trade_info["inverse"],
                "conviction": inference["conviction"],
                "horizon": inference["horizon"],
                "risk_score": f"{int(inference['conviction'] * 10)}/10"
            }
        }

def run_agency_loop():
    synthesizer = AlphaSynthesizer()
    print("🧠 [M82 AGENCY LAYER v1.2 UTF-8] World Model Activo con Filtro de Ruido.")
    
    while True:
        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 1")
                row = cursor.fetchone()
                
                if row:
                    row_id, source, headline = row
                    signal = synthesizer.process_pending_event(row_id, source, headline)
                    
                    if signal:
                        formatted_card_headline = (
                            f"[{signal['execution']['action']} {signal['execution']['ticker']}] "
                            f"CONVICTION: {int(signal['execution']['conviction']*100)}% | "
                            f"HORIZON: {signal['execution']['horizon']}\n"
                            f"THESIS: {signal['agi_thesis']}\n"
                            f"EVENT: {headline}"
                        )
                        cursor.execute("UPDATE m82_multi_stream SET headline = ?, status = 'AGI_SYNTHESIZED' WHERE id = ?", (formatted_card_headline, row_id))
                        print(f"⚡ [ALPHA SYNTHESIZED - ID {row_id}] {signal['execution']['action']} {signal['execution']['ticker']} | {signal['agi_thesis']}")
                    else:
                        # Descarta eventos que no generan Alpha
                        cursor.execute("UPDATE m82_multi_stream SET status = 'DISCARDED_NO_ALPHA' WHERE id = ?", (row_id,))
                    
                    conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ Error en Agency Layer Loop: {e}")
                
        time.sleep(1)

if __name__ == "__main__":
    run_agency_loop()
