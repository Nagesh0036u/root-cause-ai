# Root Cause AI — Complete Project

An academic, explainable root-cause detection system for microservice application logs.

## What is included
- FastAPI backend
- Streamlit dashboard
- CSV / JSON / TXT / LOG parsing
- Automatic field detection and normalization
- Transaction correlation and timeline reconstruction
- Rule-based anomaly detection
- Isolation Forest anomaly detection when enough latency data exists
- Transparent multi-signal root-cause scoring
- Dynamic evidence generation
- Synthetic microservice log generator
- Five bundled scenario datasets
- Automated tests
- Windows `run.bat`

## Quick start — Windows

### Option A
Double-click `run.bat`.

### Option B
Open Command Prompt in this folder:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

In another terminal:

```bat
.venv\Scripts\activate
streamlit run frontend\app.py
```

### URLs
Dashboard: http://localhost:8501  
FastAPI docs: http://127.0.0.1:8000/docs

## Generate logs

```bat
python log_generator\generate_logs.py --count 300 --scenario payment_failure
```

Other scenarios:
`normal`, `database_failure`, `auth_failure`, `high_latency`, `mixed`

## Test

```bat
pytest -q
```

## Sample datasets
- `normal_logs.csv`
- `payment_failure_logs.csv`
- `database_failure_logs.csv`
- `auth_failure_logs.csv`
- `high_latency_logs.csv`

## RCA logic
The score combines signals including first critical failure, error severity, HTTP 5xx events, high response time, and repeated failure patterns. The displayed score is a ranking score, not a statistical confidence percentage.

## API
- `GET /health`
- `POST /upload`
- `POST /analyze`
- `GET /transactions`
- `GET /transaction/{id}`
- `GET /services`
- `GET /root-cause/{id}`
