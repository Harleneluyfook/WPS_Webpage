import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

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

/* Sidebar */
[data-testid="stSidebar"] {
    background: #090e14;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * {
    color: #8b949e !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 13px;
    letter-spacing: 0.3px;
}

/* Metric cards */
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

/* Headings */
h1 { font-size: 1.5rem !important; font-weight: 600 !important; color: #e6edf3 !important; letter-spacing: -0.3px; }
h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: #e6edf3 !important; }
h3 { font-size: 1rem   !important; font-weight: 500 !important; color: #c9d1d9 !important; }

/* Buttons */
.stButton > button {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #30363d;
    border-color: #58a6ff;
    color: #58a6ff;
}

/* Selectbox, file uploader, text_input */
[data-testid="stSelectbox"] > div > div,
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
}

/* Divider */
hr { border-color: #21262d !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #21262d;
    border-radius: 8px;
    overflow: hidden;
}

/* Alert / info */
.stAlert {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
}

/* Upload drop zone */
[data-testid="stFileUploadDropzone"] {
    background: #161b22 !important;
    border: 1px dashed #30363d !important;
    border-radius: 8px !important;
}

/* Tab bar */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #21262d;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.3px;
    padding: 8px 20px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
}

/* Section label */
.section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #8b949e;
    margin-bottom: 12px;
    margin-top: 4px;
}

