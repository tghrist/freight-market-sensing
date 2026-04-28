import streamlit as st
import pandas as pd
import altair as alt


def render_feature_explainability(features_df: pd.DataFrame):
    st.subheader("The Supply Chain Physics: Why These Features?")
    st.markdown("""
    Rather than relying on internal sales sentiment, this XGBoost model was trained on dozens of macroeconomic indicators. 
    Through iterative feature tournaments, the model identified these five indicators as the most mathematically significant 
    drivers of OEM trailer production. 
    """)

    st.divider()

    # =======================================================
    # 3x2 Grid of Small Multiple Charts
    # =======================================================
    st.markdown("### Macroeconomic Trends (2024 - Present)")
    st.caption("Visual verification of feature stability and trend alignment across the current forecasting window.")

    # Create two rows of three columns
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    # Map out the exact columns to plot (Target is red, features are blue)
    charts = [
        (row1_col1, 'target_index', "OEM Trailer Production (Target)", ["#ff0000"]),
        (row1_col2, 'cass_shipments', "Cass Freight Shipments", ["#1f77b4"]),
        (row1_col3, 'ppi_heavy_truck_cab_mfg', "PPI: Heavy Truck Cabs", ["#1f77b4"]),
        (row2_col1, 'industrial_production', "Industrial Production Index", ["#1f77b4"]),
        (row2_col2, 'consumer_sentiment', "Consumer Sentiment", ["#1f77b4"]),
        (row2_col3, 'mfg_inventory_to_sales_ratio', "Mfg Inventory-to-Sales", ["#1f77b4"])
    ]

    for col, col_name, title, hex_color in charts:
        with col:
            st.markdown(f"**{title}**")

            # Prepare dataframe for Altair
            temp_df = features_df[[col_name]].reset_index()
            # Catch the index column name regardless of whether it's 'date' or 'index'
            if 'date' in temp_df.columns:
                temp_df = temp_df.rename(columns={'date': 'Date'})
            elif 'index' in temp_df.columns:
                temp_df = temp_df.rename(columns={'index': 'Date'})

            # Build the Altair chart
            chart = alt.Chart(temp_df).mark_line(color=hex_color[0], strokeWidth=2).encode(
                x=alt.X('Date:T', title=''),
                # zero=False dynamically scales the Y-axis to perfectly frame the data
                y=alt.Y(f'{col_name}:Q', title='', scale=alt.Scale(zero=False))
            ).properties(
                height=200
            )

            # Render in Streamlit
            st.altair_chart(chart, use_container_width=True)

    st.divider()

    # =======================================================
    # Feature Business Logic
    # =======================================================
    st.markdown("### Feature Business Logic")
    st.markdown("""
    **1. Cass Freight Shipments Index** * **The Logic:** Physical freight volume is the ultimate constraint. If freight
    shipments are dropping, fleets have excess capacity. They will not order new trailers to haul freight that doesn't
    exist.

    **2. PPI: Heavy Motor Truck Manufacturing** * **The Logic:** This acts as the ultimate CapEx constraint. As the
    absolute cost of truck cabs reaches historic highs, fleets exhaust their capital budgets simply maintaining their
    power units (tractors). This sticker shock forces them to delay their trailer replacement cycles, driving trailer
    demand down during peak inflationary periods.

    **3. Industrial Production Index** * **The Logic:** A massive percentage of flatbed and dry van freight is tied to
    heavy manufacturing. This serves as the leading indicator for the industrial sector's demand for physical
    transportation.

    **4. Consumer Sentiment Index (UMCSENT)** * **The Logic:** Consumer sentiment is the earliest upstream indicator of
    retail freight volume. Drops in consumer confidence reliably precede drops in retail inventory restocking, which
    eventually hits trailer utilization.

    **5. Manufacturing Inventory-to-Sales Ratio** * **The Logic:** This captures the **Bullwhip Effect**. When this
    ratio spikes, it means factories have overproduced and sales have slowed. They stop shipping goods to warehouses,
    heavily dampening demand for new commercial fleet equipment.
    """)