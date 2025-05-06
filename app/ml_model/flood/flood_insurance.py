from flask import Flask, request, jsonify
from app.ml_model.flood.utils import get_features
import pandas as pd
from geopy.geocoders import Nominatim
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from dotenv import load_dotenv

# Load WAQI_TOKEN from .env
load_dotenv()
TOKEN = os.getenv("API_KEY")
BASE_PREMIUM = float(os.getenv("BASE_PREMIUM"))


# Load trained ML model
# model = joblib.load("app/ml_model/flood/flood_model.pkl")
# Load dataset
df = pd.read_csv("Static/flood_insurance_data.csv")

# Features and target
X = df[['rain_mm', 'has_alert', 'near_water', 'lat', 'lon']]
y = df['flood_multiplier']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


def flood_predict_premium(data):
    # data = request.json
    lat,lon=get_lat_long(data["city"])
    

    if not all([lat, lon, BASE_PREMIUM, TOKEN]):
        return jsonify({"error": "Missing parameters"}), 400

    features = get_features(lat, lon, TOKEN)
    print(features["rain_mm"])
    print(features["has_alert"])
    print(features["near_water"])
    features["lat"] = lat
    features["lon"] = lon

    X = pd.DataFrame([{
        "rain_mm": features["rain_mm"],
        "has_alert": int(features["has_alert"]),
        "near_water": int(features["near_water"]),
        "lat": lat,
        "lon": lon
    }])
    predicted = model.predict(X)[0]
    final_premium = round(BASE_PREMIUM * predicted, 2)

    return jsonify({
        "rain_mm": features["rain_mm"],
        "has_alert": int(features["has_alert"]),
        "near_water": int(features["near_water"]),
        "lat": lat,
        "lon": lon,
        "predicted_premium": final_premium
    })


def get_lat_long(city_name):
    """
    Get latitude and longitude of a city by its name.
    :param city_name: Name of the city.
    :return: Tuple (latitude, longitude) or None if not found.
    """
    geolocator = Nominatim(user_agent="city_lat_long_finder")
    location = geolocator.geocode(city_name)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# if __name__ == "__main__":
#     app.run(debug=True)
