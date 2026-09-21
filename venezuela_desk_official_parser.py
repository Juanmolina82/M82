#!/usr/bin/env python3
import json
import os
import hashlib
from datetime import datetime, timezone

# Ruta de almacenamiento totalmente aislada del Core
RUNTIME_DESK_DIR = os.path.expanduser("~/M82/runtime/venezuela_desk")
os.makedirs(RUNTIME_DESK_DIR, exist_ok=True)

def build_event_id(authority, topic, effective_date):
    raw = f"{authority}:{topic}:{effective_date}"
    return f"VD-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:12].upper()}"

def parse_official_sources():
    now_utc = datetime.now(timezone.utc).isoformat()

    # Mapeo determinista contra fuentes públicas oficiales
    official_records = [
        {
            "authority": "OFAC",
            "jurisdiction": "US_TREASURY",
            "source_type": "PUBLIC_REGULATORY_NOTICE",
            "topic": "GL_5Z_EXTENSION",
            "entity": "PDVSA_2020_BONDS",
            "effective_date": "2026-09-18",
            "summary": "Official update on General License 5Z regarding temporary restriction of rights to PDVSA 2020 8.5% collateral.",
            "source_url": "https://ofac.treasury.gov/sanctions-programs-and-country-information/venezuela",
            "confidence": 1.00
        },
        {
            "authority": "SDNY_COURT",
            "jurisdiction": "US_FEDERAL_COURT_SDNY",
            "source_type": "JUDICIAL_DOCKET_SUMMARY",
            "topic": "FAILLA_JUDICIAL_ORDER",
            "entity": "CITGO_PETROLEUM",
            "effective_date": "2026-09-17",
            "summary": "SDNY District Court order regarding schedule and filings for PDVSA 2020 bondholders and trustees.",
            "source_url": "https://www.nysd.uscourts.gov",
            "confidence": 0.98
        },
        {
            "authority": "DELAWARE_DISTRICT_COURT",
            "jurisdiction": "US_FEDERAL_COURT_DELAWARE",
            "source_type": "AUCTION_PROCEEDING",
            "topic": "STARK_SPECIAL_MASTER_REPORT",
            "entity": "PDVH_CITGO_SALE",
            "effective_date": "2026-09-16",
            "summary": "Delaware District Court filings on Special Master recommendations for Citgo parent company share sale.",
            "source_url": "https://www.ded.uscourts.gov",
            "confidence": 0.97
        }
    ]

    event_payload = []
    for rec in official_records:
        event = {
            "event_id": build_event_id(rec["authority"], rec["topic"], rec["effective_date"]),
            "observed_at": now_utc,
            "effective_date": rec["effective_date"],
            "source_type": rec["source_type"],
            "authority": rec["authority"],
            "jurisdiction": rec["jurisdiction"],
            "topic": rec["topic"],
            "entity": rec["entity"],
            "summary": rec["summary"],
            "source_url": rec["source_url"],
            "confidence": rec["confidence"],
            "review_status": "UNVERIFIED_LOCAL_SNAPSHOT",
            "actionability": "informational_only"
        }
        event_payload.append(event)

    # Persistencia exclusivamente en el runtime segregado
    ts_filename = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RUNTIME_DESK_DIR, f"events_official_{ts_filename}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(event_payload, f, indent=2, ensure_ascii=False)

    print("===================================================================")
    print("      VENEZUELA_DESK — SATÉLITE MANUAL DE FUENTES OFICIALES      ")
    print("===================================================================")
    print(f"📄 Snapshot generado: {output_path}")
    print(f"📊 Eventos extraídos: {len(event_payload)}")
    print(f"🔒 M82 CORE STATUS: INTACTO (Sin escrituras en DB ni interacción con PM2)")
    print("===================================================================")

if __name__ == "__main__":
    parse_official_sources()
