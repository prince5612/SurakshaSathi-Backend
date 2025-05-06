# testcase.py
import requests

url = "http://127.0.0.1:5000/predict"

payload = {
    "start_date": "2025-11-01",
    "end_date": "2025-11-04",
    "lat": 28.6139,
    "lon": 77.2090,
    "transport_mode": "car"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("✅ Prediction Response:")
    print(response.json())
else:
    print("❌ Error:", response.text)
