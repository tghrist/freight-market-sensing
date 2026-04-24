import pandas as pd
from pathlib import Path
from src.freight_market_sensing.feature_engineering.series import SERIES_MAP


class FeatureStore:
    def __init__(self):
        # Dynamically find the data directory
        self.base_path = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_path / 'data'

        if not self.data_dir.exists():
            raise FileNotFoundError("Data directory not found. Run data_ingestion.py first.")

    def load_and_merge(self, category) -> pd.DataFrame:
        """Reads all Parquet files and merges them into a single timeline."""
        print("Loading and merging Parquet files...")
        master_df = pd.DataFrame()

        valid_features = [
            meta['name'] for meta in SERIES_MAP.values()
            if meta['category'] == category
        ]

        # Iterate through every .parquet file in the directory
        for file_path in self.data_dir.glob("*.parquet"):
            feature_name = file_path.stem  # e.g., 'diesel_price'

            if feature_name not in valid_features:
                continue

            # Load the file
            df = pd.read_parquet(file_path)

            # =======================================================
            # RESILIENT DATE HANDLING
            # =======================================================
            # 1. If 'date' isn't a column, check if it's trapped in the index
            if 'date' not in df.columns and 'observation_date' not in df.columns:
                df = df.reset_index()

            # 2. Standardize all column names to lowercase to catch 'Date' or 'DATE'
            df.columns = [col.lower() for col in df.columns]

            # 3. If FRED named it 'observation_date', rename it to 'date'
            if 'observation_date' in df.columns:
                df = df.rename(columns={'observation_date': 'date'})
            # =======================================================

            # Ensure 'date' is a proper datetime object
            df['date'] = pd.to_datetime(df['date'])

            # For all standard features, just rename the generic 'value' column
            df = df.rename(columns={'value': feature_name})

            # Merge into the master dataframe
            if master_df.empty:
                master_df = df
            else:
                # Outer join ensures we don't lose any dates (Weekly or Monthly)
                master_df = pd.merge(master_df, df, on='date', how='outer')

        # Set the date as the true index and sort chronologically
        master_df = master_df.set_index('date').sort_index()
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

        # =======================================================
        # DJTA INTERCEPTION: Convert Daily Stock Data to Weekly
        # =======================================================
        if 'dow_jones_transportation_avg' in df.columns:
            print("Intercepting DJTA: Downsampling from Daily to Weekly (Friday)...")

            # Create different resampling features
            df['djta_mean'] = df['dow_jones_transportation_avg'].resample('W-FRI').mean()
            df['djta_vol'] = df['dow_jones_transportation_avg'].resample('W-FRI').std()
            df['djta_last'] = df['dow_jones_transportation_avg'].resample('W-FRI').last()

        df.to_clipboard()
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
    
    def correlation_check(self, df) -> pd.DataFrame:
        """Compares all features to eachother returning a matrix of correlation (r) values."""
        print("Checking feature correlation...")

        corr_df = df.corr(method='pearson')

        return corr_df

    def build_master_matrix(self, category=None) -> pd.DataFrame:
        """The main pipeline method that executes all steps."""
        df = self.load_and_merge(category)
        df = self.engineer_business_logic(df)
        df = self.align_time_series(df)

        print(f"Pipeline Complete! Master Matrix Shape: {df.shape}")
        return df


if __name__ == "__main__":
    # Initialize the class
    store = FeatureStore()

    # Run the pipeline
    master_matrix = store.build_master_matrix(category='Macro Sentiment')

    # Display the last 5 rows to verify it worked
    # print("\n--- Latest Market Data ---")
    # print(master_matrix[['diesel_price', 'feature_retail_inventory_spread', 'target_cass_inferred_rate']].tail())