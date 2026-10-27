from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any
import pandas as pd

ALIASES = {
    "timestamp": ["timestamp","time","datetime","date","ts"],
    "service": ["service","servicename","service_name","component","application","app"],
    "request_id": ["request_id","requestid","req_id"],
    "transaction_id": ["transaction_id","transactionid","txn_id","txn","transaction"],
    "trace_id": ["trace_id","traceid","trace"],
    "correlation_id": ["correlation_id","correlationid","corr_id","correlation"],
    "status_code": ["status_code","status","http_status","http_status_code","response_code"],
    "response_time": ["response_time","response_ms","latency","latency_ms","duration","duration_ms"],
    "log_level": ["log_level","level","severity"],
    "message": ["message","msg","log","text","event"],
    "endpoint": ["endpoint","path","url","route"],
}

def _norm(s: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).strip().lower())

def detect_fields(columns):
    normalized = {_norm(c): c for c in columns}
    mapping = {}
    for target, aliases in ALIASES.items():
        for alias in aliases:
            if _norm(alias) in normalized:
                mapping[target] = normalized[_norm(alias)]
                break
    return mapping

def _parse_pipe_line(line: str):
    parts = [x.strip() for x in line.split("|")]
    if len(parts) < 5:
        return None
    # timestamp | service | transaction_id | level | message
    return {"timestamp": parts[0], "service": parts[1], "transaction_id": parts[2],
            "log_level": parts[3], "message": "|".join(parts[4:]).strip()}

def read_logs(path: str) -> tuple[pd.DataFrame, dict]:
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(p)
    elif ext == ".json":
        obj = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(obj, dict) and "logs" in obj: obj = obj["logs"]
        df = pd.DataFrame(obj if isinstance(obj, list) else [obj])
    else:
        rows = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            row = _parse_pipe_line(line)
            if row: rows.append(row)
        if not rows:
            raise ValueError("Could not parse the text/log file. Expected pipe-delimited records.")
        df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("The uploaded file contains no records.")

    mapping = detect_fields(df.columns)
    rename = {v:k for k,v in mapping.items()}
    df = df.rename(columns=rename)

    for col in ["timestamp","service","transaction_id","request_id","trace_id","correlation_id",
                "status_code","response_time","log_level","message","endpoint"]:
        if col not in df.columns:
            df[col] = None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["service"] = df["service"].fillna("Unknown Service").astype(str).str.strip()
    for col in ["transaction_id","request_id","trace_id","correlation_id","log_level","message","endpoint"]:
        df[col] = df[col].fillna("").astype(str)
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce")
    df["response_time"] = pd.to_numeric(df["response_time"], errors="coerce")
    df = df.sort_values("timestamp", na_position="last").reset_index(drop=True)
    return df, {"format": ext.lstrip("."), "field_mapping": mapping, "rows": len(df)}
