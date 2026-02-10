from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

model = joblib.load("house_model.joblib")
model_columns = joblib.load("model_columns.joblib")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vue URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the "Shape" of the data the user will send
class HomeData(BaseModel):
    Rooms: int
    Type: str
    Distance: float
    Bathroom: int
    Landsize: float

@app.get("/")
def home():
    return {"message": "House Price Prediction API is running!"}

@app.post("/predict")
def predict_price(data: HomeData):
    input_data = {col: 0 for col in model_columns}

    input_data['Rooms'] = data.Rooms
    input_data['Distance'] = data. Distance
    input_data['Bathroom'] = data.Bathroom
    input_data['Landsize'] = data.Landsize
    
    type_val = data.get('Type')
    type_column = f"Type_{data.get(type_val)}"       # One Hot Encoding
    if type_column in input_data:
        input_data[type_column] = 1

    regionname_val = data.get('Regionname')
    regionname_column = f"Type_{data.get(regionname_val)}"       # One Hot Encoding
    if regionname_column in input_data:
        input_data[regionname_column] = 1

    df = pd.DataFrame([input_data])[model_columns]

    prediction = model.predict(df)

    return {"predicted_price": float(prediction[0])}