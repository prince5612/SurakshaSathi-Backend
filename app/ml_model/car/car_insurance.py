# import os

# import requests
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from dotenv import load_dotenv
# from pymongo import MongoClient
# from urllib.parse import urlparse
# import urllib.parse
# load_dotenv()

# # 1) Load CSV
# username = os.getenv('MONGO_USER')
# password = os.getenv('MONGO_PASSWORD')
# # URL-encode username and password
# username_esc = urllib.parse.quote_plus(username)
# password_esc = urllib.parse.quote_plus(password)
# MONGO_URI = f"mongodb+srv://{username_esc}:{password_esc}@surakshasathi.d2azkdd.mongodb.net/?retryWrites=true&w=majority&appName=SurakshaSathi"

# if not MONGO_URI:
#     raise RuntimeError("MONGODB_URI environment variable is required")
# client = MongoClient(MONGO_URI)
# db=client["SurkshaSathi"]
# driver_score = db["driver_score"]

# df = pd.read_csv("Static/car_driver_dataset_with_premium.csv")

# # 2) Preprocess
# df['manufacturer_date'] = pd.to_datetime(df['manufacturer_date']).map(lambda d: d.toordinal())
# weather_le = LabelEncoder()
# df['weather'] = weather_le.fit_transform(df['weather'])

# # 3) Features & target
# X = df.drop(columns=['device_id', 'yearly_premium_rupees'])
# y = df['yearly_premium_rupees']

# # 4) Train/Test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # 5) Train RandomForest
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # 6) Evaluate
# y_pred = model.predict(X_test)
# # print("MAE:", round(mean_absolute_error(y_test, y_pred), 2))
# # print("MSE:", round(mean_squared_error(y_test, y_pred), 2))
# # print("R² :", round(r2_score(y_test, y_pred), 3))





# # 1) Sign up at https://openweathermap.org/api and set your API key
# #    e.g. export OWM_API_KEY="your_actual_key"
# OWM_API_KEY = os.getenv("OWM_API_KEY")
# if not OWM_API_KEY:
#     raise RuntimeError("Please set the OWM_API_KEY environment variable")

# # 2) Mapping from OpenWeatherMap 'main' categories to your buckets
# _weather_map = {
#     "Thunderstorm": "rain",
#     "Drizzle":      "rain",
#     "Rain":         "rain",
#     "Snow":         "rain",   # treat snow as “rain” bucket, or handle separately if you like
#     "Mist":         "fog",
#     "Smoke":        "fog",
#     "Haze":         "fog",
#     "Dust":         "fog",
#     "Fog":          "fog",
#     "Sand":         "fog",
#     "Ash":          "fog",
#     "Squall":       "rain",
#     "Tornado":      "rain",
#     "Clear":        "sunny",
#     "Clouds":       "sunny"   # you could split “few clouds” vs “overcast” if desired
# }

# def get_weather_category(city_name: str) -> str:
#     """
#     Fetch current weather for `city_name` from OpenWeatherMap,
#     then classify into 'fog', 'rain', or 'sunny'.
#     """
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city_name,
#         "appid": OWM_API_KEY,
#         "units": "metric"
#     }
#     resp = requests.get(url, params=params, timeout=5)
#     resp.raise_for_status()
#     data = resp.json()
    
#     # The API returns a list under "weather"; we take the first element's "main" field
#     main = data["weather"][0]["main"]
    
#     # Map it into our three categories (default to "sunny" if unknown)
#     return _weather_map.get(main, "sunny")


# # ——— Example usage ———
# # if __name__ == "__main__":
# #     for city in ["Mumbai", "London", "New York", "Beijing"]:
# #         cat = get_weather_category(city)
# #         print(f"{city:10s} → {cat}")

# # Directly call predict_premium without main guard

# w=get_weather_category("Beijing")
# print(w)
# sample = {
#     'manufacturer_date': '2019-09-15',
#     'car_price_lakhs': 7.5,
#     'weather':w,
#     'user_age': 55,
#     'driver_score': 90
# }

# # Function definition

# # def predict_premium(input_data: dict) -> float:
# #     """
# #     Predict yearly premium (₹) for one car/driver record.
# #     input_data keys:
# #       - manufacturer_date: 'YYYY-MM-DD'
# #       - car_price_lakhs: float
# #       - weather: one of 'rain','fog','snow','sunny'
# #       - user_age: int
# #       - driver_score: int (0–100)
# #     """
# #     # copy so we don’t mutate the original
# #     data = input_data.copy()
# #     w=get_weather_category(data["city"])
# #     pipeline = [
# #     { "$group": { "_id": None, "avgScore": { "$avg": "$score" } } }
# #     ]
# #     result = list(driver_score.aggregate(pipeline))
# #     if not result:
# #         raise ValueError("No documents in driver_score collection")
# #     avg_score = result[0]["avgScore"]
# #     print(f"Fetched average driver_score = {avg_score:.2f}")

   
# #     # encode date
# #     data['manufacturer_date'] = pd.to_datetime(data['manufacturer_date']).toordinal()
# #     # encode weather
# #     w = weather_le.transform(w)[0]
    
