import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt

# Import your centralized config and feature store
from src.freight_market_sensing.feature_engineering.features import FeatureStore
from src.config import CHAMPION_FEATURES, ACTIVE_TARGET


def generate_waterfall_plot(target_date: str):
    print("-" * 50)
    print(f"Generating SHAP Waterfall Plot for Forecast Date: {target_date}")

    # 1. Load Data
    store = FeatureStore()
    df = store.build_master_matrix()

    champions = list(CHAMPION_FEATURES.keys())

    # Make sure we have the features and target
    ml_df = df[champions + [ACTIVE_TARGET]].dropna().copy()

    X = ml_df[champions]
    y = ml_df[ACTIVE_TARGET]

    # 2. Train the Model
    # (We train on the whole dataset to build the decision trees)
    print("Training XGBoost Model...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X, y)

    # 3. Find the specific row for our target date
    # Convert string to datetime to match index
    target_dt = pd.to_datetime(target_date)

    # Let's find the closest date in the index if the exact one doesn't exist
    if target_dt not in X.index:
        closest_date = X.index[X.index.get_indexer([target_dt], method='nearest')[0]]
        print(f"Exact date {target_date} not found. Using closest date: {closest_date.strftime('%Y-%m-%d')}")
        target_dt = closest_date

    row_index = X.index.get_loc(target_dt)

    # 4. Calculate SHAP Values
    print("Calculating SHAP values...")
    explainer = shap.Explainer(model)
    shap_values = explainer(X)

    # 5. Generate the Waterfall Plot
    print("Drawing Plot...")
    plt.figure(figsize=(10, 6))

    # Plot the specific row
    shap.plots.waterfall(
        shap_values[row_index],
        max_display=6,  # Show all our champions
        show=False  # Prevent it from blocking the script
    )

    plt.title(f"Forecast Dissection: {target_dt.strftime('%B %Y')}", fontsize=16, pad=20)
    plt.tight_layout()

    file_name = f'../../waterfall_{target_dt.strftime("%Y_%m")}.png'
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()

    print(f"\nFinal Model Prediction for this date: {model.predict(X.iloc[[row_index]])[0]:.2f}")
    print(f"Saved Waterfall Plot to {file_name}")
    print("-" * 50)


if __name__ == "__main__":
    # Change this date to the exact month you want to dissect!
    # Format: 'YYYY-MM-DD'
    DATE_TO_ANALYZE = '2026-07-23'

    generate_waterfall_plot(DATE_TO_ANALYZE)
