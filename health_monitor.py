import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path.home() / "M82"
OUTPUT = BASE_DIR / "runtime" / "health" / "service_status.json"
EXPECTED = ["m82-alerts", "m82-v21"]

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["pm2", "jlist"],
        capture_output=True,
        text=True,
        timeout=30,
        check=True
    )

    processes = json.loads(result.stdout)
    found = {}

    for item in processes:
        env = item.get("pm2_env", {})
        name = item.get("name", "unknown")
        found[name] = {
            "status": env.get("status", "unknown"),
            "pid": item.get("pid"),
            "restarts": env.get("restart_time", 0)
        }

    missing = [name for name in EXPECTED if name not in found]
    unhealthy = [
        name for name in EXPECTED
        if found.get(name, {}).get("status") != "online"
    ]

    report = {
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "service": "m82-health",
        "node": "CARACAS",
        "mode": "INFORMATIONAL_ONLY",
        "expected_services": EXPECTED,
        "processes": found,
        "missing": missing,
        "unhealthy": unhealthy,
        "healthy": not missing and not unhealthy
    }

    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    main()
