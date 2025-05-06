# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# # Load dataset
# df = pd.read_csv("Static/user_dataset_updated_premium.csv")

# # Encode categorical features
# le_gender = LabelEncoder()
# le_risk = LabelEncoder()

# df["Gender"] = le_gender.fit_transform(df["Gender"])
# df["OccupationRisk"] = le_risk.fit_transform(df["OccupationRisk"])


# X = df.drop(columns=['user_id','Premium_Price'])  # Features
# y = df["Premium_Price"]                # Target




# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)



# y_pred = model.predict(X_test)
# # print("R2 Score:", r2_score(y_test, y_pred))
# # print("MSE:", mean_squared_error(y_test, y_pred))

# # Example: predict for new user (age=35, Male, income=600000, Medium risk, 2 dependents)
# new_input = pd.DataFrame([[25, le_gender.transform(['F'])[0], 400000, le_risk.transform(['Medium'])[0], 2]],
#                          columns=["Age", "Gender", "Annual_Income", "OccupationRisk", "Number_of_Dependents"])
# predicted_price = model.predict(new_input)
# print("Predicted Premium:", predicted_price[0])


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("Static/user_dataset_updated_premium.csv")

# Encode categorical features
le_gender = LabelEncoder()
le_risk = LabelEncoder()

df["Gender"] = le_gender.fit_transform(df["Gender"])
df["OccupationRisk"] = le_risk.fit_transform(df["OccupationRisk"])

# Features and target
X = df.drop(columns=['user_id', 'Premium_Price'])
y = df["Premium_Price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation (optional)
# y_pred = model.predict(X_test)
# print("R2 Score:", r2_score(y_test, y_pred))
# print("MSE:", mean_squared_error(y_test, y_pred))

# --- Prediction Function ---
import pandas as pd

def life_predict_premium(data):
    try:
        # Load and encode model assets
        df = pd.read_csv("Static/user_dataset_updated_premium.csv")

        from sklearn.preprocessing import LabelEncoder
        from sklearn.ensemble import RandomForestRegressor

        le_gender = LabelEncoder()
        le_risk = LabelEncoder()

        df["Gender"] = le_gender.fit_transform(df["Gender"])
        df["OccupationRisk"] = le_risk.fit_transform(df["OccupationRisk"])

        X = df.drop(columns=['user_id', 'Premium_Price'])
        y = df["Premium_Price"]

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Extract input values from data dictionary
        age = data.get("age")
        gender = data.get("gender")
        # if gender=="female":
        #     gender="F"
        # else:
        #     gender="M"
        income = data.get("income")
        occupation_risk = data.get("occupation_risk")  # "Low", "Medium", or "High"
        dependents = data.get("dependents")

        # Validate input
        if None in [age, gender, income, occupation_risk, dependents]:
            return {"error": "Missing one or more input fields"}, 400

        # Encode categorical fields
        encoded_gender = le_gender.transform([gender])[0]
        encoded_risk = le_risk.transform([occupation_risk])[0]

        # Prepare input
        input_df = pd.DataFrame([[age, encoded_gender, income, encoded_risk, dependents]],
                                columns=["Age", "Gender", "Annual_Income", "OccupationRisk", "Number_of_Dependents"])

        prediction = round(model.predict(input_df)[0])
        print(prediction)
        return {"predicted_premium": prediction}, 200

    except Exception as e:
        return {"error": str(e)}, 500


# # Example usage
# try:
#     predicted = predict_premium(25, "F", 400000, "Medium", 2)
#     print("Predicted Premium:", predicted)
# except ValueError as ve:
#     print("Input Error:", ve)
