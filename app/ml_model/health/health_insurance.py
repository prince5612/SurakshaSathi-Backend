import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
import os
import requests
from geopy.geocoders import Nominatim

# Load environment variables
load_dotenv()
TOKEN = os.getenv("WAQI_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set WAQI_TOKEN in your .env")

# Load and preprocess the dataset
df = pd.read_csv("Static/health_insurance_premium_dataset_1000.csv")

# Encode categorical variables
label_encoders = {}
for col in ['Has_PreExisting_Condition', 'Gender', 'Smoking', 'Alcohol']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and label
X = df.drop(columns=['User_ID', 'Premium'])
y = df['Premium']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Utility functions
def get_lat_long(city_name):
    """Get latitude and longitude of a city."""
    geolocator = Nominatim(user_agent="city_lat_long_finder")
    location = geolocator.geocode(city_name)
    return (location.latitude, location.longitude) if location else None

def get_aqi(lat, lon):
    """Fetch AQI from WAQI using coordinates."""
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={TOKEN}"
    resp = requests.get(url, timeout=5)
    data = resp.json()
    if data.get("status") != "ok":
        raise ValueError(f"WAQI API error: {data.get('data')}")
    return int(data["data"]["aqi"])

# def preprocess_input_data(input_data):
#     # Define a list of expected keys
#     expected_keys = ['Has_PreExisting_Condition', 'Gender', 'Smoking', 'Alcohol']
    
#     # Check if each key exists in the input data
#     for key in expected_keys:
#         if key not in input_data:
#             raise KeyError(f"Missing key: {key}")
        
#         # Standardize categorical values to title case or lowercase
#         input_data[key] = input_data[key].strip().capitalize()
    
#     return input_data

def preprocess_input_data(input_data):
    expected_keys = ['pre_existing_condition', 'gender', 'alcohol_consumption', 'smoking']
    
    for key in expected_keys:
        if key not in input_data:
            raise KeyError(f"Missing key: {key}")
        
        value = input_data[key].strip().lower()

        if key == "gender":
            if value == "female":
                input_data[key] = "F"
            elif value == "male":
                input_data[key] = "M"
            else:
                raise ValueError("Gender must be 'male' or 'female'")
        else:
            # Normalize Yes/No format
            if value == "yes":
                input_data[key] = "Yes"
            elif value == "no":
                input_data[key] = "No"
            else:
                raise ValueError(f"Invalid value '{value}' for field '{key}'")
    
    return input_data



def health_predict_premium(form_data):
    """
    Predict insurance premium from form fields.
    form_data: dict with keys like city, age, gender, etc.
    """
    # Standardize and preprocess input data
    form_data = preprocess_input_data(form_data)
    print(form_data)
    # Get AQI using city
    city = form_data.get("city")  # Changed to match the name in pay_health_insurance_premium
    lat_long = get_lat_long(city)
    if not lat_long:
        raise ValueError("Invalid city name provided.")
    aqi = get_aqi(lat_long[0], lat_long[1])

    # Prepare input data
    input_data = {
        "AQI_Level": aqi,
        "BMI": float(form_data["bmi"]),  # Changed to match the name in pay_health_insurance_premium
        "Daily_Steps": int(form_data["daily_steps"]),  # Changed to match the name in pay_health_insurance_premium
        "Sleep_Hours": float(form_data["sleep_hours"]),  # Changed to match the name in pay_health_insurance_premium
        "Has_PreExisting_Condition": form_data["pre_existing_condition"],  # Changed to match the name in pay_health_insurance_premium
        "Age": int(form_data["age"]),  # Changed to match the name in pay_health_insurance_premium
        "Gender": form_data["gender"],  # Changed to match the name in pay_health_insurance_premium
        "Smoking": form_data["smoking"],  # Changed to match the name in pay_health_insurance_premium
        "Alcohol": form_data["alcohol_consumption"]  # Changed to match the name in pay_health_insurance_premium
    }

    # Encode categorical fields
    for col in ['Has_PreExisting_Condition', 'Gender', 'Smoking', 'Alcohol']:
        # Ensure the label exists before transformation
        if input_data[col] not in label_encoders[col].classes_:
            raise ValueError(f"Unseen label '{input_data[col]}' found in column '{col}'")
        
        input_data[col] = label_encoders[col].transform([input_data[col]])[0]

    # Convert to DataFrame and predict
    input_df = pd.DataFrame([input_data])
    predicted_premium = model.predict(input_df)[0]
    print(predicted_premium)
    return {"predicted_premium": float(round(predicted_premium , 2))}