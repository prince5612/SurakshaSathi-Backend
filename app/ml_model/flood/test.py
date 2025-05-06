import requests

url = "http://127.0.0.1:5000/predict_premium"

payload = {
    # "lat": 4.7110,
    # "lon": 103.8198,
    "lat": 19.0760,  # Sabarmati River near Ahmedabad
    "lon": 72.8777,
    "base_premium": 1000,
    "api_key": "58927841f9ee49930f33b723080ca6b9"
}


response = requests.post(url, json=payload)

if response.status_code == 200:
    print("✅ Prediction:")
    print(response.json())
else:
    print("❌ Error:")
    print(response.status_code, response.text)