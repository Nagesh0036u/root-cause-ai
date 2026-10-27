from __future__ import annotations
import pandas as pd
from .log_parser import read_logs
from .anomaly_detector import detect_anomalies, service_baseline
from .root_cause_engine import score_transaction

def analyze_file(path: str):
    df, meta = read_logs(path)
    df = detect_anomalies(df)

    tx_col = df["transaction_id"].replace("", pd.NA)
    if tx_col.isna().all():
        # fall back to request/trace/correlation, then deterministic synthetic grouping
        for col in ["request_id","trace_id","correlation_id"]:
            if df[col].replace("", pd.NA).notna().any():
                df["transaction_id"] = df[col]
                break
    if df["transaction_id"].replace("", pd.NA).isna().all():
        df["transaction_id"] = [f"TXN_AUTO_{i+1:04d}" for i in range(len(df))]

    transactions = {}
    for tid, tx in df.groupby("transaction_id", dropna=False):
        tid = str(tid)
        tx = tx.sort_values("timestamp")
        rc = score_transaction(tx, df)
        transactions[tid] = {
            "transaction_id": tid,
            "services": tx["service"].drop_duplicates().tolist(),
            "logs": _records(tx),
            "anomalies": _records(tx[tx["is_anomaly"]]),
            "root_cause": rc,
            "timeline": _records(tx[["timestamp","service","log_level","message","status_code","response_time"]])
        }

    baseline = service_baseline(df)
    errors = df[df["is_anomaly"]]
    service_health = []
    for service, s in df.groupby("service"):
        avg = float(s["response_time"].mean()) if s["response_time"].notna().any() else 0
        err = int((s["log_level"].str.upper().isin(["ERROR","CRITICAL"]) | (s["status_code"].fillna(0)>=500)).sum())
        status = "Critical" if err >= 10 or avg > 3000 else ("Warning" if err > 0 or avg > 1000 else "Healthy")
        service_health.append({"service":service,"status":status,"errors":err,"avg_response_ms":round(avg,2)})

    failed_tx = sum(1 for v in transactions.values() if v["root_cause"]["service"])
    return {
        "meta": meta,
        "summary": {
            "total_logs": int(len(df)),
            "total_transactions": int(len(transactions)),
            "successful_transactions": int(len(transactions)-failed_tx),
            "failed_transactions": int(failed_tx),
            "anomalies_detected": int(df["is_anomaly"].sum()),
            "root_cause_incidents": int(failed_tx)
        },
        "service_health": service_health,
        "baseline": _records(baseline),
        "transactions": transactions,
        "error_distribution": [{"service":s,"errors":int((g["log_level"].str.upper().isin(["ERROR","CRITICAL"]) | (g["status_code"].fillna(0)>=500)).sum())} for s,g in df.groupby("service")]
    }

def _records(df):
    if df is None or len(df)==0: return []
    out = df.copy()
    for c in out.columns:
        out[c] = out[c].apply(lambda x: x.isoformat() if hasattr(x, "isoformat") else (None if pd.isna(x) else x))
    return out.to_dict(orient="records")
