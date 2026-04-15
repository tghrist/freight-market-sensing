import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from features import FeatureStore


def rank_features():
    print("Loading Master Matrix...")
    store = FeatureStore()
    df = store.build_master_matrix()

    print("-" * 50)

    print("Preparing Data for Trailer Demand Ranking...")

    # 1. NEW TARGET: Trailer Production Volume
    target_col = 'trailer_production_volume'

    # Drop the target, the raw Cass components, and the other target (truck sales)
    features_to_drop = [
        'cass_shipments',
        'cass_expenditures',
        'heavy_truck_sales',
        target_col
    ]

    # 2. Clean the data for the training run
    ml_df = df.dropna(subset=[target_col]).copy()

    X = ml_df.drop(columns=features_to_drop, errors='ignore')
    y = ml_df[target_col]

    print(f"Analyzing {len(X.columns)} features against {target_col}...")

    # 3. Initialize and train a basic XGBoost Regressor
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
    model.fit(X, y)

    # 4. Extract Feature Importances
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("\nTop 5 Most Influential Features for Truck Sales:")
    print(importance_df.head(5).to_string(index=False))

    # 5. Plot the results visually
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df, hue='Feature', palette='magma', legend=False)
    plt.title('Macroeconomic Drivers of Trailer Sales', fontsize=16)
    plt.xlabel('XGBoost Relative Feature Importance', fontsize=12)
    plt.ylabel('Economic Indicator', fontsize=12)
    plt.tight_layout()

    plt.savefig('../../trailer_sales_drivers.png')
    print("\nVisual saved as 'truck_sales_drivers.png' in your project root.")


if __name__ == "__main__":
    rank_features()