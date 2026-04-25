import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from pathlib import Path

# Corrected absolute imports based on the new project structure
from src.freight_market_sensing.feature_engineering.features import FeatureStore
from src.freight_market_sensing.feature_engineering.series import SERIES_MAP

BASE_PATH = Path(__file__).resolve().parent.parent.parent
SHAP_DIR = BASE_PATH / 'shap_charts'
SHAP_DIR.mkdir(parents=True, exist_ok=True)


def analyze_category(category_name: str, target_col: str):
    print("-" * 50)
    print(f"Loading Data for '{category_name}' SHAP Analysis...")
    store = FeatureStore()
    df = store.build_master_matrix()

    # 1. Dynamically get all feature names assigned to this category
    expected_features = [
        meta['name'] for meta in SERIES_MAP.values()
        if meta.get('category') == category_name
    ]

    # 2. Safety Check: Only use features that successfully loaded into the dataframe
    valid_features = [f for f in expected_features if f in df.columns]

    if not valid_features:
        print(f"Error: No features found in the master matrix for category '{category_name}'.")
        print("Skipping to next category...\n")
        return

    print(f"Found {len(valid_features)} features for '{category_name}':")
    for feature in valid_features:
        print(f" -> {feature}")

    # 3. Drop rows where we don't have target data or feature data
    ml_df = df.dropna(subset=[target_col] + valid_features).copy()
    X = ml_df[valid_features]
    y = ml_df[target_col]

    # 4. Train the mini-model for this specific category
    print("\nTraining Category Model...")
    model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X, y)

    # 5. Generate SHAP values
    print("Calculating SHAP Values (This takes a few seconds)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # 6. Generate and save the Plot
    print("Generating SHAP Summary Plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)

    # Add a title so you know what you are looking at
    plt.title(f"SHAP Analysis: {category_name}", fontsize=14, pad=20)
    plt.tight_layout()

    # Create a clean filename (e.g., 'shap_supply_chain_bullwhip.png')
    safe_category_name = category_name.lower().replace(' ', '_').replace('&', 'and')
    file_name = f'{SHAP_DIR}/shap_{safe_category_name}.png'

    plt.savefig(file_name)
    plt.close()  # Critical: Closes the plot so the next loop starts with a blank canvas

    print(f"Saved '{file_name}' to your project root!")
    print("-" * 50 + "\n")


if __name__ == "__main__":
    # The variable we are trying to predict
    target = 'trailer_production_volume'

    # The exact categories defined in your SERIES_MAP
    categories_to_test = [
        "Equipment Pricing",
        "Raw Materials",
        "Physical Output",
        "Supply Chain Bullwhip",
        "Macro Sentiment",
        "Carrier Pricing"
    ]

    # Run the tournament loop
    for category in categories_to_test:
        analyze_category(category_name=category, target_col=target)
