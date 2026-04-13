import os
from pathlib import Path
from dotenv import load_dotenv

base_path = Path(__file__).resolve().parent.parent.parent
env_path = base_path / '.env'

load_dotenv(dotenv_path=env_path)
fred_key = os.getenv("FRED_API_KEY")

print(f"Project Root: {base_path}")
print(f"Key loaded successfully: {fred_key is not None}")
