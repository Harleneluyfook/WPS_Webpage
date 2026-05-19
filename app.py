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
    page_title="Weighted Priority Scheduler",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
.stApp {
    background: #0d1117;
    color: #e6edf3;
}
[data-testid="stSidebar"] {
    background: #090e14;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #8b949e !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 13px; letter-spacing: 0.3px; }

[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px 24px;
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
    color: #e6edf3 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: #8b949e !important;
}

h1 { font-size: 1.5rem !important; font-weight: 600 !important; color: #e6edf3 !important; }
h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: #e6edf3 !important; }
h3 { font-size: 1rem   !important; font-weight: 500 !important; color: #c9d1d9 !important; }

.stButton > button {
    background: #21262d; color: #e6edf3;
    border: 1px solid #30363d; border-radius: 6px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 13px; font-weight: 500;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #30363d; border-color: #58a6ff; color: #58a6ff;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
}

hr { border-color: #21262d !important; }
[data-testid="stDataFrame"] { border: 1px solid #21262d; border-radius: 8px; overflow: hidden; }
.stAlert { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 8px !important; color: #8b949e !important; }
[data-testid="stFileUploadDropzone"] { background: #161b22 !important; border: 1px dashed #30363d !important; border-radius: 8px !important; }

.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #21262d; gap: 0; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; font-size: 13px; font-weight: 500; letter-spacing: 0.3px; padding: 8px 20px; border-bottom: 2px solid transparent; }
.stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }

.section-label {
    font-size: 11px; text-transform: uppercase;
    letter-spacing: 1.5px; color: #8b949e;
    margin-bottom: 12px; margin-top: 4px;
}
.demo-banner {
    background: #0e2030; border: 1px solid #1a4a7a;
    border-radius: 8px; padding: 10px 16px;
    font-size: 13px; color: #58a6ff; margin-bottom: 16px;
}
.stat-card {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 8px; padding: 16px 20px;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SAMPLE DATA  — 35 Baguio barangay records, 2 disaster events
# ─────────────────────────────────────────────────────────────

SAMPLE_CSV = """disaster,barangay,Affected Families,Casualties,Damaged Houses
Typhoon Igme,Camp 7,320,14,87
Typhoon Igme,Irisan,580,31,142
Typhoon Igme,Bakakeng Central,210,8,54
Typhoon Igme,Quirino Hill (Upper),440,22,115
Typhoon Igme,Guisad Central,190,6,41
Typhoon Igme,Pacdal,275,11,73
Typhoon Igme,Sto. Niño Village,360,18,96
Typhoon Igme,Lualhati,130,4,28
Typhoon Igme,Holy Ghost Proper,490,26,131
Typhoon Igme,Rock Quarry (Lower),88,2,19
Typhoon Igme,Engineers Hill,165,5,37
Typhoon Igme,Magsaysay Central,310,13,82
Typhoon Igme,Mines View Park,74,1,14
Typhoon Igme,Dominican Hill-Mirador,220,9,58
Typhoon Igme,Pinget,400,20,108
Typhoon Igme,Kias,260,10,67
Typhoon Igme,Ambiong,145,4,33
Typhoon Igme,Loakan Proper,510,28,137
Typhoon Igme,Pinsao Proper,180,7,46
Typhoon Igme,Scout Barrio,95,3,22
Flashflood 2024,Irisan,640,38,178
Flashflood 2024,Loakan Proper,290,15,74
Flashflood 2024,Bakakeng North,470,24,122
Flashflood 2024,Quirino Hill (Lower),380,19,99
Flashflood 2024,Rock Quarry (Upper),510,29,140
Flashflood 2024,Pinget,310,14,81
Flashflood 2024,Guisad Sorong,230,10,58
Flashflood 2024,Camp 8,175,7,42
Flashflood 2024,Pucsusan,420,21,110
Flashflood 2024,Gibraltar,155,5,36
Flashflood 2024,Lucnab,560,33,152
Flashflood 2024,Balsigan,200,8,50
Flashflood 2024,Sto. Niño Village,340,16,89
Flashflood 2024,Kias,270,12,68
Flashflood 2024,Ambiong,120,4,27
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
        perf.append({"Disaster": d_name, "Records": len(group),
                     "Time (ms)": round((time.perf_counter() - t0) * 1000, 6)})
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
    return {"Critical":"#f85149","High":"#e3b341",
            "Moderate":"#58a6ff","Low":"#8b949e"}.get(label, "#8b949e")


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
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### WPS")
    st.caption("Weighted Priority Scheduler")
    st.markdown("---")
    page = st.radio(
        "Module",
        ["Dashboard","Priority Queue","Analytics","Evaluation","How It Works"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    use_demo = st.toggle("Use sample data", value=True)
    if not use_demo:
        uploaded_file = st.file_uploader(
            "Upload CSV", type=["csv"], label_visibility="collapsed",
            help="Required: disaster, barangay, Affected Families, Casualties, Damaged Houses",
        )
    else:
        uploaded_file = None
    st.markdown("---")
    st.caption("Baguio City · EOC System")

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("## Weighted Priority Scheduler")
st.markdown(
    '<p class="section-label">Multi-criteria disaster response prioritization · Weighted Sum Model</p>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# LOAD + VALIDATE DATA
# ─────────────────────────────────────────────────────────────

df_raw = None

if use_demo:
    df_raw = pd.read_csv(io.StringIO(SAMPLE_CSV))
    st.markdown(
        '<div class="demo-banner">Sample data loaded — 35 barangay records across 2 disaster events '
        '(Typhoon Igme &amp; Flashflood 2024). Toggle "Use sample data" off in the sidebar to upload your own CSV.</div>',
        unsafe_allow_html=True,
    )
elif uploaded_file is not None:
    try:
        df_raw = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
        st.stop()

if df_raw is not None:
    missing = REQUIRED_COLS - set(df_raw.columns)
    if missing:
        st.error(f"Missing required columns: {', '.join(sorted(missing))}")
        st.stop()

    df = df_raw.copy()
    for col in ["Affected Families","Casualties","Damaged Houses"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["disaster"] = df["disaster"].astype(str).str.strip()
    df["barangay"] = df["barangay"].astype(str).str.strip()

    df_final, perf_df, total_ms = run_wsm(df)

    # ─────────────────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────────────────

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

        # Per-disaster summary cards
        disasters = df_final["disaster"].unique()
        cols = st.columns(len(disasters))
        for i, d in enumerate(disasters):
            sub   = df_final[df_final["disaster"] == d]
            top_b = sub.iloc[0]
            with cols[i]:
                st.markdown(
                    f'<div class="stat-card">'
                    f'<div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;'
                    f'color:#8b949e;margin-bottom:8px">{d}</div>'
                    f'<div style="font-size:1.3rem;font-family:IBM Plex Mono;color:#e6edf3;'
                    f'font-weight:600;margin-bottom:4px">{top_b["barangay"]}</div>'
                    f'<div style="font-size:12px;color:#8b949e">'
                    f'Top barangay &nbsp;·&nbsp; Score {top_b["score_pct"]:.1f}%</div>'
                    f'<div style="margin-top:12px;display:flex;gap:16px">'
                    f'<div><div style="font-size:10px;color:#8b949e;text-transform:uppercase;'
                    f'letter-spacing:1px">Records</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">{len(sub)}</div></div>'
                    f'<div><div style="font-size:10px;color:#8b949e;text-transform:uppercase;'
                    f'letter-spacing:1px">Casualties</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">'
                    f'{sub["Casualties"].sum():,}</div></div>'
                    f'<div><div style="font-size:10px;color:#8b949e;text-transform:uppercase;'
                    f'letter-spacing:1px">Families</div>'
                    f'<div style="font-family:IBM Plex Mono;color:#c9d1d9">'
                    f'{sub["Affected Families"].sum():,}</div></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("#### Top Priority Rankings")

        df_final["Urgency"] = df_final["score_pct"].apply(urgency_label)
        show_df = df_final[[
            "disaster","rank","barangay","score_pct",
            "Affected Families","Casualties","Damaged Houses","Urgency"
        ]].rename(columns={
            "disaster":"Disaster","rank":"Rank","barangay":"Barangay","score_pct":"Score (%)",
        })

        st.dataframe(
            show_df.style.background_gradient(subset=["Score (%)"], cmap="Blues"),
            use_container_width=True, height=480,
        )
        st.download_button(
            "Download Full Rankings",
            data=show_df.to_csv(index=False).encode(),
            file_name="wps_rankings.csv", mime="text/csv",
        )

    # ─────────────────────────────────────────────────────────
    # PRIORITY QUEUE
    # ─────────────────────────────────────────────────────────

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

    # ─────────────────────────────────────────────────────────
    # ANALYTICS
    # ─────────────────────────────────────────────────────────

    elif page == "Analytics":

        st.markdown("#### Analytics")

        selected_disaster = st.selectbox("Disaster event", df_final["disaster"].unique())
        top10    = df_final[df_final["disaster"] == selected_disaster].nsmallest(10, "rank")
        full_sub = df_final[df_final["disaster"] == selected_disaster].copy()
        full_sub["Urgency"] = full_sub["score_pct"].apply(urgency_label)

        # Horizontal priority bar
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

        # Stacked normalized breakdown
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

        # Scatter: score vs casualties, bubble = families
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

    # ─────────────────────────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────────────────────────

    elif page == "Evaluation":

        st.markdown("#### System Evaluation")
        tab_jac, tab_perf = st.tabs(["Jaccard Index","Computational Efficiency"])

        with tab_jac:
            st.markdown(
                '<p class="section-label">Top-k agreement between WPS and single-criterion baselines</p>',
                unsafe_allow_html=True,
            )
            K_VALUES  = [3, 5]
            BASELINES = {"Families only":"Affected Families","Casualties only":"Casualties","Houses only":"Damaged Houses"}
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
                        records.append({"Disaster":d_name,"k":k,"Baseline":b_label,
                                        "Jaccard":round(jaccard(wps_topk, base_topk), 4)})

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
            perf_display["ms / record"] = (perf_display["Time (ms)"] / perf_display["Records"]).round(6)
            st.dataframe(perf_display, use_container_width=True)

            fig_p = px.bar(
                perf_display, x="Disaster", y="ms / record",
                title="Processing Time per Record (ms)",
                color="ms / record", color_continuous_scale=BLUE_SCALE,
            )
            fig_p.update_layout(**PLOTLY_BASE)
            fig_p.update_coloraxes(showscale=False)
            st.plotly_chart(fig_p, use_container_width=True)

            p1, p2 = st.columns(2)
            p1.metric("Total processing time", f"{total_ms:.4f} ms")
            p2.metric("Records processed",     len(df_final))

    # ─────────────────────────────────────────────────────────
    # HOW IT WORKS
    # ─────────────────────────────────────────────────────────

    elif page == "How It Works":

        st.markdown("#### Algorithm Reference")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
**Weighted Sum Model (WSM)**

Each barangay receives a priority score computed from three criteria
with equal weight (1/3 each):

```
Score = (Norm_Families + Norm_Casualties + Norm_Houses) / 3
```

Barangays are ranked in descending order within each disaster group.
Ties are broken by raw casualties.
            """)
        with col_b:
            st.markdown("""
**Min-Max Normalization**

Raw values are scaled to [0, 1] so criteria with different units
remain comparable:

```
Norm(x) = (x - min) / (max - min)
```

When all values in a group are equal, 0.5 is assigned (neutral).
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
**Input CSV Requirements**

| Column | Type | Description |
|---|---|---|
| `disaster` | string | Disaster event name |
| `barangay` | string | Barangay name |
| `Affected Families` | integer | Number of displaced or affected families |
| `Casualties` | integer | Number of casualties |
| `Damaged Houses` | integer | Number of structurally damaged houses |

Each disaster group is normalized independently.
        """)

        st.markdown("---")
        st.markdown("**Download Sample CSV**")
        st.download_button(
            "Download sample_data.csv",
            data=SAMPLE_CSV.encode(),
            file_name="sample_data.csv", mime="text/csv",
        )

# ─────────────────────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────────────────────

else:
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#8b949e">
        <div style="font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px">
            Upload Required
        </div>
        <div style="font-size:15px;color:#c9d1d9;font-weight:500;margin-bottom:8px">
            Upload a CSV dataset to begin prioritization
        </div>
        <div style="font-size:13px">
            Required columns: disaster · barangay · Affected Families · Casualties · Damaged Houses
        </div>
    </div>
    """, unsafe_allow_html=True)
