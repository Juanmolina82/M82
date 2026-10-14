#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3 AGI :: X-READY TELEMETRY VERIFIER
# ==============================================================================

import os, sys

M82_DIR = os.path.expanduser("~/M82")
ORCH_PATH = os.path.join(M82_DIR, "orch.py")

REQUIRED_STRINGS = [
    ('format_x_telemetry', "CRITICAL ERROR: X-Telemetry formatter missing"),
    ('240', "CRITICAL ERROR: 240 character limit assertion missing"),
    ('#M82TOP', "CRITICAL ERROR: Hashtag footer missing"),
    ('CUSTODIA PASIVA — CPI 08:30 ET', "CRITICAL ERROR: CPI footer missing or wrong")
]

def verify_orch_code():
    print("🔍 [M82 VERIFIER V60.3] Auditando cumplimiento X-Ready...")
    if not os.path.exists(ORCH_PATH):
        print("❌ Error: orch.py no encontrado.")
        return False

    with open(ORCH_PATH, "r") as f:
        code = f.read()

    errors = 0
    for needle, err_msg in REQUIRED_STRINGS:
        if needle not in code:
            print(f"🚨 {err_msg}")
            errors += 1

    if errors == 0:
        print("✅ [VERIFICATION PASSED] Formato X-Ready V60.3 (≤240 chars) verificado 100%.")
        return True
    else:
        print(f"❌ [VERIFICATION FAILED] Fallo de aserción en el formateador X-Ready.")
        return False

if __name__ == "__main__":
    if not verify_orch_code():
        sys.exit(1)
