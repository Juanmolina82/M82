import lseg.data as ld
import json, time, sys, os
from pathlib import Path

# Importar el dispatcher activo en M82
sys.path.append(str(Path.home() / "M82"))
from feed_dispatcher import process_incoming_news

def parse_and_dispatch_story(news_item):
    """
    Normaliza el payload heterogéneo de LSEG (MRN/News) a formato M82
    """
    try:
        headline = news_item.get("headline", "Sin Titular")
        story_id = news_item.get("storyId", "")
        topic_codes = news_item.get("topicCodes", [])
        ric = news_item.get("ric", "MACRO")
        
        # Clasificación heurística según topic_codes y RIC de LSEG
        asset_type = "EQUITY"
        impact = 5
        action = "MONITOR"

        if "US30YT=RR" in ric or "US10YT=RR" in ric or "US Treasury" in headline:
            asset_type = "BOND"
            impact = 8
            action = "REVIEW_YIELD_CURVE_SPREAD"
        elif "VEN" in headline or "PDVSA" in headline or "Venezuela" in headline:
            asset_type = "BOND"
            impact = 9
            action = "CHECK_SOVEREIGN_BID_STABILITY"
        elif "CLc1" in ric or "WTI" in headline or "Crude" in headline:
            asset_type = "COMMODITY"
            impact = 7
            action = "EVALUATE_CITGO_EV_COLLATERAL"
        elif "AAPL" in ric or "Apple" in headline:
            asset_type = "EQUITY"
            impact = 7
            action = "HEDGE_SPX_SENTIMENT"
        elif "AMZN" in ric or "Amazon" in headline:
            asset_type = "EQUITY"
            impact = 7
            action = "CHECK_AMZN_50DMA_SUPPORT"
        elif "ETF" in headline or "SPY" in ric:
            asset_type = "ETF"
            impact = 6
            action = "TRACK_MARKET_BREADTH"

        payload = {
            "asset_type": asset_type,
            "ticker": ric if ric != "MACRO" else "GLOBAL-MACRO",
            "headline": headline,
            "impact": impact,
            "action": action
        }

        # Despachar al motor central en tiempo real
        process_incoming_news(payload)

    except Exception as e:
        print(f"[BRIDGE ERROR] Fallo al procesar noticia: {e}")

def start_lseg_stream():
    """
    Abre la sesión con LSEG Workspace y suscribe el callback en tiempo real
    """
    try:
        # Cargar clave desde vault.json si aplica
        vault_path = Path.home() / "M82/vault.json"
        if vault_path.exists():
            with open(vault_path) as f:
                vault = json.load(f)
                app_key = vault.get("LSEG_APP_KEY", "DEFAULT_KEY")
                os.environ["LSEG_APP_KEY"] = app_key

        ld.open_session()
        print("[LSEG BRIDGE] Sesión establecida exitosamente con Refinitiv / Workspace.")

        # Suscripción a stream de noticias (Machine Readable News / Real-Time Wire)
        news_stream = ld.content.news.headlines.Definition(
            query="LEN AND (AAPL OR AMZN OR VEN OR WTI OR US30Y OR SPX)",
            count=10
        ).get_stream()

        news_stream.on_update(lambda stream, headline: parse_and_dispatch_story(headline))
        news_stream.open()
        
        print("[LSEG BRIDGE] Streaming en tiempo real activo (Intervalo < 60s)...")
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"[LSEG BRIDGE CRITICAL] Error de conexión: {e}")

if __name__ == "__main__":
    start_lseg_stream()