/* Priority badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-critical { background: #3d1a1a; color: #f85149; border: 1px solid #6e1f1f; }
.badge-high     { background: #2d1f0e; color: #e3b341; border: 1px solid #5a3d0e; }
.badge-medium   { background: #0e2030; color: #58a6ff; border: 1px solid #1a4a7a; }
.badge-low      { background: #161b22; color: #8b949e; border: 1px solid #21262d; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def normalize_min_max(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - lo) / (hi - lo)


def urgency_badge(score: float) -> str:
    if score >= 70:
        return '<span class="badge badge-critical">Critical</span>'
    if score >= 40:
        return '<span class="badge badge-high">High</span>'
    if score >= 10:
        return '<span class="badge badge-medium">Moderate</span>'
    return '<span class="badge badge-low">Low</span>'


def jaccard(set_a: set, set_b: set) -> float:
    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#8b949e",
    font_family="IBM Plex Sans",
    title_font_color="#e6edf3",
    title_font_size=14,
    xaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", linecolor="#21262d"),
    yaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", linecolor="#21262d"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262d"),
    margin=dict(l=20, r=20, t=50, b=20),
)

COLOR_SCALE = [
    [0.0,  "#1a2332"],
    [0.33, "#1f3a5f"],
    [0.66, "#1a5fa3"],
    [1.0,  "#58a6ff"],
]

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### WPS")
    st.caption("Weighted Priority Scheduler")
    st.markdown("---")
    page = st.radio(
        "Module",
        ["Dashboard", "Priority Queue", "Analytics", "Evaluation", "How It Works"],
        label_visibility="collapsed",
    )
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
# FILE UPLOAD
# ─────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Upload disaster dataset (CSV)",
    type=["csv"],
    label_visibility="collapsed",
    help="Required columns: disaster, barangay, Affected Families, Casualties, Damaged Houses",
)

REQUIRED_COLS = {"disaster", "barangay", "Affected Families", "Casualties", "Damaged Houses"}

# ─────────────────────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────────────────────

if uploaded_file is not None:

    # ── Read ──────────────────────────────────────────────────
    try:
        df_raw = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
        st.stop()

    missing = REQUIRED_COLS - set(df_raw.columns)
    if missing:
        st.error(f"Missing required columns: {', '.join(sorted(missing))}")
        st.stop()

    # ── Clean ─────────────────────────────────────────────────
    df = df_raw.copy()
    for col in ["Affected Families", "Casualties", "Damaged Houses"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["disaster"]  = df["disaster"].astype(str).str.strip()
    df["barangay"]  = df["barangay"].astype(str).str.strip()

    # ── WSM Processing ────────────────────────────────────────
    disaster_results = []
    perf_data = []
    start_total = time.perf_counter()

    for disaster_name, group in df.groupby("disaster"):
        group = group.copy()
        t0 = time.perf_counter()

        group["norm_families"]   = normalize_min_max(group["Affected Families"])
        group["norm_casualties"] = normalize_min_max(group["Casualties"])
        group["norm_damaged"]    = normalize_min_max(group["Damaged Houses"])

        group["priority_score"] = (
            group["norm_families"] +
            group["norm_casualties"] +
            group["norm_damaged"]
        ) / 3

        group["score_pct"] = (group["priority_score"] * 100).round(2)

        group = group.sort_values("priority_score", ascending=False)
        group["rank"] = range(1, len(group) + 1)

        t1 = time.perf_counter()
        perf_data.append({
            "Disaster":    disaster_name,
            "Records":     len(group),
            "Time (ms)":   round((t1 - t0) * 1000, 6),
        })
        disaster_results.append(group)

    total_time_ms = (time.perf_counter() - start_total) * 1000
    df_final  = pd.concat(disaster_results, ignore_index=True)
    perf_df   = pd.DataFrame(perf_data)

    # ─────────────────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────────────────

    if page == "Dashboard":

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Disaster Events",   df_final["disaster"].nunique())
        c2.metric("Total Records",     len(df_final))
        c3.metric("Processing Time",   f"{total_time_ms:.4f} ms")
        c4.metric("Avg per Record",    f"{total_time_ms / len(df_final):.6f} ms")

        st.markdown("---")

        top = df_final.iloc[0]
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(
                f"**Highest Priority Barangay** &nbsp; {urgency_badge(top['score_pct'])}",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<span style='font-family:IBM Plex Mono;font-size:2rem;color:#e6edf3;"
                f"font-weight:600'>{top['barangay']}</span>&nbsp;&nbsp;"
                f"<span style='color:#8b949e;font-size:1rem'>{top['disaster']} · "
                f"Score {top['score_pct']:.2f}%</span>",
                unsafe_allow_html=True,
            )
        with col_b:
            st.metric("Score", f"{top['score_pct']:.2f}%")

        st.markdown("---")
        st.markdown("#### Top Priority Rankings")

        display_cols = {
            "disaster":         "Disaster",
            "rank":             "Rank",
            "barangay":         "Barangay",
            "score_pct":        "Score (%)",
            "Affected Families":"Affected Families",
            "Casualties":       "Casualties",
            "Damaged Houses":   "Damaged Houses",
        }

        show_df = df_final[list(display_cols)].rename(columns=display_cols)

        st.dataframe(
            show_df.style.background_gradient(
                subset=["Score (%)"],
                cmap="Blues",
            ),
            use_container_width=True,
            height=480,
        )

    # ─────────────────────────────────────────────────────────
    # PRIORITY QUEUE
    # ─────────────────────────────────────────────────────────

    elif page == "Priority Queue":

        st.markdown("#### Priority Queue")

        col_sel, col_dl = st.columns([3, 1])
        with col_sel:
            selected_disaster = st.selectbox(
                "Disaster event",
                df_final["disaster"].unique(),
                label_visibility="visible",
            )
        with col_dl:
            st.markdown("<br>", unsafe_allow_html=True)

        subset = df_final[df_final["disaster"] == selected_disaster].copy()

        export_cols = {
            "rank":             "Rank",
            "barangay":         "Barangay",
            "score_pct":        "Score (%)",
            "Affected Families":"Affected Families",
            "Casualties":       "Casualties",
            "Damaged Houses":   "Damaged Houses",
            "norm_families":    "Norm Families",
            "norm_casualties":  "Norm Casualties",
            "norm_damaged":     "Norm Damaged",
        }

        st.dataframe(
            subset[list(export_cols)]
            .rename(columns=export_cols)
            .style.background_gradient(subset=["Score (%)"], cmap="Blues"),
            use_container_width=True,
            height=520,
        )

        csv_bytes = (
            subset[list(export_cols)]
            .rename(columns=export_cols)
            .to_csv(index=False)
            .encode()
        )
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name=f"priority_queue_{selected_disaster.replace(' ', '_')}.csv",
            mime="text/csv",
        )

    # ─────────────────────────────────────────────────────────
    # ANALYTICS
    # ─────────────────────────────────────────────────────────

    elif page == "Analytics":

        st.markdown("#### Analytics")

        selected_disaster = st.selectbox(
            "Disaster event",
            df_final["disaster"].unique(),
        )

        top10 = (
            df_final[df_final["disaster"] == selected_disaster]
            .nsmallest(10, "rank")
        )

        # Bar – priority scores
        fig1 = px.bar(
            top10.sort_values("score_pct"),
            x="score_pct",
            y="barangay",
            orientation="h",
            title="Priority Score — Top 10 Barangays",
            color="score_pct",
            color_continuous_scale=COLOR_SCALE,
            labels={"score_pct": "Score (%)", "barangay": ""},
        )
        fig1.update_layout(**PLOTLY_LAYOUT)
        fig1.update_coloraxes(showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            fig2 = px.pie(
                top10,
                names="barangay",
                values="Affected Families",
                title="Affected Families Distribution",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.45,
            )
            fig2.update_layout(**PLOTLY_LAYOUT)
            fig2.update_traces(textfont_color="#e6edf3")
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            fig3 = px.bar(
                top10,
                x="barangay",
                y="Casualties",
                title="Casualties per Barangay",
                color="Casualties",
                color_continuous_scale=COLOR_SCALE,
                labels={"barangay": ""},
            )
            fig3.update_layout(**PLOTLY_LAYOUT, xaxis_tickangle=-35)
            fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3, use_container_width=True)

        # Stacked normalized scores
        melt = top10.melt(
            id_vars="barangay",
            value_vars=["norm_families", "norm_casualties", "norm_damaged"],
            var_name="Criterion",
            value_name="Normalized Score",
        )
        melt["Criterion"] = melt["Criterion"].map({
            "norm_families":   "Affected Families",
            "norm_casualties": "Casualties",
            "norm_damaged":    "Damaged Houses",
        })
        fig_stack = px.bar(
            melt,
            x="barangay",
            y="Normalized Score",
            color="Criterion",
            title="Normalized Score Breakdown",
            barmode="stack",
            color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922"],
            labels={"barangay": ""},
        )
        fig_stack.update_layout(**PLOTLY_LAYOUT, xaxis_tickangle=-35)
        st.plotly_chart(fig_stack, use_container_width=True)

    # ─────────────────────────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────────────────────────

    elif page == "Evaluation":

        st.markdown("#### System Evaluation")

        tab_jac, tab_perf = st.tabs(["Jaccard Index", "Computational Efficiency"])

        # ── Jaccard ───────────────────────────────────────────
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

            # Pre-compute baseline rankings
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
                    wps_topk = set(d_sub.nsmallest(k, "rank")["barangay"])
                    for b_label, b_df in baseline_results.items():
                        b_sub    = b_df[b_df["disaster"] == d_name]
                        base_topk = set(b_sub.nsmallest(k, "rank")["barangay"])
                        records.append({
                            "Disaster":  d_name,
                            "k":         k,
                            "Baseline":  b_label,
                            "Jaccard":   round(jaccard(wps_topk, base_topk), 4),
                        })

            jac_df = pd.DataFrame(records)
            st.dataframe(jac_df, use_container_width=True)

            fig4 = px.bar(
                jac_df,
                x="Baseline",
                y="Jaccard",
                color="k",
                barmode="group",
                title="Top-k Agreement with Single-Criterion Baselines",
                color_discrete_sequence=["#58a6ff", "#3fb950"],
                labels={"Jaccard": "Jaccard Index", "k": "k"},
            )
            fig4.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig4, use_container_width=True)

        # ── Performance ───────────────────────────────────────
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

            fig5 = px.bar(
                perf_display,
                x="Disaster",
                y="ms / record",
                title="Processing Time per Record (ms)",
                color="ms / record",
                color_continuous_scale=COLOR_SCALE,
            )
            fig5.update_layout(**PLOTLY_LAYOUT)
            fig5.update_coloraxes(showscale=False)
            st.plotly_chart(fig5, use_container_width=True)

            c1, c2 = st.columns(2)
            c1.metric("Total processing time", f"{total_time_ms:.4f} ms")
            c2.metric("Records processed", len(df_final))

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
        urgency_data = pd.DataFrame([
            {"Score Range": "≥ 70%",        "Level": "Critical", "Response Target": "Within 24 hours"},
            {"Score Range": "40% – 69%",    "Level": "High",     "Response Target": "24 – 48 hours"},
            {"Score Range": "10% – 39%",    "Level": "Moderate", "Response Target": "2 – 3 days"},
            {"Score Range": "< 10%",        "Level": "Low",      "Response Target": "Monitoring"},
        ])
        st.dataframe(urgency_data, use_container_width=True, hide_index=True)

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

# ─────────────────────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────────────────────

else:

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;padding:60px 20px;color:#8b949e">
            <div style="font-size:13px;letter-spacing:2px;text-transform:uppercase;
                        margin-bottom:12px">Upload Required</div>
            <div style="font-size:15px;color:#c9d1d9;font-weight:500;margin-bottom:8px">
                Upload a CSV dataset to begin prioritization
            </div>
            <div style="font-size:13px">
                Required columns: disaster · barangay · Affected Families · Casualties · Damaged Houses
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
