@echo off
setlocal
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
start "Root Cause AI Backend" cmd /k "call .venv\Scripts\activate && uvicorn backend.main:app --reload"
start "Root Cause AI Dashboard" cmd /k "call .venv\Scripts\activate && streamlit run frontend\app.py"
echo.
echo Dashboard: http://localhost:8501
echo API:       http://127.0.0.1:8000/docs
pause
