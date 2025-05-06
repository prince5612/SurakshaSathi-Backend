# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from app.ml_model.travel.utils import (
    compute_trip_duration,
    get_transport_multiplier,
    get_forecasted_rainfall,
    get_current_aqi,
    estimate_weather_risk,
    get_crime_index_by_lat_lon
)
import os
from geopy.geocoders import Nominatim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from dotenv import load_dotenv

load_dotenv()

# Load the dataset
df = pd.read_csv("Static/travel_insurance_dataset_india.csv")

# Select features and target based on actual columns
X = df[["duration", "crime_index", "aqi", "weather_risk", "transport_multiplier"]]
y = df["total_premium"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)



TOKEN = os.getenv("API_KEY")


def travel_predict_premium(data):
    try:
        start_date = data["start_date"]
        end_date = data["end_date"]
        lat,lon=  get_lat_long(data["city"])
        transport_mode = data["transport_mode"]

        # Compute derived features
        duration = compute_trip_duration(start_date, end_date)
        transport_multiplier = get_transport_multiplier(transport_mode)
        rainfall = get_forecasted_rainfall(lat, lon, TOKEN)
        aqi = get_current_aqi(lat, lon, TOKEN)
        weather_risk = estimate_weather_risk(aqi, rainfall)
        state, crime_index = get_crime_index_by_lat_lon(lat, lon)

        X_input = pd.DataFrame([{
            "duration": duration,
            "crime_index": crime_index,
            "aqi": aqi,
            "weather_risk": weather_risk,
            "transport_multiplier": transport_multiplier
        }])
        predicted_premium = model.predict(X_input)[0]
        print(predicted_premium)

        return jsonify({
            "duration_days": duration,
            "aqi": aqi,
            "rainfall_mm": rainfall,
            "weather_risk": weather_risk,
            "state": state,
            "crime_index": crime_index,
            "predicted_premium": round(predicted_premium, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400



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
