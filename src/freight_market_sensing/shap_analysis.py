import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from features import FeatureStore


def analyze_correlation():
    print("Loading Data for SHAP Analysis...")
    store = FeatureStore()
    df = store.build_master_matrix()

    target_col = 'trailer_production_volume'

    # Use the exact top features from your latest run
    top_features = [
        'heavy_truck_sales',
        'ppi_heavy_truck_cab_mfg',
        'target_ppi_dry_van',
        'global_aluminum_price',
        'mfg_employment'
    ]

    ml_df = df.dropna(subset=[target_col]).copy()
    X = ml_df[top_features]
    y = ml_df[target_col]

    print("Training Model...")
    model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X, y)

    print("Calculating SHAP Values (This takes a few seconds)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    print("Generating SHAP Summary Plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig('../../shap_correlation.png')
    print("Saved 'shap_correlation.png' to your project root!")


if __name__ == "__main__":
    analyze_correlation()