# #     # build DataFrame
# #     input_df = pd.DataFrame([data["manufacturer_date"],data["car_price_lakhs"],w,data["user_age"]],avg_score)
# #     # predict
# #     pred = model.predict(input_df)[0]
# #     return round(pred, 2)

# def predict_premium(input_data: dict):
#     """
#     Predict yearly premium (₹) for one car/driver record and return a Flask-compatible response.
#     Required input_data keys:
#       - manufacturer_date: 'YYYY-MM-DD'
#       - car_price_lakhs: float
#       - user_age: int
#     One of:
#       - weather: 'rain','fog','snow','sunny'
#       - city: to fetch weather

#     Returns:
#       - dict or (dict, status_code)
#     """
#     # 1) Determine weather
#     if 'city' in input_data:
#         input_data['weather'] = get_weather_category(input_data['city'])
#     if 'weather' not in input_data:
#         return {"error": "Must provide 'weather' or 'city'"}, 400

#     # 2) Fetch average driver_score from MongoDB
#     pipeline = [{"$group": {"_id": None, "avgScore": {"$avg": "$score"}}}]
#     res = list(driver_score.aggregate(pipeline))
#     if not res:
#         return {"error": "No driver_score data"}, 500
#     avg_score = res[0]["avgScore"]
#     print(avg_score)
#     # 3) Encode features
#     ord_date = pd.to_datetime(input_data['manufacturer_date']).toordinal()
#     weather_val = weather_le.transform([input_data['weather']])[0]
#     features = {
#         'manufacturer_date': ord_date,
#         'car_price_lakhs':   input_data['car_price_lakhs'],
#         'user_age':          input_data['user_age'],
#         'driver_score':      avg_score,
#         'weather':           weather_val
#     }

#     # 4) Create DataFrame row
#     df_row = pd.DataFrame([features], columns=X_train.columns)

#     # 5) Predict
#     premium = model.predict(df_row)[0]
#     print(premium)
#     return {"yearly_premium": float(round(premium, 2))}

# # Direct call
# # predicted_premium = predict_premium(sample)
# # print(f"Predicted yearly premium: ₹{predicted_premium}")

import os
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse

# Load environment
load_dotenv()

# --- MongoDB connection ---
username = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')
username_esc = urllib.parse.quote_plus(username)
password_esc = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://{username_esc}:{password_esc}@surakshasathi.d2azkdd.mongodb.net/?retryWrites=true&w=majority&appName=SurakshaSathi"
client = MongoClient(MONGO_URI)
db = client["SurkshaSathi"]
driver_score_coll = db["driver_score"]

# --- Load & train model ---

df = pd.read_csv("Static/car_driver_dataset_with_premium.csv")
df['manufacturer_date'] = pd.to_datetime(df['manufacturer_date']).map(lambda d: d.toordinal())
weather_le = LabelEncoder()
df['weather'] = weather_le.fit_transform(df['weather'])
X = df.drop(columns=['device_id', 'yearly_premium_rupees'])
y = df['yearly_premium_rupees']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Weather classification helper ---
OWM_API_KEY = os.getenv("OWM_API_KEY")
_weather_map = {
    "Thunderstorm": "rain", "Drizzle": "rain", "Rain": "rain", "Snow": "rain",
    "Mist": "fog", "Smoke": "fog", "Haze": "fog", "Dust": "fog", "Fog": "fog",
    "Sand": "fog", "Ash": "fog", "Squall": "rain", "Tornado": "rain",
    "Clear": "sunny", "Clouds": "sunny"
}

def get_weather_category(city_name: str) -> str:
    """
    Fetch current weather for `city_name` and map to 'rain','fog', or 'sunny'.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": OWM_API_KEY, "units": "metric"}
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    main = resp.json()["weather"][0]["main"]
    return _weather_map.get(main, "sunny")

# # --- Premium prediction function ---
# def predict_premium(input_data: dict):
#     """
#     Given input_data with keys:
#       - manufacturer_date: 'YYYY-MM-DD'
#       - car_price_lakhs: float
#       - user_age: int
#     And either:
#       - 'weather': one of 'rain','fog','snow','sunny'
#       - 'city': city name string to fetch weather
#     Returns:
#       dict {"yearly_premium": float} or (dict, status_code) on error.
#     """
#     # Determine weather
#     if 'city' in input_data:
#         input_data['weather'] = get_weather_category(input_data['city'])
#     if 'weather' not in input_data:
#         return {"error": "Must provide 'weather' or 'city'"}, 400

#     print(input_data["weather"])
#     # Fetch average driver score
#     pipeline = [{"$group": {"_id": None, "avgScore": {"$avg": "$score"}}}]
#     res = list(driver_score_coll.aggregate(pipeline))
#     if not res:
#         return {"error": "No driver_score data"}, 500
#     avg_score = res[0]["avgScore"]
#     print(avg_score)

