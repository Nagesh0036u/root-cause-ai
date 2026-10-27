import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))
from services.analysis_service import analyze_file

st.set_page_config(
    page_title="Root Cause AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Root Cause AI — charcoal / forest green / crimson visual system
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --charcoal: #171717;
    --aubergine: #24132F;
    --aubergine-deep: #160C1E;
    --aubergine-soft: #2D193A;
    --silver: #E8EDF2;
    --silver-soft: #B8C2CC;
    --silver-muted: #87929D;
    --marigold: #F2B705;
    --marigold-soft: #FFD45A;
    --line: #3A2A46;
    --panel: #1D1126;
}

.stApp {
    background:
        radial-gradient(circle at 88% 0%, rgba(242,183,5,.10), transparent 25%),
        radial-gradient(circle at 5% 12%, rgba(89,43,116,.18), transparent 28%),
        var(--charcoal);
    color: var(--silver);
}

[data-testid="stHeader"] { background: rgba(23,23,23,.88); }
[data-testid="stToolbar"] { visibility: hidden; }

.block-container {
    max-width: 1450px;
    padding: 2.2rem 3rem 3.5rem;
}

h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
    color: var(--silver);
}
h1 { letter-spacing: -1.5px; font-weight: 800; }
h2, h3 { letter-spacing: -.4px; }

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #24132F 0%, #1A0F23 58%, #171717 100%);
    border: 1px solid #4A3158;
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 18px 55px rgba(0,0,0,.34);
}
.hero:after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -60px;
    top: -75px;
    border-radius: 50%;
    border: 1px solid rgba(242,183,5,.35);
    box-shadow: 0 0 0 24px rgba(242,183,5,.035), 0 0 0 48px rgba(242,183,5,.018);
}
.hero-kicker {
    color: var(--marigold) !important;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}
.hero-title {
    color: #F4F7FA !important;
    font-size: 2.15rem;
    font-weight: 850;
    margin: 0;
}
.hero-sub {
    color: var(--silver-soft) !important;
    margin: 7px 0 0;
    font-size: .98rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-top: 17px;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(242,183,5,.09);
    border: 1px solid rgba(242,183,5,.30);
    color: var(--marigold-soft) !important;
    font-size: .78rem;
    font-weight: 700;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--marigold);
    box-shadow: 0 0 10px rgba(242,183,5,.75);
}

.section-head {
    display:flex;
    align-items:end;
    justify-content:space-between;
    gap:20px;
    margin: 28px 0 12px;
}
.section-kicker {
    color: var(--marigold) !important;
    font-size:.70rem;
    font-weight:800;
    letter-spacing:1.6px;
    text-transform:uppercase;
}
.section-title {
    color: var(--silver) !important;
    margin: 2px 0 0;
    font-size: 1.28rem;
    font-weight: 800;
}

