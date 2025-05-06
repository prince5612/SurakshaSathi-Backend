# aqi_service.py
import os
import requests
from dotenv import load_dotenv

# Load WAQI_TOKEN from .env
load_dotenv()
TOKEN = os.getenv("WAQI_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set WAQI_TOKEN in your .env")

def get_aqi(lat: float, lon: float) -> int:
    """Fetch AQI from WAQI for given coordinates."""
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={TOKEN}"
    resp = requests.get(url, timeout=5)
    data = resp.json()
    if data.get("status") != "ok":
        raise ValueError(f"WAQI API error: {data.get('data')}")
    return int(data["data"]["aqi"])

if __name__ == "__main__":
    # Quick test
    lat, lon = 22.30, 73.19
    print(f"AQI at {lat},{lon} =", get_aqi(lat, lon))
