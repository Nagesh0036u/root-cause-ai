from pathlib import Path
import json
STORE = Path(__file__).resolve().parents[1] / "data_store.json"

def save_analysis(result):
    STORE.write_text(json.dumps(result, indent=2), encoding="utf-8")

def get_analysis():
    if not STORE.exists(): return {}
    return json.loads(STORE.read_text(encoding="utf-8"))

def list_transactions():
    return list(get_analysis().get("transactions", {}).keys())

def get_services():
    return get_analysis().get("service_health", [])
