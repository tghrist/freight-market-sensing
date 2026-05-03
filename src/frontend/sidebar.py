import streamlit as st
from src.frontend.data_loader import load_backtest_metrics

def render_sidebar():
    st.sidebar.header("Model Architecture")
    st.sidebar.info("""
        **Engine:** XGBoost Regressor  
        **Horizon:** 90-Day Forward  
        **Architecture:** Absolute Level (Tree-Based Thresholds)
        """)

    st.sidebar.divider()

    # Backtest Performance Metrics (Dynamic JSON Ingestion)
    st.sidebar.header("Backtest Validation")

    metrics = load_backtest_metrics()

    if metrics is not None:
        st.sidebar.metric(label="Mean Absolute Percentage Error", value=metrics["mape"])

        st.sidebar.markdown(f"""
        **Training Period:** `Up to {metrics['train_end']}`

        **Testing Period (Blind):** `{metrics['test_start']} to {metrics['test_end']}`

        **Date Last Ran:** `{metrics['last_ran']}`
        """)

    else:
        st.sidebar.warning(
            "⚠️ Backtest metrics not found. Run the `run_backtest()` function in `models.py` to generate validation data.")

    st.sidebar.divider()

    st.sidebar.markdown("### Predictive Model Inputs")
    st.sidebar.markdown("""
    * [Cass Shipments](https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes/cass-freight-index)
    * [PPI: Heavy Truck Cabs](https://fred.stlouisfed.org/series/PCU336120336120)
    * [Industrial Production](https://fred.stlouisfed.org/series/INDPRO)
    * [Consumer Sentiment](https://fred.stlouisfed.org/series/UMCSENT)
    * [Mfg Inventory-to-Sales](https://fred.stlouisfed.org/series/MNFCTRIRSA)
    """)