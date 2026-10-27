from __future__ import annotations
import pandas as pd

LEVEL_WEIGHT = {"INFO":0, "WARNING":5, "WARN":5, "ERROR":20, "CRITICAL":30}

def score_transaction(tx: pd.DataFrame, all_logs: pd.DataFrame | None = None):
    services = tx["service"].dropna().unique().tolist()
    rows = []
    first_ts = tx["timestamp"].min()
    failed_services = set()
    for _, r in tx.iterrows():
        lvl = str(r.get("log_level","")).upper()
        status = r.get("status_code")
        if lvl in {"ERROR","CRITICAL"} or (pd.notna(status) and float(status) >= 500):
            failed_services.add(r["service"])

    for service in services:
        s = tx[tx["service"] == service].copy()
        score = 0.0
        evidence = []
        first_failure = False
        error_count = int(s["log_level"].str.upper().isin(["ERROR","CRITICAL"]).sum())
        status5 = int((s["status_code"].fillna(0) >= 500).sum())
        latency = s["response_time"].fillna(0)
        high_latency = int((latency > 2000).sum())

        failure_rows = s[(s["log_level"].str.upper().isin(["ERROR","CRITICAL"])) | (s["status_code"].fillna(0) >= 500)]
        if not failure_rows.empty:
            earliest = failure_rows["timestamp"].min()
            global_failures = tx[(tx["log_level"].str.upper().isin(["ERROR","CRITICAL"])) | (tx["status_code"].fillna(0) >= 500)]
            if not global_failures.empty and earliest == global_failures["timestamp"].min():
                score += 40; evidence.append("First critical failure in transaction"); first_failure = True

        if error_count:
            score += min(20, error_count * 8)
            evidence.append(f"{error_count} error-level event(s)")
        if status5:
            score += min(15, status5 * 7)
            evidence.append(f"{status5} HTTP 5xx event(s)")
        if high_latency:
            score += min(15, high_latency * 5)
            evidence.append("Response time above 2000 ms")

        if all_logs is not None:
            same = all_logs[all_logs["service"] == service]
            if len(same):
                failed = same["log_level"].str.upper().isin(["ERROR","CRITICAL"]) | (same["status_code"].fillna(0) >= 500)
                rate = float(failed.mean())
                if rate > 0.2:
                    score += 10
                    evidence.append("Repeated failure pattern across dataset")

        rows.append({"service": service, "score": round(score,1), "evidence": evidence, "first_failure": first_failure})

    ranking = sorted(rows, key=lambda x: x["score"], reverse=True)
    if not ranking or ranking[0]["score"] < 20:
        return {"service": None, "score": 0, "evidence": [], "ranking": ranking,
                "message": "Insufficient evidence for a reliable root cause."}
    return {"service": ranking[0]["service"], "score": ranking[0]["score"],
            "evidence": ranking[0]["evidence"], "ranking": ranking,
            "message": f"{ranking[0]['service']} is the most likely root cause based on the available evidence."}
