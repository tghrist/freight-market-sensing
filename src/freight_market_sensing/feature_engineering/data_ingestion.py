import os
import time
import pandas as pd
from pathlib import Path
from fredapi import Fred
from dotenv import load_dotenv
from series import SERIES_MAP

# --- 1. Path Configuration ---
# Find the project root (3 levels up from this script)
BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
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
def fetch_with_retry(series_id, max_retries=3):
    """Fetches data from FRED with exponential backoff for server errors."""
    for attempt in range(max_retries):
        try:
            data = fred.get_series(series_id)
            return data
        except Exception as e:
            error_msg = str(e)
            # If it's a server error, we wait and retry
            if "Internal Server Error" in error_msg or "500" in error_msg:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"[Server Hiccup] Retrying in {wait_time}s...", end=" ")
                time.sleep(wait_time)
            else:
                # If it's a 400 Bad Request, fail immediately
                raise e
    raise Exception("Max retries reached. FRED server is down.")


def fetch_and_save_data():
    """Iterates through the SERIES_MAP, fetches fresh data, and saves to CSV."""
    print(f"Starting Data Ingestion. Saving to: {DATA_DIR}")
    print("-" * 50)

    for series_id, meta in SERIES_MAP.items():
        if meta['source'] == 'FRED':
            file_name = meta['name']
            output_path = DATA_DIR / f"{file_name}.parquet"

            try:
                print(f"Fetching: {file_name} ({series_id})...", end=" ")

                # Use the robust retry logic
                data = fetch_with_retry(series_id)

                # Convert to a clean DataFrame
                df = pd.DataFrame(data, columns=['value'])
                df.index.name = 'date'

                # Drop empty rows
                df = df.dropna()

                # Save to the data/ folder (Overwrites existing for fresh data)
                df.to_parquet(output_path)
                print("SUCCESS")

                # RATE LIMITING
                time.sleep(0.5)

            except Exception as e:
                print(f"FAILED. Error: {e}")


if __name__ == "__main__":
    fetch_and_save_data()
    print("-" * 50)
    print("Ingestion Complete. Check the 'data/' folder.")
