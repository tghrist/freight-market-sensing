import streamlit as st
import pandas as pd
import altair as alt
import math
from src.frontend.data_loader import forecast_slope_percentage

def render_executive_dashboard(history_df: pd.DataFrame, forecast_df: pd.DataFrame):
    # Layout: Executive Metrics Row
    col1, col2, col3 = st.columns(3)

    with col1:
        # Get the final index value
        latest_index = forecast_df['forecast_production_volume'].iloc[-1]

        # Calculate the trend percentage
        fc_trend_pct = forecast_slope_percentage(forecast_df)

        # Use the 'delta' parameter to show the slope
        st.metric(
            label="90-Day Target Index (2017=100)",
            value=f"{latest_index:.1f}",
            delta=f"{fc_trend_pct:+.2f}% (Trend)"
        )

    with col2:
        st.metric(label="Forecast Status", value="Stable / Flat")

    with col3:
        st.metric(label="Primary Market Driver", value="Cass Freight Shipments")

    st.divider()

    # Advanced Altair Chart Integration
    st.subheader("Trailer Production Index: 90-Day Forecast")

    # 1. Prepare the Data
    combined_index = history_df.index.union(forecast_df.index)
    chart_df = pd.DataFrame(index=combined_index)

    chart_df['Historical Actuals'] = history_df['historical_volume']
    chart_df['90-Day AI Forecast'] = forecast_df['forecast_production_volume']

    # Bridge the visual gap
    last_date = history_df.index[-1]
    last_volume = history_df['historical_volume'].iloc[-1]
    chart_df.loc[last_date, '90-Day AI Forecast'] = last_volume

    # 2. "Melt" the Dataframe for Altair
    chart_df = chart_df.reset_index().rename(columns={'date': 'Date', 'index': 'Date'})
    melted_df = chart_df.melt(id_vars=['Date'], var_name='Data Type', value_name='Trailer Production Index')

    # Calculate dynamic y-axis minimum (round down to nearest 5)
    min_val = melted_df['Trailer Production Index'].min()
    y_min = math.floor(min_val / 5.0) * 5

    # 3. Build the Custom Chart
    chart = alt.Chart(melted_df).mark_line(strokeWidth=2.5).encode(
        x=alt.X('Date:T', title=''),
        y=alt.Y('Trailer Production Index:Q', scale=alt.Scale(domainMin=y_min)),
        color=alt.Color('Data Type:N', scale=alt.Scale(
            domain=['Historical Actuals', '90-Day AI Forecast'],
            range=['#1f77b4', '#ff0000']  # Blue and Red
        ), legend=alt.Legend(orient='bottom', title=None)),
        strokeDash=alt.condition(
            alt.datum['Data Type'] == '90-Day AI Forecast',
            alt.value([5, 5]),  # Dashed line
            alt.value([0])  # Solid line
        )
    ).properties(
        height=450
    )

    # Render in Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.caption("Note: This baseline represents a 90-day outlook of OEM trailer production, driven by underlying freight and economic fundamentals.")