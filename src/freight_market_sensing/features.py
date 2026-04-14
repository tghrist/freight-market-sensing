import pandas as pd
from pathlib import Path


class FeatureStore:
    def __init__(self):
        # Dynamically find the data directory
        self.base_path = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_path / 'data'

        if not self.data_dir.exists():
            raise FileNotFoundError("Data directory not found. Run data_ingestion.py first.")

    def load_and_merge(self) -> pd.DataFrame:
        """Reads all Parquet files and merges them into a single timeline."""
        print("Loading and merging Parquet files...")
        master_df = pd.DataFrame()

        # Iterate through every .parquet file in the directory
        for file_path in self.data_dir.glob("*.parquet"):
            feature_name = file_path.stem  # e.g., 'diesel_price'

            # Load the file
            df = pd.read_parquet(file_path)

            # Rename the generic 'value' column to the actual feature name
            df = df.rename(columns={'value': feature_name})

            # Merge into the master dataframe
            if master_df.empty:
                master_df = df
            else:
                # Outer join ensures we don't lose any dates (Weekly or Monthly)
                master_df = pd.merge(master_df, df, on='date', how='outer')

        # Sort chronologically from oldest to newest
        master_df = master_df.sort_index()
        return master_df

    def engineer_business_logic(self, df) -> pd.DataFrame:
        """Applies S&OP specific formulas to the raw data."""
        print("Engineering custom S&OP targets and features...")

        # 1. The Target: Cass Inferred Rate (Cost per shipment)
        if 'cass_expenditures' in df.columns and 'cass_shipments' in df.columns:
            df['target_cass_inferred_rate'] = df['cass_expenditures'] / df['cass_shipments']

        # 2. The Bullwhip Feature: Retail vs Total Inventory Spread
        if 'retail_inventory_to_sales_ratio' in df.columns and 'total_inventory_to_sales_ratio' in df.columns:
            df['feature_retail_inventory_spread'] = (
                    df['retail_inventory_to_sales_ratio'] - df['total_inventory_to_sales_ratio']
            )

        return df

    def align_time_series(self, df) -> pd.DataFrame:
        """Handles missing data caused by weekly vs. monthly reporting."""
        print("Aligning multi-speed time series data...")

        # Forward Fill: If a monthly number comes out on Jan 1st,
        # assume that number remains the active "truth" for every week until Feb 1st.
        df = df.ffill()

        # Drop early history where the Federal Reserve wasn't tracking certain metrics yet
        # (e.g., stopping the dataset from starting in 1940 with 90% blank columns)
        df = df.dropna()

        return df

    def build_master_matrix(self) -> pd.DataFrame:
        """The main pipeline method that executes all steps."""
        df = self.load_and_merge()
        df = self.engineer_business_logic(df)
        df = self.align_time_series(df)

        print(f"Pipeline Complete! Master Matrix Shape: {df.shape}")
        return df


if __name__ == "__main__":
    # Initialize the class
    store = FeatureStore()

    # Run the pipeline
    master_matrix = store.build_master_matrix()

    # Display the last 5 rows to verify it worked
    print("\n--- Latest Market Data ---")
    print(master_matrix[['diesel_price', 'feature_retail_inventory_spread', 'target_cass_inferred_rate']].tail())