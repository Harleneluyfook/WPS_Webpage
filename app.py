"""
Weighted Priority Scheduler (WPS)
Baguio City Emergency Response System
Streamlit Version
"""

import streamlit as st
from utils import init_session_state

st.set_page_config(
    page_title="WPS – Baguio City EOC",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0f172a; }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #ffffff !important; }

    /* Metric cards */
    [data-testid="stMetric"] { background:#fff; border-radius:16px; padding:16px; border:1px solid #e2e8f0; }
    [data-testid="stMetricValue"] { font-size:1.8rem !important; font-weight:900 !important; }

    /* Urgency badges */
    .badge-highest { background:#fee2e2; color:#dc2626; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; }
    .badge-urgent  { background:#ffedd5; color:#f97316; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; }
    .badge-moderate{ background:#dbeafe; color:#3b82f6; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; }
    .badge-low     { background:#f1f5f9; color:#94a3b8; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; }

    /* Alert banner */
    .alert-banner { background:#0f172a; color:#fff; border-radius:16px; padding:24px; margin-bottom:16px; }

    /* Hide Streamlit default header/footer */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

init_session_state()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚨 WPS")
    st.caption("Baguio City Operations")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        options=[
            "📊 Dashboard",
            "📋 Assessment Input",
            "📌 Priority Queue",
            "📈 Analytics",
            "🔍 Algorithm Assessment",
            "ℹ️ How WPS Works",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Baguio City EOC · Ops Terminal")

# ── Page routing ─────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    from pages.dashboard import show
    show()
elif page == "📋 Assessment Input":
    from pages.assessment import show
    show()
elif page == "📌 Priority Queue":
    from pages.priority_queue import show
    show()
elif page == "📈 Analytics":
    from pages.analytics import show
    show()
elif page == "🔍 Algorithm Assessment":
    from pages.evaluation import show
    show()
elif page == "ℹ️ How WPS Works":
    from pages.how_it_works import show
    show()
