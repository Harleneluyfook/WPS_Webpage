"""pages/assessment.py"""
import streamlit as st
import pandas as pd
import io
import time
from utils import (
    refresh_rankings, get_urgency, get_recommendation, BAGUIO_BARANGAYS
)


def show():
    st.markdown("## 📋 Assessment Input")
    st.caption("Enter disaster impact data per barangay. Rankings recalculate automatically.")

    tab_manual, tab_csv = st.tabs(["✏️ Manual Entry", "📤 CSV Bulk Upload"])

    # ── Manual Entry ──────────────────────────────────────────────────────────
    with tab_manual:
        barangay_names = [b.name for b in st.session_state.barangay_list]

        col_sel, col_dis = st.columns([2, 1])
        with col_sel:
            selected_name = st.selectbox(
                "Select Barangay",
                options=["— choose a barangay —"] + barangay_names,
                key="assess_select",
            )
        with col_dis:
            disaster_type = st.text_input(
                "Disaster / Event (optional)",
                placeholder="e.g. Typhoon Igme",
                key="disaster_type",
            )

        selected = None
        if selected_name and selected_name != "— choose a barangay —":
            selected = next(
                (b for b in st.session_state.barangay_list if b.name == selected_name), None
            )

        if selected:
            urg = get_urgency(selected.priority_score)
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;
                        padding:14px 18px;margin:12px 0;display:flex;align-items:center;
                        justify-content:space-between">
                <div>
                    <div style="font-weight:700;color:#0f172a">{selected.name}</div>
                    <div style="font-size:12px;color:#94a3b8;margin-top:2px">
                        Current rank: #{selected.rank} &nbsp;·&nbsp;
                        Score: {selected.priority_score * 100:.1f}%
                    </div>
                </div>
                <span class="{urg['badge']}">{urg['label']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("##### Impact Data")
        c1, c2, c3 = st.columns(3)
        with c1:
            casualties = st.number_input(
                "🩸 Casualties", min_value=0, value=0, step=1, key="inp_cas"
            )
        with c2:
            families = st.number_input(
                "👨‍👩‍👧 Affected Families", min_value=0, value=0, step=1, key="inp_fam"
            )
        with c3:
            houses = st.number_input(
                "🏚️ Damaged Houses", min_value=0, value=0, step=1, key="inp_hse"
            )

        if st.button("✅ Submit Assessment", type="primary", use_container_width=True):
            if not selected:
                st.error("Please select a barangay first.")
            else:
                selected.casualties       = casualties
                selected.affected_families = families
                selected.damaged_houses   = houses
                selected.disaster         = disaster_type.strip() or "Default"
                selected.last_updated     = time.time()
                refresh_rankings()
                st.success(f"✅ Assessment for **{selected.name}** updated and reranked!")
                st.rerun()

    # ── CSV Upload ────────────────────────────────────────────────────────────
    with tab_csv:
        st.markdown("""
        Upload a CSV with columns:
        `Barangay`, `Casualties`, `Affected Families`, `Damaged Houses`, `Disaster` *(optional)*

        The system accepts common header variations automatically.
        """)

        template_df = pd.DataFrame({
            "Barangay":         ["Camp 7", "Irisan"],
            "Casualties":       [5, 12],
            "Affected Families":[30, 80],
            "Damaged Houses":   [10, 45],
            "Disaster":         ["Typhoon Igme", "Typhoon Igme"],
        })
        csv_bytes = template_df.to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download CSV Template",
            data=csv_bytes,
            file_name="wps_template.csv",
            mime="text/csv",
        )

        uploaded = st.file_uploader("Upload CSV File", type=["csv"])
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                df.columns = df.columns.str.strip()

                # Flexible column mapping
                col_map = {
                    "barangay":          ["Barangay", "barangay", "Baranagy", "Name", "name"],
                    "casualties":        ["Casualties", "casualties"],
                    "affected_families": ["Affected Families", "affected_families", "Families", "families"],
                    "damaged_houses":    ["Damaged Houses", "damaged_houses", "Houses", "houses"],
                    "disaster":          ["Disaster", "disaster", "Event", "event"],
                }

                def find_col(options):
                    for opt in options:
                        if opt in df.columns:
                            return opt
                    return None

                brgy_col = find_col(col_map["barangay"])
                cas_col  = find_col(col_map["casualties"])
                fam_col  = find_col(col_map["affected_families"])
                hse_col  = find_col(col_map["damaged_houses"])
                dis_col  = find_col(col_map["disaster"])

                if not brgy_col:
                    st.error("Could not find 'Barangay' column. Check your CSV headers.")
                else:
                    st.dataframe(df.head(10), use_container_width=True)
                    if st.button("📥 Import Data", type="primary"):
                        count = 0
                        for _, row in df.iterrows():
                            name     = str(row[brgy_col]).strip()
                            disaster = str(row[dis_col]).strip() if dis_col else "Default"
                            cas  = int(row[cas_col])  if cas_col  else 0
                            fam  = int(row[fam_col])  if fam_col  else 0
                            hse  = int(row[hse_col])  if hse_col  else 0

                            match = next(
                                (b for b in st.session_state.barangay_list
                                 if b.name.lower() == name.lower()), None
                            )
                            if match:
                                match.casualties        = cas
                                match.affected_families = fam
                                match.damaged_houses    = hse
                                match.disaster          = disaster
                                match.last_updated      = time.time()
                                count += 1

                        refresh_rankings()
                        st.success(f"✅ Imported and re-ranked {count} barangays.")
                        st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
