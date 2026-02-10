import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib

home_data = pd.read_csv ("./dataset/train.csv")

#print (home_data.describe())
#print (home_data.columns)

features = [
    'Rooms', 'Type', 'Distance', 'Bathroom', 'Landsize', 'Regionname', 
]

X_raw = home_data[features]     # 6 columns
y = home_data['Price']
X = pd.get_dummies(X_raw)       # Many columns: 'Type' and 'Regionname' columns are one-hot encoded now.

home_model = RandomForestRegressor(random_state=1)

print ("Training...")
home_model.fit(X, y)

'''
FOR TRAINING AND TESTING THE MODEL

train_X, test_X, train_y, test_y = train_test_split(X, y, random_state=1)
test_predictions = home_model.predict(test_X)
error = mean_absolute_error(test_y, test_predictions)
print(error)
'''

model_columns = list(X.columns)

joblib.dump(home_model, "home_model.joblib")
joblib.dump(model_columns, "model_columns.joblib")

print("Saved Successfully.")