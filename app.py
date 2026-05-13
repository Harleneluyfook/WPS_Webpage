import streamlit as st

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
