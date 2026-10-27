from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rule_anomaly"] = False
    out["anomaly_reasons"] = ""

    def add(mask, reason):
        out.loc[mask, "rule_anomaly"] = True
        out.loc[mask, "anomaly_reasons"] = out.loc[mask, "anomaly_reasons"].apply(
            lambda x: (x + "; " if x else "") + reason
        )

    add(out["log_level"].str.upper().isin(["ERROR","CRITICAL"]), "error-level log")
    add(out["status_code"].fillna(0) >= 500, "HTTP 5xx")
    add(out["response_time"].fillna(0) > 2000, "high response time")

    out["ml_anomaly"] = False
    numeric = out["response_time"].fillna(0).astype(float)
    valid = numeric.notna() & (numeric > 0)
    if valid.sum() >= 10 and numeric[valid].nunique() >= 3:
        try:
            model = IsolationForest(contamination="auto", random_state=42)
            pred = model.fit_predict(numeric[valid].to_numpy().reshape(-1,1))
            out.loc[valid, "ml_anomaly"] = pred == -1
        except Exception:
            pass

    out["is_anomaly"] = out["rule_anomaly"] | out["ml_anomaly"]
    return out

def service_baseline(df):
    return (df.groupby("service")["response_time"]
              .agg(["count","mean","median","max"])
              .fillna(0).reset_index())
