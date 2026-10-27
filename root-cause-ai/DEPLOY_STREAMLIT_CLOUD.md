# Root Cause AI — Streamlit Cloud Deployment

## What this version changes

This package has a root-level `app.py` so Streamlit Community Cloud can launch the dashboard directly. The RCA backend modules remain inside `backend/` and the sample datasets remain inside `sample_data/`.

You do **not** need to run `run.bat` for the cloud deployment.

## 1. Put the project on GitHub

Create a GitHub repository and upload the **contents** of this folder (not the ZIP file).

Recommended repository name:

`root-cause-ai`

## 2. Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app**.
3. Select your repository.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **Deploy**.

Streamlit Cloud will install the dependencies from `requirements.txt` automatically.

## 3. Your final link

After deployment, Streamlit will give you a URL similar to:

`https://root-cause-ai-<your-name>.streamlit.app`

Use that URL for your HOD/judge demo.

## 4. Important

- Do not upload the ZIP itself to the Streamlit deployment.
- Upload the extracted project files to GitHub.
- Keep `backend/`, `sample_data/`, `app.py`, and `requirements.txt` in the repository.
- The current dashboard uses the Ice Silver / Deep Aubergine / Marigold visual theme.
- Uploaded files are processed in the running app. Do not rely on cloud-local files as permanent storage.
