import streamlit as st
import pandas as pd
import altair as alt
from src.config import CHAMPION_FEATURES


def render_feature_explainability(features_df: pd.DataFrame):
    st.subheader("The Supply Chain Physics: Why These Features?")
    st.markdown("""
    Rather than relying on internal sales sentiment, this XGBoost model was trained on dozens of macroeconomic indicators. 
    Through iterative feature tournaments, the model identified these specific indicators as the most mathematically significant 
    drivers of OEM trailer production. 
    """)

    st.divider()

    # =======================================================
    # Dynamic Grid of Small Multiple Charts
    # =======================================================
    st.markdown("### Macroeconomic Trends (2024 - Present)")
    st.caption("Visual verification of feature stability and trend alignment across the current forecasting window.")

    # Create the columns (assuming 1 target + up to 5 features = 6 slots)
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    grid_slots = [row1_col1, row1_col2, row1_col3, row2_col1, row2_col2, row2_col3]

    # 1. Render the Target Chart first (Hardcoded as slot 0 since it's the target)
    with grid_slots[0]:
        st.markdown("**OEM Trailer Production (Target)**")
        temp_target_df = features_df[['target_index']].reset_index()
        if 'date' in temp_target_df.columns: temp_target_df = temp_target_df.rename(columns={'date': 'Date'})

        chart = alt.Chart(temp_target_df).mark_line(color="#ff0000", strokeWidth=2).encode(
            x=alt.X('Date:T', title=''),
            y=alt.Y('target_index:Q', title='', scale=alt.Scale(zero=False))
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)

    # 2. Render the Feature Charts dynamically from the config
    for i, (feature_key, feature_meta) in enumerate(CHAMPION_FEATURES.items()):
        # Start at grid_slots[1] because target is in [0]
        slot_index = i + 1
        if slot_index < len(grid_slots):
            with grid_slots[slot_index]:
                st.markdown(f"**{feature_meta['title']}**")

                temp_df = features_df[[feature_key]].reset_index()
                if 'date' in temp_df.columns: temp_df = temp_df.rename(columns={'date': 'Date'})

                chart = alt.Chart(temp_df).mark_line(color=feature_meta['ui_color'], strokeWidth=2).encode(
                    x=alt.X('Date:T', title=''),
                    y=alt.Y(f'{feature_key}:Q', title='', scale=alt.Scale(zero=False))
                ).properties(height=200)
                st.altair_chart(chart, use_container_width=True)

    st.divider()

    # =======================================================
    # Dynamic Feature Business Logic
    # =======================================================
    st.markdown("### Feature Business Logic")

    # Loop through the config to print the text
    counter = 1
    for feature_key, feature_meta in CHAMPION_FEATURES.items():
        st.markdown(f"**{counter}. {feature_meta['title']}** * {feature_meta['logic']}")
        counter += 1