import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Weighted Priority Scheduler",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM DESIGN
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0f172a;
        color: white;
    }

    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Weighted Priority Scheduler (WPS)")
st.caption("Disaster Response Prioritization System")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Assessment Input",
        "Priority Queue",
        "Analytics",
        "Evaluation",
        "How It Works"
    ]
)

# ---------------------------------------------------
# BARANGAYS
# ---------------------------------------------------

barangays = [
    "Asin Road",
    "Aurora Hill",
    "Bakakeng Central",
    "Burnham-Legarda",
    "Camp 7",
    "Engineer’s Hill",
    "Irisan",
    "Loakan Proper",
    "Pacdal",
    "Session Road Area"
]

# ---------------------------------------------------
# SESSION STORAGE
# ---------------------------------------------------

if "data" not in st.session_state:

    st.session_state.data = pd.DataFrame({
        "Barangay": barangays,
        "Casualties": np.random.randint(0, 50, len(barangays)),
        "Affected Families": np.random.randint(50, 1000, len(barangays)),
        "Damaged Houses": np.random.randint(0, 200, len(barangays)),
        "Historical Frequency": np.random.randint(1, 10, len(barangays)),
        "Accessibility": np.random.randint(1, 10, len(barangays))
    })

# ---------------------------------------------------
# WEIGHTED PRIORITY SCHEDULER
# ---------------------------------------------------

def calculate_priority(df):

    max_c = max(df["Casualties"].max(), 1)
    max_f = max(df["Affected Families"].max(), 1)
    max_h = max(df["Damaged Houses"].max(), 1)
    max_hist = max(df["Historical Frequency"].max(), 1)

    df["Priority Score"] = (
        (df["Casualties"] / max_c) * 0.35 +
        (df["Affected Families"] / max_f) * 0.30 +
        (df["Damaged Houses"] / max_h) * 0.20 +
        (df["Historical Frequency"] / max_hist) * 0.15
    )

    df = df.sort_values(
        by="Priority Score",
        ascending=False
    )

    df["Rank"] = range(1, len(df) + 1)

    return df

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if page == "Dashboard":

    st.header("Dashboard")

    ranked_df = calculate_priority(
        st.session_state.data.copy()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Casualties",
        int(ranked_df["Casualties"].sum())
    )

    col2.metric(
        "Affected Families",
        int(ranked_df["Affected Families"].sum())
    )

    col3.metric(
        "Damaged Houses",
        int(ranked_df["Damaged Houses"].sum())
    )

    col4.metric(
        "Barangays",
        len(ranked_df)
    )

    st.divider()

    st.subheader("Top Priority Barangays")

    st.dataframe(
        ranked_df[[
            "Rank",
            "Barangay",
            "Priority Score"
        ]],
        use_container_width=True
    )

    st.divider()

    fig = px.bar(
        ranked_df.head(10),
        x="Barangay",
        y="Priority Score",
        title="Top Priority Barangays"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# ASSESSMENT INPUT
# ---------------------------------------------------

elif page == "Assessment Input":

    st.header("Assessment Input")

    selected = st.selectbox(
        "Select Barangay",
        barangays
    )

    col1, col2 = st.columns(2)

    with col1:

        casualties = st.number_input(
            "Casualties",
            min_value=0,
            value=0
        )

        families = st.number_input(
            "Affected Families",
            min_value=0,
            value=0
        )

    with col2:

        houses = st.number_input(
            "Damaged Houses",
            min_value=0,
            value=0
        )

        historical = st.slider(
            "Historical Disaster Frequency",
            1,
            10,
            5
        )

    if st.button("Save Assessment"):

        idx = st.session_state.data[
            st.session_state.data["Barangay"] == selected
        ].index[0]

        st.session_state.data.loc[idx, "Casualties"] = casualties
        st.session_state.data.loc[idx, "Affected Families"] = families
        st.session_state.data.loc[idx, "Damaged Houses"] = houses
        st.session_state.data.loc[idx, "Historical Frequency"] = historical

        st.success("Assessment Saved Successfully")

# ---------------------------------------------------
# PRIORITY QUEUE
# ---------------------------------------------------

elif page == "Priority Queue":

    st.header("Priority Queue")

    ranked_df = calculate_priority(
        st.session_state.data.copy()
    )

    st.dataframe(
        ranked_df,
        use_container_width=True
    )

# ---------------------------------------------------
# ANALYTICS
# ---------------------------------------------------

elif page == "Analytics":

    st.header("Analytics")

    ranked_df = calculate_priority(
        st.session_state.data.copy()
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.bar(
            ranked_df,
            x="Barangay",
            y="Affected Families",
            title="Affected Families"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        fig2 = px.pie(
            ranked_df,
            names="Barangay",
            values="Casualties",
            title="Casualty Distribution"
        )

                st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------

elif page == "Evaluation":

    st.header("System Evaluation")

    st.info(
        "This module can be used for ISO 25010 and expert evaluation results."
    )

    criteria = {
        "Functionality": 4.8,
        "Usability": 4.6,
        "Reliability": 4.7,
        "Efficiency": 4.5,
        "Maintainability": 4.6
    }

    eval_df = pd.DataFrame({
        "Criteria": list(criteria.keys()),
        "Score": list(criteria.values())
    })

    st.dataframe(eval_df)

    fig = px.bar(
        eval_df,
        x="Criteria",
        y="Score",
        title="Evaluation Results"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------

elif page == "How It Works":

    st.header("How The WPS Algorithm Works")

    st.markdown("""
    ### Weighted Priority Scheduler (WPS)

    The system prioritizes barangays based on:

    - Casualties
    - Affected Families
    - Damaged Houses
    - Historical Disaster Frequency

    Each criterion has a corresponding weight.

    The Weighted Scoring Model (WSM) calculates
    a Priority Score for every barangay.

    Barangays with higher scores are prioritized first
    for disaster response operations.
    """)

    st.divider()

    st.subheader("Priority Formula")

    st.latex(r'''
    Score =
    (C \times 0.35) +
    (F \times 0.30) +
    (H \times 0.20) +
    (HF \times 0.15)
    ''')
