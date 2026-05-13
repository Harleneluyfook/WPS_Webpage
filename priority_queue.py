"""pages/priority_queue.py"""
import streamlit as st
import pandas as pd
import io
from utils import get_urgency, get_recommendation, refresh_rankings


def show():
    st.markdown("## 📌 Disaster Response Priority Queue")
    st.caption("Live ranked list of all 128 Baguio barangays waiting for emergency resources.")

    ranked = st.session_state.ranked_data
    assessed = [b for b in ranked if b.last_updated]

    # ── Controls ──────────────────────────────────────────────────────────────
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Find barangay in queue...", placeholder="Type a name...", label_visibility="collapsed")
    with col_filter:
        urgency_filter = st.selectbox(
            "Filter", ["All", "Highest", "Urgent", "Moderate", "Low"],
            label_visibility="collapsed"
        )

    # ── Export button ─────────────────────────────────────────────────────────
    if assessed:
        rows = []
        for b in assessed:
            urg = get_urgency(b.priority_score)
            rows.append({
                "Rank": b.rank, "Barangay": b.name,
                "Casualties": b.casualties,
                "Affected Families": b.affected_families,
                "Damaged Houses": b.damaged_houses,
                "Priority Score (%)": round(b.priority_score * 100, 2),
                "Urgency": urg["label"],
                "Recommendation": get_recommendation(b.priority_score),
                "Disaster": b.disaster,
            })
        export_df = pd.DataFrame(rows)
        csv_bytes = export_df.to_csv(index=False).encode()
        st.download_button("⬇️ Export Queue as CSV", data=csv_bytes,
                           file_name="wps_priority_queue.csv", mime="text/csv")

    st.markdown("---")

    # ── Active queue stats ────────────────────────────────────────────────────
    highest_n = sum(1 for b in assessed if get_urgency(b.priority_score)["label"] == "Highest")
    c1, c2, c3 = st.columns(3)
    c1.metric("Active in Queue", len(assessed))
    c2.metric("🔴 Highest Priority", highest_n)
    c3.metric("Total Barangays", 128)

    st.markdown("---")

    # ── Queue list ────────────────────────────────────────────────────────────
    display_list = ranked

    if search:
        display_list = [b for b in display_list if search.lower() in b.name.lower()]
    if urgency_filter != "All":
        display_list = [b for b in display_list if get_urgency(b.priority_score)["label"] == urgency_filter]

    if not display_list:
        st.info("No barangays match your current filter.")
        return

    # Show assessed first, then unassessed
    display_assessed   = [b for b in display_list if b.last_updated]
    display_unassessed = [b for b in display_list if not b.last_updated]

    if display_assessed:
        st.markdown("##### 🔴 Assessed Barangays")
        for b in display_assessed:
            urg  = get_urgency(b.priority_score)
            rec  = get_recommendation(b.priority_score)
            pct  = b.priority_score * 100

            with st.expander(
                f"{urg['emoji']} **#{b.rank} {b.name}** — Score: {pct:.1f}% · {urg['label']}",
                expanded=False,
            ):
                dc1, dc2, dc3, dc4 = st.columns(4)
                dc1.metric("Casualties",        b.casualties)
                dc2.metric("Affected Families", b.affected_families)
                dc3.metric("Damaged Houses",    b.damaged_houses)
                dc4.metric("Priority Score",    f"{pct:.1f}%")

                rc1, rc2 = st.columns([3, 1])
                with rc1:
                    st.markdown(f"""
                    **Normalized Scores:**
                    Casualties `{b.normalized_casualties:.3f}` ·
                    Families `{b.normalized_families:.3f}` ·
                    Houses `{b.normalized_houses:.3f}`

                    📋 **Recommendation:** {rec}
                    """)
                with rc2:
                    if st.button("🗑️ Reset", key=f"reset_{b.id}"):
                        b.casualties = 0; b.affected_families = 0; b.damaged_houses = 0
                        b.priority_score = 0; b.last_updated = None
                        refresh_rankings()
                        st.rerun()

    if display_unassessed:
        with st.expander(f"⚪ Unassessed Barangays ({len(display_unassessed)})", expanded=False):
            for b in display_unassessed:
                st.markdown(f"- {b.name}")

    # ── Reset All ─────────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("⚠️ Reset ALL Assessment Data", type="secondary"):
        for b in st.session_state.barangay_list:
            b.casualties = 0; b.affected_families = 0; b.damaged_houses = 0
            b.priority_score = 0; b.last_updated = None
        refresh_rankings()
        st.success("All data has been reset.")
        st.rerun()
