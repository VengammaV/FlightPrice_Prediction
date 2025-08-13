import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Path to the saved model and its components
MODEL_PATH =  "model_data.joblib"

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

def prepare_input(input_dict):
    expected_columns = ['Age', 'Flight_Distance', 'Inflight_wifi_service',
       'Departure/Arrival_time_convenient', 'Ease_of_Online_booking',
       'Gate_location', 'Food_and_drink', 'Online_boarding', 'Seat_comfort',
       'Inflight_entertainment', 'On-board_service', 'Leg_room_service',
       'Baggage_handling', 'Checkin_service', 'Inflight_service',
       'Cleanliness', 'Arrival_Delay_in_Minutes',
       'Customer_Type_disloyal Customer', 'Type_of_Travel_Personal Travel',
       'Class_Eco', 'Class_Eco Plus']
    
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    for key, value in input_dict.items():
        
        if key == 'Age':
            df['Age'] = value
        elif key == 'Flight_Distance':
            df['Flight_Distance'] = value
        elif key == 'Inflight_wifi_service':
            df['Inflight_wifi_service'] = value
        elif key == 'Departure_Arrival_time_convenient':
            df['Departure/Arrival_time_convenient'] = value
        elif key == 'Ease_of_Online_booking':
            df['Ease_of_Online_booking'] = value
        elif key == 'Gate_location':
            df['Gate_location'] = value
        elif key == 'Food_and_drink':
            df['Food_and_drink'] = value
        elif key == 'Online_boarding':
            df['Online_boarding'] = value
        elif key == 'Seat_comfort':
            df['Seat_comfort'] = value
        elif key == 'Inflight_entertainment':
            df['Inflight_entertainment'] = value
        elif key == 'On_board_service':
            df['On-board_service'] = value
        elif key == 'Leg_room_service':
            df['Leg_room_service'] = value
        elif key == 'Baggage_handling':
            df['Baggage_handling'] = value
        elif key== 'Checkin_service':
            df['Checkin_service'] = value
        elif key == 'Inflight_service':
            df['Inflight_service'] = value
        elif key == 'Cleanliness':
            df['Cleanliness'] = value
        elif key == 'Arrival_Delay_in_Minutes':
            df['Arrival_Delay_in_Minutes'] = value
        elif key == 'Customer_Type':
            if value ==  'disloyal Customer':
                df['Customer_Type_disloyal Customer'] = 1
        elif key == 'Type_of_Travel':
            if value == 'Personal Travel':
                df['Type_of_Travel_Personal Travel'] = 1
        elif key == 'Class':
            if value == 'Eco Plus':
                df['Class_Eco Plus'] = 1
            elif value == 'Eco':
                df['Class_Eco'] = 1
        
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df

def cust_predict(input_dict):
    input_df =  prepare_input(input_dict)
    prediction = model.predict(input_df)
    return int(prediction[0])

        
        
        


            