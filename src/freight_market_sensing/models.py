import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error

from src.freight_market_sensing.feature_engineering.features import FeatureStore


def run_backtest():
    print("-" * 50)
    print("Initializing S&OP Capacity Model (Delta Architecture)...")

    store = FeatureStore()
    df = store.build_master_matrix()

    features = [
        'ppi_heavy_truck_cab_mfg',
        'industrial_production',
        'mfg_inventory_to_sales_ratio',
        'consumer_sentiment',
        'cass_shipments'
    ]
    base_target = 'trailer_production_volume'

    # =======================================================
    # THE DELTA FIX: Predict the Rate of Change
    # Instead of absolute volume, predict the 90-day % change
    # =======================================================
    forecast_horizon_days = 90

    # 1. Calculate what the % change will be 90 days from now compared to today
    df['future_pct_change'] = (df[base_target].shift(-forecast_horizon_days) - df[base_target]) / df[base_target]

    # 2. Save today's raw volume so we can reconstruct the math later
    df['current_volume'] = df[base_target]

    target = 'future_pct_change'
    # =======================================================

    # Drop NaNs. We must include 'current_volume' in the drop so rows align perfectly
    ml_df = df[features + [target, 'current_volume', base_target]].dropna().copy()

    split_index = int(len(ml_df) * 0.8)

    train_df = ml_df.iloc[:split_index]
    test_df = ml_df.iloc[split_index:]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]  # This is the ACTUAL future % change

    print(f"Training on historical data up to: {train_df.index[-1].date()}")
    print(f"Testing blind forecast from: {test_df.index[0].date()} to {test_df.index[-1].date()}")

    print("\nTraining XGBoost Engine on Rate of Change...")
    model = xgb.XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    print("Generating Forecast...")
    predicted_deltas = model.predict(X_test)

    # Add predictions back to the test dataframe
    test_df = test_df.copy()
    test_df['predicted_delta'] = predicted_deltas

    # =======================================================
    # RECONSTRUCTION: Convert % Change back to Absolute Volume
    # Future Volume = Today's Volume * (1 + Predicted % Change)
    # =======================================================
    test_df['forecast_volume'] = test_df['current_volume'] * (1 + test_df['predicted_delta'])

    # Get the actual future volume for MAPE calculation
    actual_future_volume = test_df['current_volume'] * (1 + y_test)

    mape = mean_absolute_percentage_error(actual_future_volume, test_df['forecast_volume'])
    print(f"\nModel Performance:")
    print(f"MAPE (Mean Absolute Percentage Error): {mape:.2%}")

    print("\nGenerating Backtest Chart...")
    plt.figure(figsize=(14, 7))

    # Plot the historical baseline (using current_volume)
    plt.plot(train_df.index, train_df['current_volume'], label='Historical Actuals', color='lightgray', linewidth=2)

    # Plot the actual future production that happened during the test phase
    plt.plot(test_df.index, actual_future_volume, label='Actual Production (Test)', color='blue', linewidth=2)

    # Plot our reconstructed XGBoost forecast
    plt.plot(test_df.index, test_df['forecast_volume'], label='XGBoost Forecast (Reconstructed)', color='red',
             linestyle='--', linewidth=2)

    plt.axvline(x=train_df.index[-1], color='black', linestyle=':', label='Forecast Start')

    plt.title('S&OP Capacity Forecast Backtest: The Delta Architecture', fontsize=16, pad=15)
    plt.ylabel('Trailer Production Volume', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    file_name = '../../backtest_results.png'
    plt.savefig(file_name)
    plt.close()

    print(f"Saved '{file_name}' to your project root!")
    print("-" * 50 + "\n")


def generate_live_forecast():
    print("-" * 50)
    print("Generating Live 90-Day S&OP Forecast...")

    store = FeatureStore()
    df = store.build_master_matrix()

    features = [
        'ppi_heavy_truck_cab_mfg',
        'industrial_production',
        'mfg_inventory_to_sales_ratio',
        'consumer_sentiment',
        'cass_shipments'
    ]
    base_target = 'trailer_production_volume'

    forecast_horizon_days = 90

    # Calculate the % change for historical training
    df['future_pct_change'] = (df[base_target].shift(-forecast_horizon_days) - df[base_target]) / df[base_target]
    df['current_volume'] = df[base_target]

    target = 'future_pct_change'

    # =======================================================
    # THE PRODUCTION SPLIT
    # =======================================================
    # 1. Training Data: All historical rows where we know the future outcome (target is NOT NaN)
    train_df = df.dropna(subset=features + [target, 'current_volume']).copy()

    # 2. Live Data: The most recent 90 days. We have the features today, but the future target is NaN!
    live_df = df[df[target].isna()].dropna(subset=features + ['current_volume']).copy()

    print(f"Training model on {len(train_df)} historical records...")

    # Train the engine on 100% of historical data
    model = xgb.XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(train_df[features], train_df[target])

    print("Executing blind future forecast...")

    # Feed the most recent 90 days of features into the model
    live_df['predicted_delta'] = model.predict(live_df[features])

    # Reconstruct the absolute volumes for the future
    live_df['forecast_production_volume'] = live_df['current_volume'] * (1 + live_df['predicted_delta'])

    # =======================================================
    # DATE SHIFTING FOR EXPORT
    # Shift the dates forward 90 days so the export matches the actual future timeline
    # =======================================================
    live_df.index = live_df.index + pd.Timedelta(days=forecast_horizon_days)

    print(f"Forecast generated for: {live_df.index[0].date()} to {live_df.index[-1].date()}")

    # Format a clean export dataframe
    export_df = live_df[['forecast_production_volume']].round(0)  # Round to whole trailers

    # Save directly to your root directory for Power BI/Excel consumption
    export_filename = '../../live_90_day_forecast.csv'
    export_df.to_csv(export_filename)

    print(f"Success! Saved '{export_filename}' to your project root.")
    print("-" * 50 + "\n")


if __name__ == "__main__":
    # Comment out the backtest and run the live forecast!
    # run_backtest()
    generate_live_forecast()
