import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    # Load Forecast
    forecast_df = pd.read_csv('live_90_day_forecast.csv', parse_dates=['date'])
    forecast_df.set_index('date', inplace=True)

    # Load Historical Actuals
    history_df = pd.read_csv('historical_actuals.csv', parse_dates=['date'])
    history_df.set_index('date', inplace=True)

    # Load Features for the 3x2 Grid
    features_df = pd.read_csv('feature_history.csv', parse_dates=['date'])
    features_df.set_index('date', inplace=True)

    # Return all three dataframes
    return history_df, forecast_df, features_df

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