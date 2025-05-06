import requests
from geopy.distance import geodesic

import requests

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

def check_flood_alerts(lat, lon, api_key, days=4, rain_threshold=30.0):
    """
    Checks if there's a flood risk based on forecasted rainfall over the next `days`.
    Flood risk is flagged if total rainfall exceeds `rain_threshold` in mm.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            print("API error:", data)
            return False

        total_rainfall = 0.0
        forecasts = data.get("list", [])
        max_entries = days * 8  # 3-hour intervals (8 per day)

        for entry in forecasts[:max_entries]:
            rain_data = entry.get("rain", {})
            rainfall_3h = rain_data.get("3h", 0.0)
            total_rainfall += rainfall_3h

        total_rainfall = round(total_rainfall, 2)

        return total_rainfall >= rain_threshold

    except Exception as e:
        print("❌ Error checking flood risk:", e)
        return False

def is_near_water(lat, lon, threshold_km=2):
    # Build Overpass QL query to find water-related features including nodes, ways, and relations
    query = f"""
    [out:json];
    (
      node["natural"="water"](around:{int(threshold_km * 1000)},{lat},{lon});
      way["natural"="water"](around:{int(threshold_km * 1000)},{lat},{lon});
      relation["natural"="water"](around:{int(threshold_km * 1000)},{lat},{lon});

      node["waterway"](around:{int(threshold_km * 1000)},{lat},{lon});
      way["waterway"](around:{int(threshold_km * 1000)},{lat},{lon});
      relation["waterway"](around:{int(threshold_km * 1000)},{lat},{lon});

      node["landuse"="reservoir"](around:{int(threshold_km * 1000)},{lat},{lon});
      way["landuse"="reservoir"](around:{int(threshold_km * 1000)},{lat},{lon});
      relation["landuse"="reservoir"](around:{int(threshold_km * 1000)},{lat},{lon});
    );
    out body;
    """

    url = "https://overpass-api.de/api/interpreter"
    try:
        # Send the request with the properly encoded query
        response = requests.post(url, data={"data": query})
        response.raise_for_status()  # Check if the request was successful

        # Check if the response contains data
        data = response.json()
        # print(f"🔍 Nearby water elements found: {len(data.get('elements', []))}")  

        return bool(data.get("elements"))
    except requests.exceptions.RequestException as e:
        print(f"❌ Overpass API Error: {e}")
        return False


def get_features(lat, lon, api_key):
    return {
        "rain_mm": get_forecasted_rainfall(lat, lon, api_key),
        "has_alert": check_flood_alerts(lat, lon, api_key),
        "near_water": is_near_water(lat, lon)
    }
