import requests
from datetime import datetime
import pandas as pd

crime_df = pd.read_csv("Static/india_state_crime_index.csv")

# --- Transport multipliers ---
TRANSPORT_MULTIPLIERS = {
    "flight": 1.5,
    "train": 1.2,
    "bus": 1.0,
    "car": 1.1,
    "bike": 0.9,
    "walk":0.8
}

def compute_trip_duration(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        duration = (end_date - start_date).days
        return max(duration, 1)
    except Exception as e:
        raise ValueError(f"Invalid date format: {e}")

def get_transport_multiplier(mode):
    return TRANSPORT_MULTIPLIERS.get(mode.lower(), 1.0)

def get_forecasted_rainfall(lat, lon, api_key, days=4):
    try:
        # Updated endpoint with lat/lon
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            print("API error:", data)
            return 0

        total_rainfall = 0.0
        forecasts = data.get("list", [])

        # Only get data for the next `days` days (~8 records per day)
        max_entries = days * 8
        for entry in forecasts[:max_entries]:
            rain_data = entry.get("rain", {})
            rainfall_3h = rain_data.get("3h", 0.0)
            total_rainfall += rainfall_3h

        return round(total_rainfall, 2)

    except Exception as e:
        print("Error getting forecasted rainfall:", e)
        return 0

def get_current_aqi(lat, lon, api_key):
    """
    Fetch current AQI value using OpenWeatherMap Air Pollution API.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["list"][0]["main"]["aqi"] * 50  # OWM AQI levels: 1–5. Map to ~0–250
    except Exception as e:
        print(f"❌ AQI fetch error: {e}")
        return 100  # default moderate value

def estimate_weather_risk(aqi, rainfall_mm):
    """
    Simple function to return a weather risk score (scale 1-5).
    """
    if aqi > 200 or rainfall_mm > 150:
        return 5
    elif aqi > 150 or rainfall_mm > 100:
        return 4
    elif aqi > 100 or rainfall_mm > 50:
        return 3
    elif aqi > 50 or rainfall_mm > 20:
        return 2
    else:
        return 1
def get_state_from_lat_lon(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    headers = {"User-Agent": "Crime-Index-App"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if "address" in data and "state" in data["address"]:
        return data["address"]["state"]
    return None

def get_crime_index_by_lat_lon(lat, lon):
    state = get_state_from_lat_lon(lat, lon)
    if not state:
        return None, "State not found from coordinates"

    row = crime_df[crime_df["State"].str.lower() == state.lower()]
    if row.empty:
        return state, None
    crime_index = row.iloc[0]["Crime_Index"]
    return state, crime_index