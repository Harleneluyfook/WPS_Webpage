import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import io
import copy

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Weighted Priority Scheduler",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

.stApp { background: #0d1117; color: #e6edf3; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #090e14 !important;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #8b949e !important; }
[data-testid="stSidebar"] h3 { color: #e6edf3 !important; font-size: 1rem !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 13px; letter-spacing: 0.3px; }

/* Fix the sidebar collapse/expand arrow button visibility */
[data-testid="collapsedControl"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #8b949e !important;
}
[data-testid="collapsedControl"]:hover { border-color: #58a6ff !important; }
section[data-testid="stSidebar"] > div > div > button {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px 24px;
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 500 !important;
    color: #e6edf3 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: #8b949e !important;
}

/* ── Headings ── */
h1 { font-size: 1.4rem !important; font-weight: 600 !important; color: #e6edf3 !important; }
h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: #e6edf3 !important; }
h3 { font-size: 1rem   !important; font-weight: 500 !important; color: #c9d1d9 !important; }
h4 { font-size: 0.9rem !important; font-weight: 500 !important; color: #8b949e !important;
     text-transform: uppercase; letter-spacing: 1px; }

/* ── Buttons ── */
.stButton > button {
    background: #21262d; color: #e6edf3;
    border: 1px solid #30363d; border-radius: 6px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 13px; font-weight: 500;
    transition: all 0.15s ease;
}
.stButton > button:hover { background: #30363d; border-color: #58a6ff; color: #58a6ff; }
.stButton > button[kind="primary"] {
    background: #1f6feb !important; border-color: #388bfd !important; color: #fff !important;
}
.stButton > button[kind="primary"]:hover { background: #388bfd !important; }

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stFileUploader"],
textarea {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
}
input[type="number"] { background: #161b22 !important; color: #e6edf3 !important; }
label { color: #8b949e !important; font-size: 12px !important; }

/* ── Tables / Dataframes ── */
hr { border-color: #21262d !important; }
[data-testid="stDataFrame"] { border: 1px solid #21262d; border-radius: 8px; overflow: hidden; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #21262d; gap: 0; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #8b949e;
    font-size: 13px; font-weight: 500; letter-spacing: 0.3px;
    padding: 8px 20px; border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }

/* ── Alerts ── */
.stAlert { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
[data-testid="stFileUploadDropzone"] { background: #161b22 !important; border: 1px dashed #30363d !important; border-radius: 8px !important; }

/* ── Custom components ── */
.section-label {
    font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px;
    color: #8b949e; margin-bottom: 12px; margin-top: 4px;
}
.stat-card {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 8px; padding: 16px 20px; height: 100%;
}
.info-banner {
    background: #0e2030; border: 1px solid #1a4a7a;
    border-radius: 8px; padding: 10px 16px;
    font-size: 13px; color: #58a6ff; margin-bottom: 16px;
}
.entry-row {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 8px; padding: 14px 18px; margin-bottom: 8px;
}
.urgency-critical { color: #f85149; font-weight: 600; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px; }
.urgency-high     { color: #e3b341; font-weight: 600; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px; }
.urgency-moderate { color: #58a6ff; font-weight: 600; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px; }
.urgency-low      { color: #8b949e; font-weight: 600; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# REAL DATASET  (Baguio City EOC — embedded, no upload needed)
# ─────────────────────────────────────────────────────────────

REAL_CSV = """Disaster,Baranagy,Affected Families,Casualties,Damaged Houses
SW Monsoon (2025),Irisan,1,0,0
SW Monsoon (2025),Outlook Drive,1,0,0
Continuous Rain (2025),Loakan Liwanag,1,0,0
Continuous Rain (2025),Loakan Proper,2,0,0
ST Uwan (2025),Atok trail,3,0,3
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

def normalize_min_max(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - lo) / (hi - lo)


def run_wsm(df: pd.DataFrame):
    """Run WSM algorithm. Accepts df with columns: disaster, barangay,
    Affected Families, Casualties, Damaged Houses."""
    results, perf = [], []
    start = time.perf_counter()
    for d_name, group in df.groupby("disaster"):
        group = group.copy()
        t0 = time.perf_counter()
        group["norm_families"]   = normalize_min_max(group["Affected Families"])
        group["norm_casualties"] = normalize_min_max(group["Casualties"])
        group["norm_damaged"]    = normalize_min_max(group["Damaged Houses"])
        group["priority_score"]  = (
            group["norm_families"] + group["norm_casualties"] + group["norm_damaged"]
        ) / 3
        group["score_pct"] = (group["priority_score"] * 100).round(2)
        group = group.sort_values("priority_score", ascending=False)
        group["rank"] = range(1, len(group) + 1)
        perf.append({
            "Disaster":  d_name,
            "Records":   len(group),
            "Time (ms)": round((time.perf_counter() - t0) * 1000, 6),
        })
        results.append(group)
    total_ms = (time.perf_counter() - start) * 1000
    return pd.concat(results, ignore_index=True), pd.DataFrame(perf), total_ms


def jaccard(a: set, b: set) -> float:
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def urgency_label(score: float) -> str:
    if score >= 70: return "Critical"
    if score >= 40: return "High"
    if score >= 10: return "Moderate"
    return "Low"


def urgency_color(label: str) -> str:
    return {"Critical":"#f85149","High":"#e3b341","Moderate":"#58a6ff","Low":"#8b949e"}.get(label,"#8b949e")


PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font_color="#8b949e", font_family="IBM Plex Sans",
    title_font_color="#e6edf3", title_font_size=14,
    xaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", linecolor="#21262d"),
    yaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", linecolor="#21262d"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262d"),
    margin=dict(l=20, r=20, t=50, b=20),
)
BLUE_SCALE   = [[0.0,"#1a2332"],[0.33,"#1f3a5f"],[0.66,"#1a5fa3"],[1.0,"#58a6ff"]]
REQUIRED_COLS = {"disaster","barangay","Affected Families","Casualties","Damaged Houses"}

# ─────────────────────────────────────────────────────────────
# SESSION STATE  — keeps assessment additions across reruns
# ─────────────────────────────────────────────────────────────

if "added_entries" not in st.session_state:
    st.session_state.added_entries = []   # list of dicts

def load_base_df() -> pd.DataFrame:
    """Load and normalise the embedded real dataset."""
    df = pd.read_csv(io.StringIO(REAL_CSV))
    # The CSV header uses 'Baranagy' (typo) — handle both
    if "Baranagy" in df.columns:
        df.rename(columns={"Baranagy": "barangay"}, inplace=True)
    if "Disaster" in df.columns:
        df.rename(columns={"Disaster": "disaster"}, inplace=True)
    for col in ["Affected Families", "Casualties", "Damaged Houses"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["disaster"] = df["disaster"].astype(str).str.strip()
    df["barangay"] = df["barangay"].astype(str).str.strip()
    return df


def build_working_df() -> pd.DataFrame:
    """Combine base dataset with any admin-added entries."""
    base = load_base_df()
    if st.session_state.added_entries:
        added = pd.DataFrame(st.session_state.added_entries)
        return pd.concat([base, added], ignore_index=True)
    return base

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### WPS")
    st.caption("Weighted Priority Scheduler")
    st.markdown("---")
    page = st.radio(
        "Module",
        [
            "Dashboard",
            "Assessment Input",
            "Priority Queue",
            "Analytics",
            "Evaluation",
            "How It Works",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Data source toggle
    use_upload = st.toggle("Upload custom CSV instead", value=False)
    uploaded_file = None
    if use_upload:
        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            label_visibility="collapsed",
            help="Required columns: disaster, barangay, Affected Families, Casualties, Damaged Houses",
        )

    st.markdown("---")
    st.caption("Baguio City EOC · Admin")

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("## Weighted Priority Scheduler")
st.markdown(
    '<p class="section-label">Baguio City EOC · Multi-criteria disaster response prioritization</p>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# RESOLVE ACTIVE DATASET
# ─────────────────────────────────────────────────────────────

if use_upload and uploaded_file is not None:
    try:
        df_raw = pd.read_csv(uploaded_file)
        # Normalise column names
        col_map = {}
        for c in df_raw.columns:
            cl = c.strip().lower()
            if cl in ("baranagy","barangay","name"): col_map[c] = "barangay"
            elif cl in ("disaster","event"):         col_map[c] = "disaster"
        df_raw.rename(columns=col_map, inplace=True)
        missing = REQUIRED_COLS - set(df_raw.columns)
        if missing:
            st.error(f"Missing columns in uploaded CSV: {', '.join(sorted(missing))}")
            st.stop()
        for col in ["Affected Families","Casualties","Damaged Houses"]:
            df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0).astype(int)
        df_raw["disaster"] = df_raw["disaster"].astype(str).str.strip()
        df_raw["barangay"] = df_raw["barangay"].astype(str).str.strip()
        df = df_raw
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
        st.stop()
else:
    df = build_working_df()
    if page != "Assessment Input":
        st.markdown(
            '<div class="info-banner">Showing official Baguio City EOC dataset '
            f'({len(df)} records · {df["disaster"].nunique()} disaster events). '
            'Use "Assessment Input" to add new entries, or toggle "Upload custom CSV" in the sidebar.</div>',
            unsafe_allow_html=True,
        )

# Run WSM
df_final, perf_df, total_ms = run_wsm(df)

# ═════════════════════════════════════════════════════════════
# PAGES
# ═════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────

if page == "Dashboard":

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Disaster Events",  df_final["disaster"].nunique())
    c2.metric("Total Records",    len(df_final))
    c3.metric("Processing Time",  f"{total_ms:.4f} ms")
    c4.metric("Avg per Record",   f"{total_ms / len(df_final):.6f} ms")

    st.markdown("---")

    # Highest priority callout
    top     = df_final.iloc[0]
    top_urg = urgency_label(top["score_pct"])
    top_col = urgency_color(top_urg)

    ca, cb = st.columns([3, 1])
    with ca:
        st.markdown(
            f"**Highest Priority Barangay** &nbsp;"
            f"<span style='background:#1a2332;color:{top_col};border:1px solid {top_col};"
            f"padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;"
            f"letter-spacing:0.5px;text-transform:uppercase'>{top_urg}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<span style='font-family:IBM Plex Mono;font-size:2rem;color:#e6edf3;"
            f"font-weight:600'>{top['barangay']}</span>"
            f"&nbsp;&nbsp;<span style='color:#8b949e;font-size:1rem'>"
            f"{top['disaster']} &nbsp;·&nbsp; Score {top['score_pct']:.2f}%</span>",
            unsafe_allow_html=True,
        )
    with cb:
        st.metric("Score", f"{top['score_pct']:.2f}%")

    st.markdown("---")

    # Per-disaster summary cards (up to 4 per row)
    disasters = list(df_final["disaster"].unique())
    for row_start in range(0, len(disasters), 4):
        row_d = disasters[row_start:row_start + 4]
        cols  = st.columns(len(row_d))
        for i, d in enumerate(row_d):
            sub   = df_final[df_final["disaster"] == d]
            top_b = sub.iloc[0]
            urg   = urgency_label(top_b["score_pct"])
            col   = urgency_color(urg)
            with cols[i]:
                st.markdown(
                    f'<div class="stat-card">'
                    f'<div style="font-size:10px;text-transform:uppercase;letter-spacing:1.2px;'
                    f'color:#8b949e;margin-bottom:6px">{d}</div>'
                    f'<div style="font-size:1rem;font-family:IBM Plex Mono;color:#e6edf3;'
                    f'font-weight:600;margin-bottom:4px">{top_b["barangay"]}</div>'
                    f'<div style="font-size:11px;margin-bottom:10px">'
                    f'<span style="color:{col};font-weight:600;text-transform:uppercase;'
                    f'font-size:10px;letter-spacing:0.5px">{urg}</span>'
                    f'&nbsp;·&nbsp;<span style="color:#8b949e">Score {top_b["score_pct"]:.1f}%</span>'
                    f'</div>'
                    f'<div style="display:flex;gap:14px;font-size:11px">'
                    f'<div><div style="color:#8b949e;text-transform:uppercase;font-size:9px;'
                    f'letter-spacing:1px">Records</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">{len(sub)}</div></div>'
                    f'<div><div style="color:#8b949e;text-transform:uppercase;font-size:9px;'
                    f'letter-spacing:1px">Casualties</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">{sub["Casualties"].sum()}</div></div>'
                    f'<div><div style="color:#8b949e;text-transform:uppercase;font-size:9px;'
                    f'letter-spacing:1px">Families</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">{sub["Affected Families"].sum()}</div></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("")

    st.markdown("---")
    st.markdown("#### Top Priority Rankings")

    df_final["Urgency"] = df_final["score_pct"].apply(urgency_label)
    show_df = df_final[[
        "disaster","rank","barangay","score_pct",
        "Affected Families","Casualties","Damaged Houses","Urgency",
    ]].rename(columns={
        "disaster":"Disaster","rank":"Rank","barangay":"Barangay","score_pct":"Score (%)",
    })

    st.dataframe(
        show_df.style.background_gradient(subset=["Score (%)"], cmap="Blues"),
        use_container_width=True, height=480,
    )
    st.download_button(
        "Download Full Rankings CSV",
        data=show_df.to_csv(index=False).encode(),
        file_name="wps_rankings.csv", mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────
# ASSESSMENT INPUT  — admin / LGU data entry form
# ─────────────────────────────────────────────────────────────

elif page == "Assessment Input":

    st.markdown("#### Assessment Input")
    st.markdown(
        '<p class="section-label">Admin / LGU — add or update barangay disaster data</p>',
        unsafe_allow_html=True,
    )

    # ── Add new entry form ────────────────────────────────────
    with st.expander("Add New Assessment Entry", expanded=True):

        # Populate dropdown with all known barangays from the base dataset
        base_df    = load_base_df()
        known_brgy = sorted(base_df["barangay"].unique().tolist())
        known_dis  = sorted(base_df["disaster"].unique().tolist())

        col_d, col_b = st.columns([2, 2])
        with col_d:
            disaster_opt = st.selectbox(
                "Disaster Event",
                options=["— select or type new —"] + known_dis,
                key="form_disaster_select",
            )
            if disaster_opt == "— select or type new —":
                disaster_val = st.text_input(
                    "Or enter new disaster name",
                    placeholder="e.g. TY Marce (2025)",
                    key="form_disaster_new",
                )
            else:
                disaster_val = disaster_opt

        with col_b:
            barangay_opt = st.selectbox(
                "Barangay",
                options=["— select or type new —"] + known_brgy,
                key="form_brgy_select",
            )
            if barangay_opt == "— select or type new —":
                barangay_val = st.text_input(
                    "Or enter new barangay name",
                    placeholder="e.g. New Barangay",
                    key="form_brgy_new",
                )
            else:
                barangay_val = barangay_opt

        st.markdown("")
        n1, n2, n3 = st.columns(3)
        with n1:
            fam_val = st.number_input(
                "Affected Families", min_value=0, value=0, step=1, key="form_fam"
            )
        with n2:
            cas_val = st.number_input(
                "Casualties", min_value=0, value=0, step=1, key="form_cas"
            )
        with n3:
            house_val = st.number_input(
                "Damaged Houses", min_value=0, value=0, step=1, key="form_house"
            )

        st.markdown("")
        submit = st.button("Add Entry", type="primary")

        if submit:
            d_clean = disaster_val.strip()
            b_clean = barangay_val.strip()
            if not d_clean or not b_clean:
                st.error("Both Disaster Event and Barangay are required.")
            else:
                st.session_state.added_entries.append({
                    "disaster":          d_clean,
                    "barangay":          b_clean,
                    "Affected Families": int(fam_val),
                    "Casualties":        int(cas_val),
                    "Damaged Houses":    int(house_val),
                })
                st.success(f"Entry added: {b_clean} / {d_clean}")
                st.rerun()

    # ── Show pending entries ──────────────────────────────────
    if st.session_state.added_entries:
        st.markdown("---")
        st.markdown(f"#### Pending Entries &nbsp; <span style='color:#8b949e;font-size:13px;font-weight:400'>{len(st.session_state.added_entries)} record(s) queued</span>", unsafe_allow_html=True)

        for i, entry in enumerate(st.session_state.added_entries):
            urg = urgency_label(0)  # not yet scored; show after commit
            ecol1, ecol2, ecol3, ecol4, ecol5, ecol6 = st.columns([3, 2, 1, 1, 1, 1])
            ecol1.markdown(f"**{entry['barangay']}**")
            ecol2.markdown(f"<span style='color:#8b949e;font-size:12px'>{entry['disaster']}</span>", unsafe_allow_html=True)
            ecol3.markdown(f"<span style='color:#8b949e;font-size:11px'>Fam: {entry['Affected Families']}</span>", unsafe_allow_html=True)
            ecol4.markdown(f"<span style='color:#8b949e;font-size:11px'>Cas: {entry['Casualties']}</span>", unsafe_allow_html=True)
            ecol5.markdown(f"<span style='color:#8b949e;font-size:11px'>Hse: {entry['Damaged Houses']}</span>", unsafe_allow_html=True)
            if ecol6.button("Remove", key=f"del_{i}"):
                st.session_state.added_entries.pop(i)
                st.rerun()

        st.markdown("")
        bc1, bc2 = st.columns([1, 4])
        with bc1:
            if st.button("Clear All Entries", type="secondary"):
                st.session_state.added_entries = []
                st.rerun()
        with bc2:
            # Download pending as CSV
            pending_df = pd.DataFrame(st.session_state.added_entries)
            st.download_button(
                "Download Pending Entries as CSV",
                data=pending_df.to_csv(index=False).encode(),
                file_name="wps_new_entries.csv", mime="text/csv",
            )

    else:
        st.markdown("---")
        st.markdown(
            '<div style="color:#8b949e;font-size:13px;padding:16px 0">'
            'No pending entries. Use the form above to add assessment data.</div>',
            unsafe_allow_html=True,
        )

    # ── Upload a batch CSV of new entries ─────────────────────
    st.markdown("---")
    with st.expander("Batch Upload Assessment CSV"):
        st.markdown(
            '<p class="section-label">Upload multiple rows at once — will be merged with the existing dataset</p>',
            unsafe_allow_html=True,
        )
        batch_file = st.file_uploader(
            "Assessment batch CSV",
            type=["csv"], key="batch_upload",
            label_visibility="collapsed",
        )
        # Template download
        template = pd.DataFrame([{
            "disaster":"TY Marce (2025)","barangay":"Irisan",
            "Affected Families":10,"Casualties":2,"Damaged Houses":5,
        }])
        st.download_button(
            "Download CSV template",
            data=template.to_csv(index=False).encode(),
            file_name="assessment_template.csv", mime="text/csv",
        )
        if batch_file:
            try:
                batch_df = pd.read_csv(batch_file)
                col_map  = {}
                for c in batch_df.columns:
                    cl = c.strip().lower()
                    if cl in ("baranagy","barangay"): col_map[c] = "barangay"
                    elif cl == "disaster":            col_map[c] = "disaster"
                batch_df.rename(columns=col_map, inplace=True)
                for col in ["Affected Families","Casualties","Damaged Houses"]:
                    if col in batch_df.columns:
                        batch_df[col] = pd.to_numeric(batch_df[col], errors="coerce").fillna(0).astype(int)
                st.dataframe(batch_df, use_container_width=True)
                if st.button("Import Batch", type="primary"):
                    for _, row in batch_df.iterrows():
                        st.session_state.added_entries.append({
                            "disaster":          str(row.get("disaster","")).strip(),
                            "barangay":          str(row.get("barangay","")).strip(),
                            "Affected Families": int(row.get("Affected Families", 0)),
                            "Casualties":        int(row.get("Casualties", 0)),
                            "Damaged Houses":    int(row.get("Damaged Houses", 0)),
                        })
                    st.success(f"Imported {len(batch_df)} entries.")
                    st.rerun()
            except Exception as e:
                st.error(f"Could not read file: {e}")

# ─────────────────────────────────────────────────────────────
# PRIORITY QUEUE
# ─────────────────────────────────────────────────────────────

elif page == "Priority Queue":

    st.markdown("#### Priority Queue")

    selected_disaster = st.selectbox("Disaster event", df_final["disaster"].unique())
    subset = df_final[df_final["disaster"] == selected_disaster].copy()
    subset["Urgency"] = subset["score_pct"].apply(urgency_label)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Barangays",         len(subset))
    s2.metric("Total Casualties",  f"{subset['Casualties'].sum():,}")
    s3.metric("Affected Families", f"{subset['Affected Families'].sum():,}")
    s4.metric("Damaged Houses",    f"{subset['Damaged Houses'].sum():,}")
    st.markdown("")

    export_cols = {
        "rank":"Rank","barangay":"Barangay","score_pct":"Score (%)",
        "Affected Families":"Affected Families","Casualties":"Casualties",
        "Damaged Houses":"Damaged Houses",
        "norm_families":"Norm Families","norm_casualties":"Norm Casualties",
        "norm_damaged":"Norm Damaged","Urgency":"Urgency",
    }
    renamed = subset[list(export_cols)].rename(columns=export_cols)
    st.dataframe(
        renamed.style.background_gradient(subset=["Score (%)"], cmap="Blues"),
        use_container_width=True, height=520,
    )
    st.download_button(
        "Download Queue CSV",
        data=renamed.to_csv(index=False).encode(),
        file_name=f"queue_{selected_disaster.replace(' ','_')}.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────────────────────────

elif page == "Analytics":

    st.markdown("#### Analytics")

    selected_disaster = st.selectbox("Disaster event", df_final["disaster"].unique())
    top10    = df_final[df_final["disaster"] == selected_disaster].nsmallest(10, "rank")
    full_sub = df_final[df_final["disaster"] == selected_disaster].copy()
    full_sub["Urgency"] = full_sub["score_pct"].apply(urgency_label)

    fig1 = px.bar(
        top10.sort_values("score_pct"), x="score_pct", y="barangay", orientation="h",
        title="Priority Score — Top 10 Barangays",
        color="score_pct", color_continuous_scale=BLUE_SCALE,
        labels={"score_pct":"Score (%)","barangay":""},
    )
    fig1.update_layout(**PLOTLY_BASE)
    fig1.update_coloraxes(showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.pie(
            top10, names="barangay", values="Affected Families",
            title="Affected Families Distribution",
            color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.45,
        )
        fig2.update_layout(**PLOTLY_BASE)
        fig2.update_traces(textfont_color="#e6edf3")
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = px.bar(
            top10, x="barangay", y="Casualties",
            title="Casualties per Barangay",
            color="Casualties", color_continuous_scale=BLUE_SCALE,
            labels={"barangay":""},
        )
        fig3.update_layout(**PLOTLY_BASE, xaxis_tickangle=-35)
        fig3.update_coloraxes(showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    melt = top10.melt(
        id_vars="barangay",
        value_vars=["norm_families","norm_casualties","norm_damaged"],
        var_name="Criterion", value_name="Normalized Score",
    )
    melt["Criterion"] = melt["Criterion"].map({
        "norm_families":"Affected Families",
        "norm_casualties":"Casualties",
        "norm_damaged":"Damaged Houses",
    })
    fig4 = px.bar(
        melt, x="barangay", y="Normalized Score", color="Criterion",
        title="Normalized Score Breakdown per Barangay",
        barmode="stack",
        color_discrete_sequence=["#58a6ff","#3fb950","#d29922"],
        labels={"barangay":""},
    )
    fig4.update_layout(**PLOTLY_BASE, xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(
        full_sub, x="Casualties", y="score_pct",
        size="Affected Families", color="Urgency",
        hover_name="barangay",
        color_discrete_map={"Critical":"#f85149","High":"#e3b341","Moderate":"#58a6ff","Low":"#8b949e"},
        title="Priority Score vs Casualties  (bubble size = affected families)",
        labels={"score_pct":"Score (%)"},
    )
    fig5.update_layout(**PLOTLY_BASE)
    st.plotly_chart(fig5, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────────────────────────

elif page == "Evaluation":

    st.markdown("#### System Evaluation")
    tab_jac, tab_perf = st.tabs(["Jaccard Index","Computational Efficiency"])

    with tab_jac:
        st.markdown(
            '<p class="section-label">Top-k agreement between WPS and single-criterion baselines</p>',
            unsafe_allow_html=True,
        )
        K_VALUES  = [3, 5]
        BASELINES = {
            "Families only":   "Affected Families",
            "Casualties only": "Casualties",
            "Houses only":     "Damaged Houses",
        }
        baseline_results = {}
        for b_label, b_col in BASELINES.items():
            groups = []
            for d_name, grp in df.groupby("disaster"):
                g = grp.copy().sort_values(b_col, ascending=False)
                g["rank"] = range(1, len(g) + 1)
                groups.append(g)
            baseline_results[b_label] = pd.concat(groups, ignore_index=True)

        records = []
        for k in K_VALUES:
            for d_name in df_final["disaster"].unique():
                d_sub = df_final[df_final["disaster"] == d_name]
                if len(d_sub) < k:
                    continue
                wps_topk = set(d_sub.nsmallest(k,"rank")["barangay"])
                for b_label, b_df in baseline_results.items():
                    base_topk = set(b_df[b_df["disaster"]==d_name].nsmallest(k,"rank")["barangay"])
                    records.append({
                        "Disaster": d_name, "k": k,
                        "Baseline": b_label,
                        "Jaccard":  round(jaccard(wps_topk, base_topk), 4),
                    })

        jac_df = pd.DataFrame(records)
        st.dataframe(jac_df, use_container_width=True)

        fig_j = px.bar(
            jac_df, x="Baseline", y="Jaccard", color="k", barmode="group",
            title="Top-k Agreement with Single-Criterion Baselines",
            color_discrete_sequence=["#58a6ff","#3fb950"],
            labels={"Jaccard":"Jaccard Index","k":"k"},
        )
        fig_j.update_layout(**PLOTLY_BASE)
        st.plotly_chart(fig_j, use_container_width=True)

    with tab_perf:
        st.markdown(
            '<p class="section-label">WSM processing time per disaster group</p>',
            unsafe_allow_html=True,
        )
        perf_display = perf_df.copy()
        perf_display["ms / record"] = (
            perf_display["Time (ms)"] / perf_display["Records"]
        ).round(6)
        st.dataframe(perf_display, use_container_width=True)

        fig_p = px.bar(
            perf_display, x="Disaster", y="ms / record",
            title="Processing Time per Record (ms)",
            color="ms / record", color_continuous_scale=BLUE_SCALE,
        )
        fig_p.update_layout(**PLOTLY_BASE, xaxis_tickangle=-30)
        fig_p.update_coloraxes(showscale=False)
        st.plotly_chart(fig_p, use_container_width=True)

        p1, p2 = st.columns(2)
        p1.metric("Total processing time", f"{total_ms:.4f} ms")
        p2.metric("Records processed",     len(df_final))

# ─────────────────────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────────────────────

elif page == "How It Works":

    st.markdown("#### Algorithm Reference")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**Weighted Sum Model (WSM)**

Each barangay receives a priority score from three equally weighted criteria:

```
Score = (Norm_Families + Norm_Casualties + Norm_Houses) / 3
```

Barangays are ranked in descending order within each disaster group.
Ties are resolved by raw casualty count.
        """)
    with col_b:
        st.markdown("""
**Min-Max Normalization**

Raw values are scaled to [0, 1] so criteria with different units stay comparable:

```
Norm(x) = (x − min) / (max − min)
```

If all values in a group are equal, 0.5 is assigned (neutral).
        """)

    st.markdown("---")
    st.markdown("**Urgency Thresholds**")
    st.dataframe(
        pd.DataFrame([
            {"Score Range":"≥ 70%",     "Level":"Critical", "Response Target":"Within 24 hours"},
            {"Score Range":"40% – 69%", "Level":"High",     "Response Target":"24 – 48 hours"},
            {"Score Range":"10% – 39%", "Level":"Moderate", "Response Target":"2 – 3 days"},
            {"Score Range":"< 10%",     "Level":"Low",      "Response Target":"Monitoring"},
        ]),
        use_container_width=True, hide_index=True,
    )

    st.markdown("---")
    st.markdown("""
**CSV Column Requirements**

| Column | Type | Notes |
|---|---|---|
| `disaster` | string | Event name, e.g. "TY Carina (2024)" |
| `barangay` | string | Barangay name (typo "Baranagy" also accepted) |
| `Affected Families` | integer | Displaced or affected family count |
| `Casualties` | integer | Casualty count |
| `Damaged Houses` | integer | Structurally damaged house count |

Each disaster group is normalized independently.
    """)

    st.markdown("---")
    st.markdown("**Download the official dataset**")
    base_df = load_base_df()
    st.download_button(
        "Download full_dataset.csv",
        data=base_df.rename(columns={"barangay":"Barangay","disaster":"Disaster"}).to_csv(index=False).encode(),
        file_name="full_dataset.csv", mime="text/csv",
    )
