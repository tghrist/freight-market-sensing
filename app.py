import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Commercial Vehicle Demand Radar",
    page_icon="🚛",
    layout="wide"
)

# 2. Title and Executive Summary
st.title("Freight Market Sensing: 90-Day Commercial Vehicle Demand Forecast")
st.markdown("""
This application acts as a physics-based macroeconomic constraint for commercial equipment manufacturing. 
It filters out historical anomalies and regulatory pull-forwards to identify the true, sustainable 
macroeconomic baseline for trailer demand.
""")

st.divider()


# 3. Load the Data
# The @st.cache_data decorator ensures the app doesn't reload the CSV every time you click a button
@st.cache_data
def load_forecast_data():
    # Adjust this path if your app.py is in a different folder than your CSV
    df = pd.read_csv('live_90_day_forecast.csv', parse_dates=['date'])
    df.set_index('date', inplace=True)
    return df


try:
    forecast_df = load_forecast_data()

    # 4. Layout: Executive Metrics Row
    col1, col2, col3 = st.columns(3)

    with col1:
        # Get the latest forecasted index value
        latest_index = forecast_df['forecast_production_volume'].iloc[-1]
        st.metric(label="90-Day Target Index (2017=100)", value=f"{latest_index:.1f}")

    with col2:
        st.metric(label="Forecast Status", value="Stable / Flat")

    with col3:
        st.metric(label="Primary Market Driver", value="Cass Freight Shipments")

    st.divider()

    # 5. Layout: The Main Chart
    st.subheader("Master Capacity Plan: Baseline Projection")
    st.line_chart(forecast_df['forecast_production_volume'], color="#FF0000")

    st.caption(
        "Note: This baseline represents the macro-supported demand limit. Volume above this line should be treated as high-risk regulatory hedging.")

except FileNotFoundError:
    st.error("Forecast data not found. Please run the `models.py` export pipeline first.")

# 6. Sidebar for Navigation/Context
st.sidebar.header("Model Architecture")
st.sidebar.info("""
**Engine:** XGBoost Regressor  
**Horizon:** 90-Day Forward  
**Architecture:** Rate-of-Change (Delta)
""")
st.sidebar.markdown("### Champion Features")
st.sidebar.markdown("""
* `cass_shipments`
* `ppi_heavy_truck_cab_mfg`
* `industrial_production`
* `consumer_sentiment`
* `mfg_inventory_to_sales_ratio`
""")