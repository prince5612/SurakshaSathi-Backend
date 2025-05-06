import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("flood_insurance_data.csv")

# Features and target
X = df[['rain_mm', 'has_alert', 'near_water', 'lat', 'lon']]
y = df['flood_multiplier']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "flood_model.pkl")
print("Model trained and saved as flood_model.pkl")
