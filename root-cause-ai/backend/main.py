from pathlib import Path
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from services.analysis_service import analyze_file
from services.storage import save_analysis, get_analysis, list_transactions, get_services

app = FastAPI(title="Root Cause AI", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "root-cause-ai"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".csv",".json",".txt",".log"}:
        raise HTTPException(400, "Unsupported file type. Use CSV, JSON, TXT, or LOG.")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Uploaded file is empty.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(data)
        temp = f.name
    try:
        result = analyze_file(temp)
        save_analysis(result)
        return result
    finally:
        Path(temp).unlink(missing_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return await upload(file)

@app.get("/transactions")
def transactions():
    return {"transactions": list_transactions()}

@app.get("/transaction/{transaction_id}")
def transaction(transaction_id: str):
    result = get_analysis()
    tx = result.get("transactions", {}).get(transaction_id)
    if tx is None:
        raise HTTPException(404, "Transaction not found.")
    return tx

@app.get("/services")
def services():
    return {"services": get_services()}

@app.get("/root-cause/{transaction_id}")
def root_cause(transaction_id: str):
    result = get_analysis()
    tx = result.get("transactions", {}).get(transaction_id)
    if tx is None:
        raise HTTPException(404, "Transaction not found.")
    return tx.get("root_cause", {})