.metric {
    background: linear-gradient(145deg, #24132F, #1A0F23);
    border: 1px solid #473153;
    border-radius: 16px;
    padding: 17px 18px;
    min-height: 104px;
    box-shadow: 0 10px 30px rgba(0,0,0,.20);
    transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
.metric:hover {
    transform: translateY(-2px);
    border-color: rgba(242,183,5,.55);
    box-shadow: 0 12px 32px rgba(242,183,5,.08);
}
.metric-label {
    color: var(--silver-muted) !important;
    font-size:.72rem;
    text-transform:uppercase;
    letter-spacing:1.15px;
    font-weight:800;
}
.metric-value {
    color: #F4F7FA !important;
    font-size:1.75rem;
    line-height:1.2;
    font-weight:850;
    margin-top:8px;
}
.metric-accent { color: var(--marigold) !important; }

.panel {
    background: linear-gradient(145deg, #24132F, #1A0F23);
    border:1px solid #473153;
    border-radius:18px;
    padding:20px;
    box-shadow:0 12px 34px rgba(0,0,0,.22);
    margin-bottom:14px;
}
.panel-red {
    border-color: rgba(242,183,5,.55);
    background: linear-gradient(145deg, #2A1736, #1A0F23);
}
.panel-title { color: var(--silver) !important; font-weight:800; font-size:1rem; margin-bottom:4px; }
.panel-muted { color: var(--silver-muted) !important; font-size:.84rem; }

.rca-box {
    background: linear-gradient(135deg, #2B1638, #1B1024 55%, #24132F);
    border:1px solid rgba(242,183,5,.72);
    border-radius:20px;
    padding:22px;
    box-shadow: 0 12px 38px rgba(242,183,5,.08);
}
.rca-label {
    color: var(--marigold) !important;
    font-size:.70rem;
    letter-spacing:1.5px;
    font-weight:850;
    text-transform:uppercase;
}
.rca-service {
    color:#FFF2BE !important;
    font-size:1.48rem;
    font-weight:900;
    margin-top:5px;
}
.score {
    display:inline-flex;
    align-items:center;
    gap:7px;
    margin-top:13px;
    padding:6px 10px;
    background:rgba(242,183,5,.13);
    border:1px solid rgba(242,183,5,.42);
    border-radius:999px;
    color:#FFE18A !important;
    font-size:.78rem;
    font-weight:800;
}

.evidence {
    background:#1B1024;
    border:1px solid #473153;
    border-radius:20px;
    padding:22px;
}
.evidence-item {
    padding:10px 0;
    border-bottom:1px solid #34233F;
    color:#DDE4EA !important;
    font-size:.9rem;
}
.evidence-item:last-child { border-bottom:0; }
.check {
    display:inline-flex;
    width:22px; height:22px;
    align-items:center; justify-content:center;
    margin-right:8px;
    border-radius:50%;
    background:rgba(242,183,5,.13);
    color:var(--marigold) !important;
    font-weight:900;
}

.flow {
    display:flex;
    align-items:center;
    flex-wrap:wrap;
    gap:8px;
    margin-top:10px;
}
.flow-node {
    background:#2A1736;
    border:1px solid #4D355A;
    border-radius:11px;
    padding:9px 12px;
    color:#E7ECF0 !important;
    font-size:.80rem;
    font-weight:750;
}
.flow-arrow { color:var(--marigold) !important; font-weight:900; }

.upload-panel {
    border:1px dashed #6A4A78;
    background:rgba(36,19,47,.62);
    border-radius:18px;
    padding:8px;
}
.stFileUploader label { color:#E5EBF0 !important; }
[data-testid="stFileUploaderDropzone"] {
    background:#1B1024 !important;
    border-color:#5B3D69 !important;
    border-radius:14px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { color:#AEB8C1 !important; }

div[data-baseweb="select"] > div {
    background:#1B1024 !important;
    border-color:#5B3D69 !important;
    color:#E8EDF2 !important;
}
div[data-baseweb="select"] span { color:#E8EDF2 !important; }

.stButton button {
    background:var(--marigold) !important;
    color:#171717 !important;
    border:0 !important;
    border-radius:10px !important;
    font-weight:850 !important;
}
.stButton button:hover {
    background:#FFD04A !important;
    box-shadow:0 0 22px rgba(242,183,5,.20);
}

[data-testid="stDataFrame"] {
    border:1px solid #473153;
    border-radius:14px;
    overflow:hidden;
}

hr { border-color:#3B2A46 !important; }

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#24132F 0%,#1B1024 65%,#171717 100%);
    border-right:1px solid #473153;
}
[data-testid="stSidebar"] * { color:#E4EAF0; }

.footer {
    text-align:center;
    color:#68737D !important;
    font-size:.72rem;
    padding:30px 0 5px;
    letter-spacing:.4px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Microservice Observability • Explainable AI</div>
    <div class="hero-title">◈ Root Cause AI</div>
    <div class="hero-sub">Find where a failure started — not just where the errors appeared.</div>
    <div class="hero-badge"><span class="dot"></span> Analysis engine ready</div>
</div>
""", unsafe_allow_html=True)

# Input area
st.markdown("""
<div class="section-head">
  <div>
    <div class="section-kicker">01 / Ingest</div>
    <div class="section-title">Bring in your application logs</div>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.55, 1], gap="large")
with c1:
    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload logs",
        type=["csv", "json", "txt", "log"],
        help="Supported formats: CSV, JSON, TXT and LOG"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    sample_dir = ROOT / "sample_data"
    samples = sorted(sample_dir.glob("*_logs.csv"))
    sample_choice = st.selectbox(
        "Or choose a bundled sample dataset",
        ["—"] + [p.name for p in samples]
    )

result = None
if uploaded:
    suffix = Path(uploaded.name).suffix
    tmp = ROOT / "data" / "uploaded" / ("upload" + suffix)
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_bytes(uploaded.getvalue())
    try:
        with st.spinner("Reading logs and tracing transactions..."):
            result = analyze_file(str(tmp))
    except Exception as e:
        st.error(f"Could not analyze the file: {e}")
elif sample_choice != "—":
    try:
        with st.spinner("Reading logs and tracing transactions..."):
            result = analyze_file(str(sample_dir / sample_choice))
    except Exception as e:
        st.error(f"Could not analyze the sample: {e}")

if result:
    s = result["summary"]

    st.markdown("""
    <div class="section-head">
      <div>
        <div class="section-kicker">02 / System Pulse</div>
        <div class="section-title">What is happening across the system?</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    labels = [
        ("Total Logs", s["total_logs"], ""),
        ("Transactions", s["total_transactions"], ""),
        ("Successful", s["successful_transactions"], "metric-accent"),
        ("Failed", s["failed_transactions"], ""),
        ("Anomalies", s["anomalies_detected"], ""),
        ("RCA Incidents", s["root_cause_incidents"], ""),
    ]
    cols = st.columns(6, gap="medium")
    for c, (label, val, cls) in zip(cols, labels):
        c.markdown(
            f'<div class="metric"><div class="metric-label">{label}</div>'
            f'<div class="metric-value {cls}">{val}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="section-head">
      <div>
        <div class="section-kicker">03 / Service Health</div>
        <div class="section-title">Which services are under pressure?</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    health = pd.DataFrame(result["service_health"])
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Service health snapshot</div><div class="panel-muted">Errors observed per service</div>', unsafe_allow_html=True)
        st.dataframe(health, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Error concentration</div><div class="panel-muted">Higher bars indicate more observed errors</div>', unsafe_allow_html=True)
        if not health.empty:
            chart = health.set_index("service")["errors"]
            st.bar_chart(chart, height=275)
        else:
            st.info("No service health data available.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
      <div>
        <div class="section-kicker">04 / Investigation</div>
        <div class="section-title">Follow one transaction to the source</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tx_ids = list(result["transactions"].keys())
    if tx_ids:
        tid = st.selectbox("Select transaction", tx_ids)
        tx = result["transactions"][tid]
        rc = tx["root_cause"]

        left, right = st.columns([1, 1.35], gap="large")

        with left:
            if rc["service"]:
                st.markdown(f"""
                <div class="rca-box">
                    <div class="rca-label">Most likely root cause</div>
                    <div class="rca-service">◉ {rc["service"]}</div>
                    <div class="score">Root Cause Score&nbsp; {rc["score"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(rc["message"])

        with right:
            evidence_html = ""
            for item in rc["evidence"]:
                evidence_html += f'<div class="evidence-item"><span class="check">✓</span>{item}</div>'
            st.markdown(
                '<div class="evidence"><div class="panel-title">Why the system chose it</div>'
                '<div class="panel-muted">Evidence behind the ranking</div>'
                + evidence_html + '</div>',
                unsafe_allow_html=True
            )

        st.markdown("""
        <div class="section-head">
          <div>
            <div class="section-kicker">05 / Request Path</div>
            <div class="section-title">How the transaction moved through the system</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        flow = ""
        for i, service in enumerate(tx["services"]):
            if i:
                flow += '<span class="flow-arrow">→</span>'
            flow += f'<span class="flow-node">{service}</span>'
        st.markdown(f'<div class="panel"><div class="flow">{flow}</div></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="section-head">
          <div>
            <div class="section-kicker">06 / Timeline</div>
            <div class="section-title">What happened, in order?</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        timeline = pd.DataFrame(tx["timeline"])
        if not timeline.empty:
            st.dataframe(timeline, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="section-head">
          <div>
            <div class="section-kicker">07 / Anomalies</div>
            <div class="section-title">Events that look unusual</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        anomalies = pd.DataFrame(tx["anomalies"])
        if not anomalies.empty:
            st.dataframe(anomalies, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="panel"><span class="panel-muted">No anomalies were detected for this transaction.</span></div>', unsafe_allow_html=True)
    else:
        st.info("No transactions were found in the analysis result.")
else:
    st.markdown("""
    <div class="panel" style="margin-top:24px;text-align:center;padding:38px;">
        <div style="font-size:2rem;">◈</div>
        <div class="panel-title" style="font-size:1.15rem;margin-top:8px;">Ready to investigate</div>
        <div class="panel-muted">Upload a log file or choose a bundled sample dataset to begin tracing failures.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="footer">ROOT CAUSE AI • Explainable microservice failure investigation</div>',
    unsafe_allow_html=True
)
