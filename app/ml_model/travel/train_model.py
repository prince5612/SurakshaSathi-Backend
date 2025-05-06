import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the dataset
df = pd.read_csv("travel_insurance_dataset_india.csv")

# Select features and target based on actual columns
X = df[["duration", "crime_index", "aqi", "weather_risk", "transport_multiplier"]]
y = df["total_premium"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "travel_insurance_model.pkl")

print("✅ Random Forest model trained and saved as 'travel_insurance_model.pkl'")
