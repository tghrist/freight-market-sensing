import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Corrected absolute import based on your project structure
from src.freight_market_sensing.feature_engineering.features import FeatureStore
from src.config import CHAMPION_FEATURES, ACTIVE_TARGET


def analyze_champion_correlation():
    print("-" * 50)
    print("Loading Data for Final Correlation Check...")
    store = FeatureStore()
    df = store.build_master_matrix()

    # The Final "Dream Team" Roster + The Target Variable (Dynamically loaded from config)
    champions = list(CHAMPION_FEATURES.keys()) + [ACTIVE_TARGET]

    # Safety Check: Ensure all champions are in the master matrix
    missing_cols = [col for col in champions if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns in master matrix: {missing_cols}")
        print("Please check data_ingestion.py and run it again.")
        return

    # Isolate the dataframe and drop NaNs to ensure the math aligns on the exact same dates
    ml_df = df[champions].dropna().copy()

    # Calculate Pearson correlation using your built-in FeatureStore method
    print("Calculating Pearson Correlation Matrix...")
    corr_matrix = store.correlation_check(ml_df)

    # Generate the Heatmap Plot
    print("Generating Heatmap...")
    plt.figure(figsize=(12, 10))

    # Create a mask to hide the upper triangle (removes duplicate squares for a cleaner chart)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # Draw the heatmap using seaborn
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,  # Show the actual R value numbers
        fmt=".2f",  # Round to 2 decimal places
        cmap='coolwarm',  # Red for positive correlation, Blue for negative
        vmin=-1,  # Lock scale bottom at -1
        vmax=1,  # Lock scale top at +1
        square=True,
        linewidths=.5
    )

    plt.title("S&OP Roster Validation: Champion Feature Correlation", fontsize=16, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    file_name = '../../champion_correlation.png'
    plt.savefig(file_name)
    plt.close()

    print(f"Saved '{file_name}' to your project root!")
    print("-" * 50 + "\n")


if __name__ == "__main__":
    analyze_champion_correlation()