import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

home_data = pd.read_csv ("./dataset/train.csv")

features = [
    'Rooms', 'Type', 'Distance', 'Bathroom', 'Landsize', 'Regionname', 
]

X_raw = home_data[features]     # 6 columns
y = home_data['Price']
X = pd.get_dummies(X_raw)       # Many columns: 'Type' and 'Regionname' columns are one-hot encoded now.

home_model = RandomForestRegressor(random_state=1)

print ("Training...")
home_model.fit(X, y)

model_columns = list(X.columns)

joblib.dump(home_model, "home_model.joblib")
joblib.dump(model_columns, "model_columns.joblib")

print("Saved Successfully.")