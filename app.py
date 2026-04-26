import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="CV & Trailer Demand Forecast",
    page_icon="🚛",
    layout="wide"
)

# 2. Title and Executive Summary
st.title("Commercial Vehicle & Trailer Demand Forecast")
st.markdown("""
Designed for Tier 1 commercial vehicle suppliers, this machine learning pipeline predicts the 90-day forward trajectory
of North American trailer manufacturing. Rather than forecasting volatile freight spot rates, this engine tracks the
'heavy physics' of the supply chain—capital costs, inventory bottlenecks, and physical output—to predict actual OEM
assembly line volume. This provides component manufacturers with an unbiased, data-driven anchor for Sales and
Operations Planning.
""")

st.divider()


# 3. Load the Data
@st.cache_data
def load_data():
    # Load Forecast
    forecast_df = pd.read_csv('live_90_day_forecast.csv', parse_dates=['date'])
    forecast_df.set_index('date', inplace=True)

    # Load Historical Actuals
    history_df = pd.read_csv('historical_actuals.csv', parse_dates=['date'])
    history_df.set_index('date', inplace=True)

    return history_df, forecast_df


def forecast_slope_percentage(df: pd.DataFrame) -> float:
    # Create the x-axis
    df['row_number'] = range(1, len(df) + 1)

    # Calculate the linear trendline (slope = points per period)
    slope, intercept = np.polyfit(df['row_number'], df['forecast_production_volume'], 1)

    # Calculate the starting and ending values of that smoothed trendline
    start_value = (slope * 1) + intercept
    end_value = (slope * len(df)) + intercept

    # Calculate the true percentage change across the forecast window
    total_pct_change = ((end_value - start_value) / start_value) * 100

    return total_pct_change


try:
    history_df, forecast_df = load_data()

    # 4. Layout: Executive Metrics Row (Keep your existing metrics here!)
    col1, col2, col3 = st.columns(3)

    with col1:
        # Get the final index value
        latest_index = forecast_df['forecast_production_volume'].iloc[-1]

        # Calculate the trend percentage using your new function
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

    # =======================================================
    # 5. Advanced Altair Chart Integration
    # =======================================================
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
    # Rename 'date' (or 'index') to a capital 'Date' to fix the KeyError
    chart_df = chart_df.reset_index().rename(columns={'date': 'Date', 'index': 'Date'})
    melted_df = chart_df.melt(id_vars=['Date'], var_name='Data Type', value_name='Trailer Production Index')

    # 3. Build the Custom Chart
    chart = alt.Chart(melted_df).mark_line(strokeWidth=2.5).encode(
        x=alt.X('Date:T', title=''),
        # Set the exact Y-Axis floor to 40
        y=alt.Y('Trailer Production Index:Q', scale=alt.Scale(domainMin=40)),
        color=alt.Color('Data Type:N', scale=alt.Scale(
            domain=['Historical Actuals', '90-Day AI Forecast'],
            range=['#1f77b4', '#ff0000']  # Blue and Red
        ), legend=alt.Legend(orient='bottom', title=None)),  # <--- MOVED TO BOTTOM
        # Reintroduce the dashed line for the forecast
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

    st.caption(
        "Note: This baseline represents a 90-day outlook of OEM trailer production, driven by underlying freight and economic fundamentals.")

except FileNotFoundError:
    st.error("Data files not found. Please run the `models.py` export pipeline first.")

# =======================================================
# 6. Sidebar for Navigation/Context
# =======================================================
st.sidebar.header("Model Architecture")
st.sidebar.info("""
**Engine:** XGBoost Regressor  
**Horizon:** 90-Day Forward  
**Architecture:** Rate-of-Change (Delta)
""")

st.sidebar.divider()

# Backtest Performance Metrics (Dynamic JSON Ingestion)
st.sidebar.header("Backtest Validation")

try:
    with open('backtest_metrics.json', 'r') as f:
        metrics = json.load(f)

    st.sidebar.metric(label="Mean Absolute Percentage Error", value=metrics["mape"])

    st.sidebar.markdown(f"""
    **Training Period:** `Up to {metrics['train_end']}`

    **Testing Period (Blind):** `{metrics['test_start']} to {metrics['test_end']}`

    **Date Last Ran:** `{metrics['last_ran']}`
    """)

except FileNotFoundError:
    st.sidebar.warning(
        "⚠️ Backtest metrics not found. Run the `run_backtest()` function in `models.py` to generate validation data.")

st.sidebar.divider()

st.sidebar.markdown("### Champion Features")
st.sidebar.markdown("""
* `cass_shipments`
* `ppi_heavy_truck_cab_mfg`
* `industrial_production`
* `consumer_sentiment`
* `mfg_inventory_to_sales_ratio`
""")