#     # Encode features
#     ord_date = pd.to_datetime(input_data['manufacturer_date']).toordinal()
#     weather_val = weather_le.transform([input_data['weather']])[0]
#     features = {
#         'manufacturer_date': ord_date,
#         'car_price_lakhs':   input_data['car_price_lakhs'],
#         'user_age':          input_data['user_age'],
#         'driver_score':      avg_score,
#         'weather':           weather_val
#     }
#     df_row = pd.DataFrame([features], columns=X_train.columns)

#     # Predict
#     premium = model.predict(df_row)[0]
#     print(premium)
#     return {"predicted_premium": float(round(premium, 2))}

def predict_premium(input_data: dict):
    """
    Given input_data with keys:
      - manufacturer_date: 'YYYY-MM-DD'
      - car_price_lakhs: float
      - user_age: int
      - device_id: string
    And either:
      - 'weather': one of 'rain','fog','snow','sunny'
      - 'city': city name string to fetch weather
    Returns JSON-safe dict:
      {
        "predicted_premium": float,
        "features": {
           "manufacturer_date": int,
           "car_price_lakhs": float,
           "user_age": int,
           "driver_score": float,
           "weather": int
        }
      }
    Or (dict, status_code) on error.
    """
    # require device_id
    device_id = input_data.get("device_id")
    if not device_id:
        return {"error": "Must provide 'device_id'"}, 400

    # determine weather if needed
    if "city" in input_data:
        input_data["weather"] = get_weather_category(input_data["city"])
    if "weather" not in input_data:
        return {"error": "Must provide 'weather' or 'city'"}, 400

    # compute average driver score for this device
    pipeline = [
        {"$match": {"device_id": device_id}},
        {"$group": {"_id": None, "avgScore": {"$avg": "$score"}}}
    ]
    res = list(driver_score_coll.aggregate(pipeline))
    if not res:
        return {"error": f"No driver_score data for device_id={device_id}"}, 404

    # cast avgScore to Python float
    avg_score = float(res[0]["avgScore"])

    # encode features
    # ensure ord_date is Python int
    ord_date = int(pd.to_datetime(input_data["manufacturer_date"]).toordinal())
    # label‑encoder returns a numpy.int64 – cast to int
    weather_val = int(weather_le.transform([input_data["weather"]])[0])

    # build a pure‑Python features dict
    features = {
        "manufacturer_date": ord_date,
        "car_price_lakhs": float(input_data["car_price_lakhs"]),
        "user_age": int(input_data["user_age"]),
        "driver_score": avg_score,
        "weather": weather_val
    }

    # build DataFrame row in correct column order
    df_row = pd.DataFrame([features], columns=X_train.columns)

    # predict (model may return numpy type)
    premium = model.predict(df_row)[0]
    premium_py = float(round(premium, 2))

    # return only native Python types
    return {
        "predicted_premium": premium_py,
        "features": features
    }




from app.ml_model.car.driver_score import ingest_gps_point, compute_driver_score, compute_premium, user_events, user_points
from flask import Flask, request, jsonify

gps_logs = []

def receive_gps():
    data = request.get_json(force=True)
    # validate required fields
    for key in ("device_id", "ts", "lat", "lon", "speed_kmh"):
        if key not in data or data[key] is None:
            return jsonify({"error": f"Missing field {key}"}), 400

    device_id = data["device_id"]
    ts        = data["ts"]
    lat       = data["lat"]
    lon       = data["lon"]
    speed     = data["speed_kmh"]

    # store raw log
    from datetime import datetime
    log_entry = {
        "device_id": device_id,
        "timestamp": datetime.utcfromtimestamp(ts),
        "lat": lat,
        "lon": lon,
        "speed_kmh": speed,
    }
    gps_logs.append(log_entry)

    # process for driver score and premium
    ingest_gps_point(device_id, ts, lat, lon, speed)

    # compute raw acceleration from last two points
    acc = None
    pts = user_points[device_id]
    if len(pts) >= 2:
        p1, p2 = pts[-2], pts[-1]
        dt = p2['t'] - p1['t']
        if dt > 0:
            acc = (p2['v'] - p1['v']) / dt  # m/s^2

    # fetch event counters
    events = user_events[device_id]
    brakes = events.get('brakes', 0)
    accels = events.get('accels', 0)
    night  = events.get('night', False)

    score   = compute_driver_score(device_id)
    premium = compute_premium(device_id, base_rate=50.0)  # example base rate

    # Print latitude, longitude, speed, acceleration, event counts, score, and premium
    print(
        f"[GPS] {device_id} → "
        f"lat={lat:.5f}, lon={lon:.5f}, speed={speed:.1f} km/h, "
        f"acc={acc:.2f} m/s², brakes={brakes}, accels={accels}, night={night} | "
        f"[SCORE] {score:.1f} | [PREMIUM] ₹{premium:.2f}"
    )

    return jsonify({
        "status": "ok",
        "driver_score": score,
        "daily_premium": premium
    }), 200


def get_logs():
    # return last 20 raw entries
    return jsonify(gps_logs[-20:]), 200