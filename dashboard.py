"""pages/dashboard.py"""
import streamlit as st
from datetime import datetime
from utils import get_stats, get_assessed, get_urgency


def show():
    st.markdown("## 📊 Dashboard")
    st.caption("Weighted Sum Model (WSM) Priority Scheduling for 128 Barangays")

    # ── Alert Banner ──────────────────────────────────────────────────────────
    now = datetime.now()
    st.markdown(f"""
    <div class="alert-banner">
        <h3 style="margin:0 0 8px 0">🚨 Emergency Response Dashboard</h3>
        <p style="color:#94a3b8;margin:0">
            Real-time disaster prioritization for 128 barangays of Baguio City.
            Rankings computed using the Weighted Sum Model based on casualties,
            affected families, and damaged structures.
        </p>
        <div style="display:flex;gap:16px;margin-top:16px">
            <div style="background:#1e293b;padding:12px 20px;border-radius:12px;border:1px solid #334155">
                <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:2px">Status</div>
                <div style="font-size:18px;font-weight:900;color:#ef4444">OPERATIONAL</div>
            </div>
            <div style="background:#1e293b;padding:12px 20px;border-radius:12px;border:1px solid #334155">
                <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:2px">Last Update</div>
                <div style="font-size:18px;font-weight:900;color:#fff">{now.strftime('%H:%M')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    stats = get_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏆 Top Priority", stats["highest_priority_name"])
    with col2:
        st.metric("👨‍👩‍👧 Total Affected Families", f"{stats['total_families']:,}")
    with col3:
        st.metric("🩸 Total Casualties", f"{stats['total_casualties']:,}")
    with col4:
        st.metric("📍 Barangays Assessed", f"{stats['total_assessed']}")

    st.markdown("---")

    # ── Top 5 Priority Areas + Operational Status ─────────────────────────────
    left, right = st.columns([2, 1])

    with left:
        st.markdown("#### 📈 Critical Priority Areas (Top 5)")
        assessed = get_assessed()
        top5 = assessed[:5]

        if top5:
            for b in top5:
                urg = get_urgency(b.priority_score)
                pct = b.priority_score * 100
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px 18px;
                            display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                    <div style="display:flex;align-items:center;gap:14px">
                        <div style="width:40px;height:40px;border-radius:10px;background:#f8fafc;
                                    display:flex;align-items:center;justify-content:center;
                                    font-weight:900;color:#64748b;font-size:13px">#{b.rank}</div>
                        <div>
                            <div style="font-weight:700;color:#0f172a;font-size:14px">{b.name}</div>
                            <div style="font-size:11px;color:#94a3b8;margin-top:2px">
                                👨‍👩‍👧 {b.affected_families} families &nbsp;·&nbsp; 🩸 {b.casualties} casualties
                            </div>
                        </div>
                    </div>
                    <div style="text-align:right">
                        <span class="{urg['badge']}">{urg['label']}</span>
                        <div style="font-size:20px;font-weight:900;font-family:monospace;color:#0f172a;margin-top:4px">
                            {pct:.1f}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No assessment data yet. Go to **Assessment Input** to add data.")

    with right:
        st.markdown("#### 🎯 Operational Status")
        total = 128
        assessed_n = stats["total_assessed"]
        remaining  = total - assessed_n
        progress   = assessed_n / total

        st.markdown(f"""
        <div style="background:#f8fafc;border-radius:16px;padding:20px">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px">
                <span style="color:#64748b">Total Barangays</span><strong>128</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px">
                <span style="color:#64748b">Assessed</span>
                <strong style="color:#2563eb">{assessed_n}</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:12px">
                <span style="color:#64748b">Remaining</span><strong>{remaining}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress)

        st.markdown("---")
        st.warning(
            "⚠️ **Quick Action Required**\n\n"
            "Check the top-ranked barangays in the Priority Queue. "
            "Recommendations update automatically as new data is entered."
        )
