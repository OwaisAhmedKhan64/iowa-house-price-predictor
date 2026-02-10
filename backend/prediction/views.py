from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(settings.BASE_DIR / 'home_model.joblib')
COLUMNS_PATH = os.path.join(settings.BASE_DIR / 'model_columns.joblib')

model = joblib.load (MODEL_PATH)
columns = joblib.load (COLUMNS_PATH)

class PredictPrice (APIView):
    def post (self, request):
        try:
            data = request.data

            input_data = {column: 0 for column in columns}
            input_data ['Rooms'] = data.get('Rooms')
            input_data ['Distance'] = data.get('Distance')
            input_data ['Bathroom'] = data.get('Bathroom')
            input_data ['Landsize'] = data.get('Landsize')

            # Translating One Hot Encoding

            type_data = data.get ('Type')
            type_column = f"Type_{type_data}"
            if type_column in input_data:
                input_data[type_column] = 1
            
            regionname_data = data.get ('Regionname')
            regionname_column = f"Regionname_{regionname_data}"
            if regionname_column in input_data:
                input_data[regionname_column] = 1
            
            # Making the table

            df = pd.DataFrame ([input_data])[columns]

            prediction = model.predict (df)[0]

            active_columns = [k for k, v in input_data.items() if v == 1]
            print(f"Columns activated for this prediction: {active_columns}")

            return Response ({'predicted_price': round(prediction, 2)}, status=status.HTTP_200_OK)
        
            
        
        except Exception as e:
            return Response ({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        