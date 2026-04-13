import os
import time
import pandas as pd
from pathlib import Path
from fredapi import Fred
from dotenv import load_dotenv

# --- 1. Path Configuration ---
# Find the project root (3 levels up from this script)
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / '.env'
DATA_DIR = BASE_PATH / 'data'

# Ensure the data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 2. Environment & API Setup ---
load_dotenv(dotenv_path=ENV_PATH)
FRED_KEY = os.getenv("FRED_API_KEY")

if not FRED_KEY:
    raise ValueError("FRED_API_KEY not found. Check your .env file location.")

fred = Fred(api_key=FRED_KEY)

# --- 3. The Feature & Validator Dictionary ---
# Mapping the cryptic FRED IDs to clean, human-readable file names
SERIES_MAP = {
    # FAST INDICATORS
    'WEI': 'weekly_economic_index',
    'GASDESW': 'diesel_price',
    'RAILFRTINTERMODAL': 'rail_intermodal',
    'VIXCLS': 'vix_volatility',
    'T10Y2Y': 'yield_curve_spread',
    'ICSA': 'initial_jobless_claims',

    # MEDIUM INDICATORS
    'HOUST': 'housing_starts',
    'DGORDER': 'durable_goods_orders',
    'ADXTNO': 'durable_goods_ex_transport',
    'MANEMP': 'mfg_employment',
    'UMCSENT': 'consumer_sentiment',
    'PALUMUSDM': 'global_aluminum_price',
    'HTRUCKSSAAR': 'heavy_truck_sales',

    # SLOW INDICATORS
    'INDPRO': 'industrial_production',
    'TSIFRGHT': 'freight_tsi',
    'WPU101': 'ppi_iron_steel',
    'WPU102501': 'ppi_aluminum_shapes',
    'PCU336212336212': 'ppi_truck_mfg',
    'RETAILIRSA': 'inventory_to_sales_ratio',

    # VALIDATORS (TARGETS)
    'PCU4841214841212': 'target_ppi_dry_van',
    'PCU484122484122': 'target_ppi_ltl_reefer',
    'PCU484230484230': 'target_ppi_flatbed'
}


def fetch_and_save_data():
    """Iterates through the SERIES_MAP, fetches data, and saves to CSV."""
    print(f"Starting Data Ingestion. Saving to: {DATA_DIR}")
    print("-" * 50)

    for series_id, file_name in SERIES_MAP.items():
        try:
            print(f"Fetching: {file_name} ({series_id})...", end=" ")

            # Pull the data from FRED
            data = fred.get_series(series_id)

            # Convert to a clean DataFrame
            df = pd.DataFrame(data, columns=['value'])
            df.index.name = 'date'

            # Drop empty rows (some old FRED series have leading NaNs)
            df = df.dropna()

            # Save to the data/ folder
            output_path = DATA_DIR / f"{file_name}.csv"
            df.to_csv(output_path)

            print("SUCCESS")

            # RATE LIMITING: Sleep for 0.5 seconds to avoid being blocked by FRED
            time.sleep(0.5)

        except Exception as e:
            print(f"FAILED. Error: {e}")


if __name__ == "__main__":
    fetch_and_save_data()
    print("-" * 50)
    print("Ingestion Complete. Check the 'data/' folder.")