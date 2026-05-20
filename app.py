"""
Weighted Priority Scheduler (WPS) — Streamlit
Baguio City Emergency Operations Center
Matches the original React/Vite layout: light theme, collapsible sidebar, 6-page nav
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import io

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="WPS · Baguio City EOC",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS  — light theme matching original React app
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp { background: #f8fafc; color: #0f172a; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
}

/* Sidebar toggle arrow — always visible on dark bg */
[data-testid="collapsedControl"] {
    color: #94a3b8 !important;
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 6px !important;
}
[data-testid="collapsedControl"]:hover {
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
}
button[data-testid="baseButton-header"] {
    color: #94a3b8 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 900 !important;
    color: #0f172a !important;
}
[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
}

/* ── Headings ── */
h1, h2, h3, h4 { color: #0f172a !important; }

/* ── Buttons ── */
.stButton > button {
    background: #ffffff; color: #374151;
    border: 1px solid #e2e8f0; border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 13px; font-weight: 600;
    padding: 8px 16px;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.stButton > button:hover {
    background: #f8fafc; border-color: #94a3b8;
}
.stButton > button[kind="primary"] {
    background: #0f172a !important; color: #fff !important;
    border-color: #0f172a !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1e293b !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
}
input[type="number"], [data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
}
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
}
label { color: #64748b !important; font-size: 12px !important; font-weight: 500 !important; }

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #e2e8f0;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #94a3b8;
    font-size: 13px; font-weight: 600;
    letter-spacing: 0.2px; padding: 10px 20px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #0f172a !important;
    border-bottom-color: #0f172a !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
}
[data-testid="stFileUploadDropzone"] {
    background: #f8fafc !important;
    border: 1px dashed #cbd5e1 !important;
    border-radius: 12px !important;
}

/* ── Custom cards ── */
.hero-card {
    background: #0f172a; color: #fff;
    border-radius: 20px; padding: 28px 32px;
    position: relative; overflow: hidden;
    margin-bottom: 8px;
}
.hero-card h3 { color: #fff !important; font-size: 1.4rem; font-weight: 800; margin-bottom: 8px; }
.hero-card p  { color: #94a3b8; font-size: 13px; line-height: 1.6; max-width: 520px; }
.hero-badge {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 12px; padding: 12px 20px; text-align: center;
}
.hero-badge .label { font-size: 9px; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px; }
.hero-badge .value { font-size: 1.1rem; font-weight: 800; color: #fff; margin-top: 2px; }

.stat-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 16px; padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    height: 100%;
}
.stat-card .label {
    font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px;
    color: #94a3b8; font-weight: 700; margin-bottom: 6px;
}
.stat-card .name {
    font-size: 1rem; font-weight: 700; color: #0f172a;
    margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.stat-card .sub { font-size: 11px; color: #94a3b8; margin-bottom: 12px; }
.stat-card .nums { display: flex; gap: 16px; }
.stat-card .nums .n-label { font-size: 9px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }
.stat-card .nums .n-val { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #374151; font-weight: 500; }

.queue-row {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 14px 18px;
    display: flex; align-items: center; justify-content: space-between;
    transition: border-color 0.15s ease; margin-bottom: 6px;
    cursor: pointer;
}
.queue-row:hover { border-color: #94a3b8; }

.badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;
}
.badge-highest  { background: #fef2f2; color: #dc2626; }
.badge-urgent   { background: #fff7ed; color: #ea580c; }
.badge-moderate { background: #eff6ff; color: #3b82f6; }
.badge-low      { background: #f8fafc; color: #94a3b8; }

.action-card {
    background: #fff7ed; border: 1px solid #fed7aa;
    border-radius: 14px; padding: 18px 20px;
}
.action-card h5 { color: #9a3412 !important; font-size: 13px; font-weight: 700; margin-bottom: 6px; }
.action-card p  { color: #c2410c; font-size: 12px; line-height: 1.5; margin: 0; }

.ops-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 18px 20px;
}
.ops-row { display: flex; justify-content: space-between; align-items: center;
    font-size: 13px; padding: 4px 0; }
.ops-row .ops-label { color: #94a3b8; }
.ops-row .ops-val   { font-weight: 700; color: #0f172a; }

.progress-bar-bg { background: #e2e8f0; border-radius: 999px; height: 6px; margin-top: 8px; overflow: hidden; }
.progress-bar-fill { background: #0f172a; height: 100%; border-radius: 999px; transition: width 0.4s ease; }

.section-label {
    font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px;
    color: #94a3b8; font-weight: 700; margin-bottom: 10px;
}

.info-banner {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 10px; padding: 10px 16px;
    font-size: 12px; color: #1d4ed8; margin-bottom: 14px;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# REAL DATASET
# ─────────────────────────────────────────────────────────────

REAL_CSV = """Disaster,Barangay,Affected Families,Casualties,Damaged Houses
SW Monsoon (2025),Irisan,1,0,0
SW Monsoon (2025),Outlook Drive,1,0,0
Continuous Rain (2025),Loakan Liwanag,1,0,0
Continuous Rain (2025),Loakan Proper,2,0,0
ST Uwan (2025),Atok Trail,3,0,3
ST Uwan (2025),Bakakeng Central,10,0,3
ST Uwan (2025),Bakakeng Norte/Sur,1,0,1
ST Uwan (2025),BGH Compound,15,0,0
ST Uwan (2025),Brookspoint,5,0,0
ST Uwan (2025),Cabinet Hill - Teachers Camp,9,0,1
ST Uwan (2025),Camp 7,9,0,3
ST Uwan (2025),City Camp Central,2,0,0
ST Uwan (2025),Country Club Village,2,0,0
ST Uwan (2025),Cresencia Village,1,0,1
ST Uwan (2025),Dominican-Mirador,20,0,0
ST Uwan (2025),Dontogan,3,0,3
ST Uwan (2025),East Modern Site,1,0,1
ST Uwan (2025),Fairview,4,0,1
ST Uwan (2025),Gabriela Silang,1,0,0
ST Uwan (2025),Guisad Surong,19,0,0
ST Uwan (2025),Happy Hollow,4,0,1
ST Uwan (2025),Happy Homes-Old Lucban,8,0,0
ST Uwan (2025),Honeymoon-Holyghost,2,0,0
ST Uwan (2025),Irisan,36,0,17
ST Uwan (2025),Kias,9,0,1
ST Uwan (2025),Loakan Proper,9,0,2
ST Uwan (2025),Lourdes Subdivision Ext,37,0,0
ST Uwan (2025),Lower Quirino Hill,1,0,1
ST Uwan (2025),Lower Rock Quarry,9,0,0
ST Uwan (2025),Lualhati,1,0,1
ST Uwan (2025),Magsaysay Private Road,10,0,0
ST Uwan (2025),Middle Quirino Hill,1,0,1
ST Uwan (2025),Outlook Drive,9,0,2
ST Uwan (2025),Pacdal,3,0,0
ST Uwan (2025),Padre Zamora,1,0,1
ST Uwan (2025),Pinget,2,0,2
ST Uwan (2025),Pinsao Proper,6,0,0
ST Uwan (2025),Quezon Hill Proper,1,0,1
ST Uwan (2025),Saint Joseph Village,1,0,1
ST Uwan (2025),San Luis Village,10,0,0
ST Uwan (2025),South Drive,2,0,2
ST Uwan (2025),Sto. Rosario Valley,42,0,0
ST Uwan (2025),Upper Quezon Hill,3,0,1
STS Crising (2025),Bakakeng Central,2,0,0
STS Crising (2025),Camp 7,11,0,3
STS Crising (2025),Dominican-Mirador,3,0,1
STS Crising (2025),Honeymoon-Holyghost,3,0,1
STS Crising (2025),Irisan,8,0,2
STS Crising (2025),Loakan Apugan,5,0,2
STS Crising (2025),Loakan Proper,1,0,0
STS Crising (2025),Pinsao Pilot Project,4,0,0
STS Crising (2025),Pinsao Proper,1,0,1
STS Crising (2025),Sto. Nino SlaughterHouse,3,0,0
STS Crising (2025),Upper Market,11,0,0
STS Crising (2025),Upper Quezon Hill,3,0,1
TS Dante + SW Monsoon (2025),Alfonso Tabora,2,0,0
TS Dante + SW Monsoon (2025),Ambiong,3,0,0
TS Dante + SW Monsoon (2025),Asin Road,3,0,3
TS Dante + SW Monsoon (2025),Atok Trail,4,0,3
TS Dante + SW Monsoon (2025),Bakakeng Central,9,0,5
TS Dante + SW Monsoon (2025),Bakakeng Norte/Sur,7,0,4
TS Dante + SW Monsoon (2025),BGH Compound,5,0,1
TS Dante + SW Monsoon (2025),Camp 7,28,0,2
TS Dante + SW Monsoon (2025),City Camp Central,33,0,0
TS Dante + SW Monsoon (2025),Dominican-Mirador,29,0,1
TS Dante + SW Monsoon (2025),Green Water Village,5,0,5
TS Dante + SW Monsoon (2025),Guisad Central,25,0,0
TS Dante + SW Monsoon (2025),Irisan,96,0,8
TS Dante + SW Monsoon (2025),Loakan Proper,5,0,2
TS Dante + SW Monsoon (2025),Lourdes Subdivision Ext,49,0,0
TS Dante + SW Monsoon (2025),Outlook Drive,25,0,15
TS Dante + SW Monsoon (2025),Pinsao Pilot Project,5,0,5
TS Dante + SW Monsoon (2025),Pinsao Proper,6,0,3
TS Dante + SW Monsoon (2025),Saint Joseph Village,15,0,2
TS Dante + SW Monsoon (2025),San Luis Village,17,0,15
TS Dante + SW Monsoon (2025),Sto. Rosario Valley,12,0,3
TS Dante + SW Monsoon (2025),Sto. Tomas Proper,18,0,5
TS Paolo (2025),Irisan,3,0,1
TS Paolo (2025),Loakan Liwanag,1,0,1
TS Paolo (2025),Asin Road,1,0,1
Typhoon Bising (2025),Irisan,3,0,3
Typhoon Bising (2025),Pinsao Proper,1,0,1
ST Leon (2024),Happy Hollow,1,0,1
ST Leon (2024),Dominican-Mirador,2,0,2
STS Kristine (2024),Asin Road,2,0,0
STS Kristine (2024),Gibraltar,1,0,0
STS Kristine (2024),Guisad Central,1,0,0
STS Kristine (2024),Irisan,2,0,0
STS Kristine (2024),Kias,1,0,1
STS Kristine (2024),Loakan Proper,2,0,0
STS Kristine (2024),Mines View,1,0,0
STS Kristine (2024),Outlook Drive,5,0,1
STS Kristine (2024),Pinsao Proper,1,0,1
STS Kristine (2024),San Luis Village,1,0,0
TC Julian (2024),Aurora Hill Proper,1,0,1
TC Julian (2024),Asin Road,2,0,2
TC Julian (2024),Bakakeng Central,1,0,0
TC Julian (2024),Balsigan,2,0,2
TC Julian (2024),Cabinet Hill - Teachers Camp,2,0,0
TC Julian (2024),Campo Filipino,5,0,0
TC Julian (2024),Cresencia Village,4,0,0
TC Julian (2024),Dominican-Mirador,5,0,3
TC Julian (2024),Guisad Central,7,0,0
TC Julian (2024),Irisan,18,0,0
TC Julian (2024),Loakan Apugan,2,0,0
TC Julian (2024),Lower Magsaysay,4,0,0
TC Julian (2024),Mines View,3,0,0
TC Julian (2024),San Luis Village,7,0,2
TC Julian (2024),South Drive,4,0,0
TY Carina (2024),Atok Trail,3,0,1
TY Carina (2024),Bakakeng Central,4,0,2
TY Carina (2024),Bakakeng Norte/Sur,3,0,3
TY Carina (2024),BGH Compound,4,0,0
TY Carina (2024),Campo Filipino,7,0,0
TY Carina (2024),Cresencia Village,3,0,0
TY Carina (2024),Dontogan,5,0,2
TY Carina (2024),Fairview,4,0,2
TY Carina (2024),Gibraltar,11,0,0
TY Carina (2024),Guisad Central,6,0,0
TY Carina (2024),Happy Hollow,5,0,0
TY Carina (2024),Irisan,35,0,1
TY Carina (2024),Kias,7,0,0
TY Carina (2024),Loakan Apugan,2,0,0
TY Carina (2024),Loakan Proper,5,0,1
TY Carina (2024),Lower Magsaysay,7,0,0
TY Carina (2024),Lucnab,4,0,0
TY Carina (2024),Pacdal,4,0,3
TY Carina (2024),Padre Burgos,6,0,0
TY Carina (2024),Pinsao Pilot Project,3,0,1
TY Carina (2024),Pinsao Proper,8,0,5
TY Carina (2024),San Luis Village,4,0,0
TY Carina (2024),Sto. Nino SlaughterHouse,4,0,0
TY Carina (2024),Sto. Tomas Proper,5,0,0
TY Enteng (2024),Asin Road,2,0,2
TY Enteng (2024),Dontogan,1,0,1
TY Enteng (2024),Loakan Proper,1,0,1
TY Enteng (2024),Quezon Hill Proper,1,0,0
TY Nika (2024),Dominican-Mirador,2,0,0
TY Nika (2024),Guisad Surong,1,0,1
Typhoon Pepito (2024),Asin Road,3,0,2
Typhoon Pepito (2024),Atok Trail,2,0,1
Typhoon Pepito (2024),Bakakeng Central,2,0,2
Typhoon Pepito (2024),City Camp Central,19,0,0
Typhoon Pepito (2024),Dominican-Mirador,1,0,0
Typhoon Pepito (2024),Guisad Surong,14,0,0
Typhoon Pepito (2024),Irisan,8,0,0
Typhoon Pepito (2024),Kias,3,0,0
Typhoon Pepito (2024),Loakan Proper,2,0,2
Typhoon Pepito (2024),Lourdes Subdivision Ext,21,0,0
Typhoon Pepito (2024),Outlook Drive,5,0,2
Typhoon Pepito (2024),Pinsao Proper,1,0,0
Typhoon Pepito (2024),San Luis Village,5,0,1
Typhoon Pepito (2024),Sto. Tomas Proper,2,0,0
Typhoon Pepito (2024),Upper Quezon Hill,2,0,0
Typhoon Pepito (2024),Victoria Village,3,0,2
Typhoon Hanna (2023),Upper Quezon Hill,2,0,0
Typhoon Hanna (2023),Sto. Tomas Proper,1,0,0
Typhoon Hanna (2023),Fairview,3,0,0
TC Florita (2022),Bakakeng Central,6,0,0
TC Florita (2022),Cabinet Hill - Teachers Camp,1,0,1
TC Florita (2022),Camp 7,5,0,2
TC Florita (2022),Fairview,3,0,0
TC Florita (2022),Hillside,1,0,0
TC Florita (2022),Irisan,3,0,2
TC Florita (2022),Kias,2,0,1
TC Florita (2022),Lower Magsaysay,1,0,0
TC Florita (2022),San Luis Village,5,0,2
TC Florita (2022),Sto. Nino SlaughterHouse,1,0,1
TS Paeng,Atok Trail,1,0,1
TS Paeng,Bakakeng Central,2,0,0
TS Paeng,BGH Compound,2,0,1
TS Paeng,Cabinet Hill - Teachers Camp,2,0,1
TS Paeng,Camp 7,1,0,1
TS Paeng,Dontogan,3,0,3
TS Paeng,DPS Compound,1,0,1
TS Paeng,Gibraltar,1,0,0
TS Paeng,Happy Hollow,4,0,2
TS Paeng,Honeymoon-Holyghost,2,0,0
TS Paeng,Irisan,21,0,18
TS Paeng,Loakan Proper,1,0,1
TS Paeng,Lucnab,1,0,1
TS Paeng,Middle Quirino Hill,3,0,3
TS Paeng,Outlook Drive,1,0,1
TS Paeng,Pinsao Pilot Project,1,0,1
TS Paeng,San Vicente,1,0,1
TS Paeng,Sto. Nino SlaughterHouse,2,0,2
TS Paeng,Upper Quezon Hill,1,0,0
"""

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def normalize_mm(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - lo) / (hi - lo)


def run_wsm(df: pd.DataFrame):
    results, perf = [], []
    t_start = time.perf_counter()
    for d_name, grp in df.groupby("Disaster"):
        grp = grp.copy()
        t0  = time.perf_counter()
        grp["norm_fam"] = normalize_mm(grp["Affected Families"])
        grp["norm_cas"] = normalize_mm(grp["Casualties"])
        grp["norm_hse"] = normalize_mm(grp["Damaged Houses"])
        grp["score"]    = (grp["norm_fam"] + grp["norm_cas"] + grp["norm_hse"]) / 3
        grp["score_pct"]= (grp["score"] * 100).round(2)
        grp = grp.sort_values(["score","Casualties"], ascending=False)
        grp["rank"] = range(1, len(grp) + 1)
        perf.append({"Disaster": d_name, "Records": len(grp),
                     "Time (ms)": round((time.perf_counter() - t0) * 1000, 6)})
        results.append(grp)
    total_ms = (time.perf_counter() - t_start) * 1000
    return pd.concat(results, ignore_index=True), pd.DataFrame(perf), total_ms


def urgency(score: float):
    if score >= 0.7: return "Highest",  "badge-highest",  "#dc2626"
    if score >= 0.4: return "Urgent",   "badge-urgent",   "#ea580c"
    if score >= 0.1: return "Moderate", "badge-moderate", "#3b82f6"
    return              "Low",      "badge-low",      "#94a3b8"


def recommendation(score: float) -> str:
    if score >= 0.7: return "Immediate response (within 24 hours)"
    if score >= 0.4: return "Urgent (24–48 hours)"
    if score >= 0.1: return "Scheduled (2–3 days)"
    return "Monitoring / delayed response"


def jaccard(a: set, b: set) -> float:
    u = a | b
    return len(a & b) / len(u) if u else 0.0


PBASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font_color="#64748b", font_family="Inter",
    title_font_color="#0f172a", title_font_size=14,
    xaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0", linecolor="#e2e8f0"),
    yaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0", linecolor="#e2e8f0"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#e2e8f0"),
    margin=dict(l=20, r=20, t=50, b=20),
)
BLUES = [[0.0,"#eff6ff"],[0.33,"#93c5fd"],[0.66,"#3b82f6"],[1.0,"#1d4ed8"]]

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "added_entries" not in st.session_state:
    st.session_state.added_entries = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────

def load_base() -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(REAL_CSV))
    for col in ["Affected Families", "Casualties", "Damaged Houses"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["Disaster"] = df["Disaster"].astype(str).str.strip()
    df["Barangay"] = df["Barangay"].astype(str).str.strip()
    return df


def get_df() -> pd.DataFrame:
    base = load_base()
    if st.session_state.added_entries:
        added = pd.DataFrame(st.session_state.added_entries)
        return pd.concat([base, added], ignore_index=True)
    return base

# ─────────────────────────────────────────────────────────────
# SIDEBAR  — dark, matches original React sidebar exactly
# ─────────────────────────────────────────────────────────────

NAV_ITEMS = [
    ("Dashboard",           "dashboard"),
    ("Assessment Input",    "assessment"),
    ("Priority Queue",      "queue"),
    ("Analytics",           "analytics"),
    ("Algorithm Assessment","evaluation"),
    ("How WPS Works",       "how-it-works"),
]

with st.sidebar:
    # Logo block
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:8px 4px 20px 4px;
                border-bottom:1px solid #1e293b;margin-bottom:16px">
        <div style="width:40px;height:40px;background:#2563eb;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;
                    font-weight:900;color:#fff;font-size:18px;flex-shrink:0">W</div>
        <div>
            <div style="font-size:15px;font-weight:800;color:#fff;line-height:1">WPS</div>
            <div style="font-size:9px;color:#475569;text-transform:uppercase;
                        letter-spacing:2px;margin-top:2px">Baguio City Ops</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nav buttons
    for label, key in NAV_ITEMS:
        active = st.session_state.page == label
        bg     = "#2563eb" if active else "transparent"
        fg     = "#ffffff" if active else "#94a3b8"
        border = "none"
        st.markdown(
            f"""<div style="margin-bottom:2px">
            <button onclick="window.location.href=''" id="nav_{key}"
                style="width:100%;text-align:left;padding:10px 14px;border-radius:9px;
                       background:{bg};color:{fg};border:{border};cursor:pointer;
                       font-size:13px;font-weight:{'600' if active else '500'};
                       font-family:Inter,sans-serif;transition:all 0.15s">
                {label}
            </button></div>""",
            unsafe_allow_html=True,
        )
        if st.button(label, key=f"nav_{key}_btn",
                     use_container_width=True,
                     help=f"Go to {label}"):
            st.session_state.page = label
            st.rerun()

    st.markdown("<div style='margin-top:auto'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0">
        <div style="width:32px;height:32px;border-radius:50%;background:#1e293b;
                    border:2px solid #334155;flex-shrink:0;display:flex;
                    align-items:center;justify-content:center;
                    font-size:11px;font-weight:700;color:#64748b">BC</div>
        <div>
            <div style="font-size:12px;font-weight:700;color:#fff">Baguio City EOC</div>
            <div style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:1px">Ops Terminal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER BAR
# ─────────────────────────────────────────────────────────────

page = st.session_state.page
page_subtitle = "Weighted Sum Model (WSM) Priority Scheduling for 128 Barangays"
now = pd.Timestamp.now()

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.markdown(f"## {page}")
    st.markdown(f'<p class="section-label">{page_subtitle}</p>', unsafe_allow_html=True)
with hcol2:
    st.markdown(
        f'<div style="text-align:right;padding-top:8px">'
        f'<div style="font-size:9px;font-weight:700;color:#94a3b8;text-transform:uppercase;'
        f'letter-spacing:1.5px">Current Time</div>'
        f'<div style="font-size:13px;font-weight:700;color:#0f172a">'
        f'{now.strftime("%b %d, %Y")} | {now.strftime("%H:%M")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# BUILD WORKING DATA
# ─────────────────────────────────────────────────────────────

df       = get_df()
df_final, perf_df, total_ms = run_wsm(df)

# ═════════════════════════════════════════════════════════════
#  DASHBOARD
# ═════════════════════════════════════════════════════════════

if page == "Dashboard":

    # Hero card
    top_row = df_final.iloc[0]
    urg_lbl, urg_cls, urg_col = urgency(top_row["score"])
    st.markdown(f"""
    <div class="hero-card">
        <div style="position:relative;z-index:1">
            <h3>Emergency Response Dashboard</h3>
            <p>Real-time disaster prioritization for 128 barangays of Baguio City.
            Rankings are computed using the Weighted Sum Model based on reported casualties,
            affected families, and damaged structures.</p>
        </div>
        <div style="display:flex;gap:12px;margin-top:20px;position:relative;z-index:1">
            <div class="hero-badge">
                <div class="label">Status</div>
                <div class="value" style="color:#ef4444">OPERATIONAL</div>
            </div>
            <div class="hero-badge">
                <div class="label">Last Update</div>
                <div class="value">{now.strftime('%H:%M')}</div>
            </div>
        </div>
        <div style="position:absolute;right:-60px;bottom:-60px;width:300px;height:300px;
                    background:rgba(239,68,68,0.08);border-radius:50%;filter:blur(60px)"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Metric strip
    c1, c2, c3, c4 = st.columns(4)
    total_assessed = df_final["Barangay"].nunique()
    c1.metric("Top Priority",        df_final.iloc[0]["Barangay"])
    c2.metric("Total Affected",      f"{df['Affected Families'].sum():,}")
    c3.metric("Total Casualties",    f"{df['Casualties'].sum():,}")
    c4.metric("Queue Density",       f"{len(df_final)} records")

    st.markdown("")

    left_col, right_col = st.columns([2, 1])

    # Top 5 list
    with left_col:
        st.markdown("**Critical Priority Areas (Top 5)**")
        top5 = df_final.head(5)
        for _, row in top5.iterrows():
            ul, ucls, ucol = urgency(row["score"])
            st.markdown(f"""
            <div class="queue-row" style="cursor:default">
                <div style="display:flex;align-items:center;gap:14px">
                    <div style="width:38px;height:38px;border-radius:10px;background:#f8fafc;
                                display:flex;align-items:center;justify-content:center;
                                font-weight:800;font-size:13px;color:#64748b;flex-shrink:0">
                        #{int(row['rank'])}
                    </div>
                    <div>
                        <div style="font-weight:700;font-size:14px;color:#0f172a">{row['Barangay']}</div>
                        <div style="font-size:11px;color:#94a3b8;margin-top:2px">
                            {row['Disaster']} &nbsp;·&nbsp;
                            {row['Affected Families']} families &nbsp;·&nbsp;
                            {row['Casualties']} casualties
                        </div>
                    </div>
                </div>
                <div style="text-align:right">
                    <span class="badge {ucls}">{ul}</span>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:1.2rem;
                                font-weight:700;color:#0f172a;margin-top:4px">
                        {row['score_pct']:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("View full queue", key="goto_queue"):
            st.session_state.page = "Priority Queue"
            st.rerun()

    with right_col:
        total_brgy    = df["Barangay"].nunique()
        assessed_n    = len(df_final[df_final["score"] > 0])
        remaining     = max(0, 128 - total_brgy)
        pct           = min(total_brgy / 128, 1.0)

        st.markdown(f"""
        <div class="ops-card" style="margin-bottom:12px">
            <div style="font-weight:700;font-size:14px;color:#0f172a;margin-bottom:14px">Operational Status</div>
            <div class="ops-row"><span class="ops-label">Total Barangays</span><span class="ops-val">128</span></div>
            <div class="ops-row"><span class="ops-label">In Dataset</span><span class="ops-val" style="color:#2563eb">{total_brgy}</span></div>
            <div class="ops-row"><span class="ops-label">Disaster Events</span><span class="ops-val">{df_final['Disaster'].nunique()}</span></div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{pct*100:.1f}%"></div>
            </div>
        </div>
        <div class="action-card">
            <h5>Quick Action Required</h5>
            <p>Check the top-ranked barangays in the Priority Queue.
            Recommendations are automatically updated as new data is entered.</p>
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  ASSESSMENT INPUT
# ═════════════════════════════════════════════════════════════

elif page == "Assessment Input":

    st.markdown(
        '<div class="info-banner">Admin / LGU — add new barangay assessment data. '
        'Entries are merged with the official dataset and rankings update immediately.</div>',
        unsafe_allow_html=True,
    )

    base_df     = load_base()
    known_brgy  = sorted(base_df["Barangay"].unique().tolist())
    known_dis   = sorted(base_df["Disaster"].unique().tolist())

    tab_manual, tab_batch = st.tabs(["Manual Entry", "Batch CSV Upload"])

    # ── Manual Entry ─────────────────────────────────────────
    with tab_manual:
        st.markdown("")

        col_d, col_b = st.columns(2)
        with col_d:
            d_choice = st.selectbox(
                "Disaster Event",
                ["— select existing —"] + known_dis + ["+ Add new event"],
                key="d_select",
            )
            if d_choice == "+ Add new event":
                d_val = st.text_input("New disaster name", placeholder="e.g. TY Marce (2025)", key="d_new")
            elif d_choice == "— select existing —":
                d_val = ""
            else:
                d_val = d_choice

        with col_b:
            b_choice = st.selectbox(
                "Barangay",
                ["— select existing —"] + known_brgy + ["+ Add new barangay"],
                key="b_select",
            )
            if b_choice == "+ Add new barangay":
                b_val = st.text_input("New barangay name", key="b_new")
            elif b_choice == "— select existing —":
                b_val = ""
            else:
                b_val = b_choice

        st.markdown("")
        n1, n2, n3 = st.columns(3)
        with n1:
            fam = st.number_input("Affected Families", min_value=0, value=0, step=1, key="n_fam")
        with n2:
            cas = st.number_input("Casualties",        min_value=0, value=0, step=1, key="n_cas")
        with n3:
            hse = st.number_input("Damaged Houses",    min_value=0, value=0, step=1, key="n_hse")

        st.markdown("")
        if st.button("Add Assessment Entry", type="primary", key="add_entry"):
            d_clean = d_val.strip()
            b_clean = b_val.strip()
            if not d_clean or not b_clean:
                st.error("Both Disaster Event and Barangay are required.")
            else:
                st.session_state.added_entries.append({
                    "Disaster":          d_clean,
                    "Barangay":          b_clean,
                    "Affected Families": int(fam),
                    "Casualties":        int(cas),
                    "Damaged Houses":    int(hse),
                })
                st.success(f"Entry added — {b_clean} / {d_clean}. Rankings updated.")
                st.rerun()

    # ── Batch CSV ────────────────────────────────────────────
    with tab_batch:
        st.markdown("")
        tmpl = pd.DataFrame([{
            "Disaster": "TY Marce (2025)", "Barangay": "Irisan",
            "Affected Families": 10, "Casualties": 2, "Damaged Houses": 5,
        }])
        st.download_button(
            "Download CSV template",
            data=tmpl.to_csv(index=False).encode(),
            file_name="assessment_template.csv", mime="text/csv",
        )
        batch_file = st.file_uploader(
            "Upload assessment CSV", type=["csv"],
            key="batch_upload", label_visibility="collapsed",
        )
        if batch_file:
            try:
                bdf = pd.read_csv(batch_file)
                # Normalise headers
                remap = {}
                for c in bdf.columns:
                    cl = c.strip().lower()
                    if cl in ("baranagy","barangay","name"): remap[c] = "Barangay"
                    elif cl == "disaster":                   remap[c] = "Disaster"
                bdf.rename(columns=remap, inplace=True)
                for col in ["Affected Families","Casualties","Damaged Houses"]:
                    if col in bdf.columns:
                        bdf[col] = pd.to_numeric(bdf[col], errors="coerce").fillna(0).astype(int)
                st.dataframe(bdf, use_container_width=True)
                if st.button("Import All Rows", type="primary", key="import_batch"):
                    for _, row in bdf.iterrows():
                        st.session_state.added_entries.append({
                            "Disaster":          str(row.get("Disaster","")).strip(),
                            "Barangay":          str(row.get("Barangay","")).strip(),
                            "Affected Families": int(row.get("Affected Families", 0)),
                            "Casualties":        int(row.get("Casualties", 0)),
                            "Damaged Houses":    int(row.get("Damaged Houses", 0)),
                        })
                    st.success(f"Imported {len(bdf)} entries.")
                    st.rerun()
            except Exception as e:
                st.error(f"Could not read file: {e}")

    # ── Pending entries list ──────────────────────────────────
    if st.session_state.added_entries:
        st.markdown("---")
        st.markdown(
            f"**Pending entries** &nbsp;"
            f"<span style='color:#94a3b8;font-size:13px;font-weight:400'>"
            f"{len(st.session_state.added_entries)} record(s) added this session</span>",
            unsafe_allow_html=True,
        )
        for i, e in enumerate(st.session_state.added_entries):
            c1, c2, c3, c4, c5, c6 = st.columns([3, 2, 1, 1, 1, 1])
            c1.markdown(f"**{e['Barangay']}**")
            c2.markdown(f"<span style='color:#94a3b8;font-size:12px'>{e['Disaster']}</span>", unsafe_allow_html=True)
            c3.markdown(f"<span style='font-size:11px;color:#64748b'>Fam: {e['Affected Families']}</span>", unsafe_allow_html=True)
            c4.markdown(f"<span style='font-size:11px;color:#64748b'>Cas: {e['Casualties']}</span>", unsafe_allow_html=True)
            c5.markdown(f"<span style='font-size:11px;color:#64748b'>Hse: {e['Damaged Houses']}</span>", unsafe_allow_html=True)
            if c6.button("Remove", key=f"rm_{i}"):
                st.session_state.added_entries.pop(i)
                st.rerun()

        bc1, bc2 = st.columns([1, 5])
        with bc1:
            if st.button("Clear All", key="clear_all"):
                st.session_state.added_entries = []
                st.rerun()
        with bc2:
            pend = pd.DataFrame(st.session_state.added_entries)
            st.download_button(
                "Download pending entries",
                data=pend.to_csv(index=False).encode(),
                file_name="pending_entries.csv", mime="text/csv",
            )

# ═════════════════════════════════════════════════════════════
#  PRIORITY QUEUE
# ═════════════════════════════════════════════════════════════

elif page == "Priority Queue":

    col_head, col_dl = st.columns([4, 1])
    with col_head:
        st.markdown("**Disaster Response Priority Queue**")
        st.markdown('<p class="section-label">Live ranked list of barangays waiting for emergency resources</p>', unsafe_allow_html=True)
    with col_dl:
        st.markdown("<br>", unsafe_allow_html=True)
        all_export = df_final[["rank","Barangay","Disaster","score_pct",
                                "Affected Families","Casualties","Damaged Houses"]].copy()
        all_export.columns = ["Rank","Barangay","Disaster","Score (%)","Affected Families","Casualties","Damaged Houses"]
        st.download_button("Export List", data=all_export.to_csv(index=False).encode(),
                           file_name="priority_queue.csv", mime="text/csv")

    # Filters
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1:
        search_q = st.text_input("", placeholder="Find barangay in queue...", key="q_search", label_visibility="collapsed")
    with fc2:
        dis_filter = st.selectbox("Disaster", ["All"] + list(df_final["Disaster"].unique()), key="q_dis", label_visibility="collapsed")
    with fc3:
        urg_filter = st.selectbox("Urgency", ["All","Highest","Urgent","Moderate","Low"], key="q_urg", label_visibility="collapsed")

    # Active count metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active in Queue",    len(df_final))
    m2.metric("Disaster Events",    df_final["Disaster"].nunique())
    m3.metric("Total Casualties",   f"{df_final['Casualties'].sum():,}")
    m4.metric("Total Affected Fam", f"{df_final['Affected Families'].sum():,}")

    st.markdown("")

    # Apply filters
    view = df_final.copy()
    if search_q:
        view = view[view["Barangay"].str.lower().str.contains(search_q.lower())]
    if dis_filter != "All":
        view = view[view["Disaster"] == dis_filter]
    if urg_filter != "All":
        view = view[view["score"].apply(lambda s: urgency(s)[0]) == urg_filter]

    if view.empty:
        st.info("No records match the current filter.")
    else:
        for _, row in view.iterrows():
            ul, ucls, ucol = urgency(row["score"])
            rec = recommendation(row["score"])
            with st.expander(
                f"#{int(row['rank'])}  {row['Barangay']}  —  {row['Disaster']}  |  Score: {row['score_pct']:.1f}%  ·  {ul}",
                expanded=False,
            ):
                d1, d2, d3, d4 = st.columns(4)
                d1.metric("Affected Families", row["Affected Families"])
                d2.metric("Casualties",        row["Casualties"])
                d3.metric("Damaged Houses",    row["Damaged Houses"])
                d4.metric("Priority Score",    f"{row['score_pct']:.2f}%")
                st.markdown(
                    f"Normalized — Families: `{row['norm_fam']:.3f}` &nbsp;·&nbsp;"
                    f"Casualties: `{row['norm_cas']:.3f}` &nbsp;·&nbsp;"
                    f"Houses: `{row['norm_hse']:.3f}`  \n"
                    f"**Recommendation:** {rec}",
                )

# ═════════════════════════════════════════════════════════════
#  ANALYTICS
# ═════════════════════════════════════════════════════════════

elif page == "Analytics":

    sel_dis = st.selectbox("Select Disaster Event", df_final["Disaster"].unique(), key="an_dis")
    sub     = df_final[df_final["Disaster"] == sel_dis].copy()
    sub["Urgency"] = sub["score"].apply(lambda s: urgency(s)[0])
    top10   = sub.nsmallest(10, "rank")

    # Row 1 – horizontal bar
    fig1 = px.bar(
        top10.sort_values("score_pct"), x="score_pct", y="Barangay", orientation="h",
        title="Priority Score — Top 10 Barangays",
        color="score_pct", color_continuous_scale=BLUES,
        labels={"score_pct":"Score (%)","Barangay":""},
    )
    fig1.update_layout(**PBASE); fig1.update_coloraxes(showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

    # Row 2 – pie + casualties bar
    r1, r2 = st.columns(2)
    with r1:
        fig2 = px.pie(top10, names="Barangay", values="Affected Families",
                      title="Affected Families Distribution",
                      color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.45)
        fig2.update_layout(**PBASE)
        st.plotly_chart(fig2, use_container_width=True)
    with r2:
        fig3 = px.bar(top10, x="Barangay", y="Casualties",
                      title="Casualties per Barangay",
                      color="Casualties", color_continuous_scale=BLUES, labels={"Barangay":""})
        fig3.update_layout(**PBASE, xaxis_tickangle=-35); fig3.update_coloraxes(showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    # Row 3 – stacked normalized breakdown
    melt = top10.melt(id_vars="Barangay",
                      value_vars=["norm_fam","norm_cas","norm_hse"],
                      var_name="Criterion", value_name="Normalized Score")
    melt["Criterion"] = melt["Criterion"].map(
        {"norm_fam":"Affected Families","norm_cas":"Casualties","norm_hse":"Damaged Houses"})
    fig4 = px.bar(melt, x="Barangay", y="Normalized Score", color="Criterion",
                  title="Normalized Score Breakdown", barmode="stack",
                  color_discrete_sequence=["#3b82f6","#22c55e","#f59e0b"],
                  labels={"Barangay":""})
    fig4.update_layout(**PBASE, xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)

    # Row 4 – scatter
    fig5 = px.scatter(sub, x="Casualties", y="score_pct",
                      size="Affected Families", color="Urgency",
                      hover_name="Barangay",
                      color_discrete_map={"Highest":"#dc2626","Urgent":"#ea580c",
                                          "Moderate":"#3b82f6","Low":"#94a3b8"},
                      title="Priority Score vs Casualties (bubble = affected families)",
                      labels={"score_pct":"Score (%)"})
    fig5.update_layout(**PBASE)
    st.plotly_chart(fig5, use_container_width=True)

# ═════════════════════════════════════════════════════════════
#  ALGORITHM ASSESSMENT (Evaluation)
# ═════════════════════════════════════════════════════════════

elif page == "Algorithm Assessment":

    tab_j, tab_p = st.tabs(["Jaccard Index", "Computational Efficiency"])

    with tab_j:
        st.markdown('<p class="section-label">Top-k agreement between WPS and single-criterion baselines</p>', unsafe_allow_html=True)

        K_VALS    = [3, 5]
        BASELINES = {"Families only":"Affected Families",
                     "Casualties only":"Casualties",
                     "Houses only":"Damaged Houses"}
        b_results = {}
        for bl, bc in BASELINES.items():
            grps = []
            for dn, g in df.groupby("Disaster"):
                g2 = g.copy().sort_values(bc, ascending=False)
                g2["rank"] = range(1, len(g2)+1)
                grps.append(g2)
            b_results[bl] = pd.concat(grps, ignore_index=True)

        recs = []
        for k in K_VALS:
            for dn in df_final["Disaster"].unique():
                ds = df_final[df_final["Disaster"]==dn]
                if len(ds) < k: continue
                wtop = set(ds.nsmallest(k,"rank")["Barangay"])
                for bl, bdf2 in b_results.items():
                    btop = set(bdf2[bdf2["Disaster"]==dn].nsmallest(k,"rank")["Barangay"])
                    recs.append({"Disaster":dn,"k":k,"Baseline":bl,
                                 "Jaccard":round(jaccard(wtop,btop),4)})
        jdf = pd.DataFrame(recs)
        st.dataframe(jdf, use_container_width=True)

        figj = px.bar(jdf, x="Baseline", y="Jaccard", color="k", barmode="group",
                      title="Top-k Agreement with Baselines",
                      color_discrete_sequence=["#3b82f6","#22c55e"],
                      labels={"Jaccard":"Jaccard Index"})
        figj.update_layout(**PBASE)
        st.plotly_chart(figj, use_container_width=True)

    with tab_p:
        st.markdown('<p class="section-label">WSM processing time per disaster group</p>', unsafe_allow_html=True)
        pdf = perf_df.copy()
        pdf["ms / record"] = (pdf["Time (ms)"] / pdf["Records"]).round(6)
        st.dataframe(pdf, use_container_width=True)
        figp = px.bar(pdf, x="Disaster", y="ms / record",
                      title="Processing Time per Record (ms)",
                      color="ms / record", color_continuous_scale=BLUES)
        figp.update_layout(**PBASE, xaxis_tickangle=-30); figp.update_coloraxes(showscale=False)
        st.plotly_chart(figp, use_container_width=True)
        p1, p2 = st.columns(2)
        p1.metric("Total processing time", f"{total_ms:.4f} ms")
        p2.metric("Records processed",     len(df_final))

# ═════════════════════════════════════════════════════════════
#  HOW WPS WORKS
# ═════════════════════════════════════════════════════════════

elif page == "How WPS Works":

    ca, cb = st.columns(2)
    with ca:
        st.markdown("""
**Weighted Sum Model (WSM)**

Each barangay receives a priority score from three equally weighted criteria:

```
Score = (Norm_Families + Norm_Casualties + Norm_Houses) / 3
```

Barangays are ranked descending within each disaster group.
Ties are resolved by raw casualty count.
        """)
    with cb:
        st.markdown("""
**Min-Max Normalization**

Raw values are scaled to [0, 1] so criteria with different units stay comparable:

```
Norm(x) = (x − min) / (max − min)
```

When all values in a group are equal, 0.5 is assigned (neutral score).
        """)

    st.markdown("---")
    st.markdown("**Urgency Thresholds**")
    st.dataframe(
        pd.DataFrame([
            {"Score Range":"≥ 70%","Level":"Highest","Response":"Immediate (within 24 hours)"},
            {"Score Range":"40–69%","Level":"Urgent","Response":"24–48 hours"},
            {"Score Range":"10–39%","Level":"Moderate","Response":"2–3 days"},
            {"Score Range":"< 10%","Level":"Low","Response":"Monitoring"},
        ]),
        use_container_width=True, hide_index=True,
    )

    st.markdown("---")
    st.markdown("""
**CSV Column Requirements**

| Column | Type | Notes |
|---|---|---|
| `Disaster` | string | Event name, e.g. "TY Carina (2024)" |
| `Barangay` | string | Barangay name ("Baranagy" typo also accepted) |
| `Affected Families` | integer | Displaced or affected family count |
| `Casualties` | integer | Casualty count |
| `Damaged Houses` | integer | Structurally damaged house count |

Each disaster group is normalized independently. New entries can be added via **Assessment Input**.
    """)

    st.markdown("---")
    base_export = load_base()
    st.download_button(
        "Download official dataset (CSV)",
        data=base_export.to_csv(index=False).encode(),
        file_name="baguio_disaster_dataset.csv", mime="text/csv",
    )
