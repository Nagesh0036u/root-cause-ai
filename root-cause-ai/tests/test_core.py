import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from services.log_parser import read_logs, detect_fields
from services.anomaly_detector import detect_anomalies
from services.root_cause_engine import score_transaction
from services.analysis_service import analyze_file

def test_field_detection():
    m=detect_fields(["Time","Service_Name","Txn_ID","Level","Latency_ms"])
    assert m["timestamp"]=="Time"
    assert m["service"]=="Service_Name"
    assert m["transaction_id"]=="Txn_ID"

def test_payment_sample_root_cause():
    r=analyze_file(str(Path(__file__).resolve().parents[1]/"sample_data/payment_failure_logs.csv"))
    assert r["transactions"]
    root_services={v["root_cause"]["service"] for v in r["transactions"].values() if v["root_cause"]["service"]}
    assert "Payment_Service" in root_services

def test_anomaly_rules():
    r=analyze_file(str(Path(__file__).resolve().parents[1]/"sample_data/high_latency_logs.csv"))
    assert r["summary"]["anomalies_detected"] > 0

def test_database_sample():
    r=analyze_file(str(Path(__file__).resolve().parents[1]/"sample_data/database_failure_logs.csv"))
    assert any(v["root_cause"]["service"]=="Database_Service" for v in r["transactions"].values())
