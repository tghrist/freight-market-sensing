import streamlit as st

# Import the new UI components
from src.frontend.data_loader import load_data
from src.frontend.dashboard_tab import render_executive_dashboard
from src.frontend.explainability_tab import render_feature_explainability
from src.frontend.sidebar import render_sidebar

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

# 3. Load Data & Render Layout
try:
    history_df, forecast_df = load_data()

    # Layout: Tabs Configuration
    tab1, tab2 = st.tabs(["Executive Dashboard", "Model Explainability (Features)"])

    with tab1:
        render_executive_dashboard(history_df, forecast_df)

    with tab2:
        render_feature_explainability()

except FileNotFoundError:
    st.error("Data files not found. Please run the `models.py` export pipeline first.")

# 4. Render Sidebar
render_sidebar()