import pandas as pd
import pickle

with open("flight_pred_light.pkl",'rb') as file:
  model = pickle.load(file)

def calculate_duration_hours(d_h, d_m, a_h, a_m):
    total_dep_min = d_h*60 + d_m
    total_arr_min = a_h*60 + a_m
    if total_arr_min < total_dep_min:
        total_arr_min = total_arr_min + 24*60
        duration = total_arr_min - total_dep_min
    else:
        duration = total_arr_min - total_dep_min
    return duration

def preprocess_input(input_dict):
    expected_columns = [
                'Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_hour',
       'Dep_min', 'Arr_hour', 'Arr_min', 'Duration_hours', 'Airline_Air India',
       'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways',
       'Airline_Jet Airways Business', 'Airline_Multiple carriers',
       'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
       'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
       'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
       'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
       'Destination_Kolkata'
    ]
    
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    for key, value in input_dict.items():
        if key == 'Airline':
            if value == 'Trujet':
                df['Airline_Trujet'] = 1
            elif value == 'Vistara Premium economy':
                df['Airline_Vistara Premium economy'] = 1
            elif value == 'Multiple carriers Premium economy':
                df['Airline_Multiple carriers Premium economy']=1
            elif value == 'GoAir':
                df['Airline_GoAir'] = 1
            elif value == 'SpiceJet':
                df['Airline_SpiceJet'] = 1
            elif value == 'Vistara':
                df['Airline_Vistara'] = 1
            elif value == 'Air India':
                df['Airline_Air India'] = 1
            elif value == 'Jet Airways Business':
                df['Airline_Jet Airways Business'] = 1
            elif value == 'IndiGo':
                df['Airline_IndiGo'] = 1
            elif value == 'Multiple carriers':
                df['Airline_Multiple carriers'] = 1
            elif value == 'Jet Airways':
                df['Airline_Jet Airways'] = 1
        elif key == 'Source':
            if value == 'Delhi':
                df['Source_Delhi'] =1
            elif value == 'Chennai':
                df['Source_Chennai'] = 1
            elif value == 'Mumbai':
                df['Source_Mumbai'] = 1
            elif value == 'Kolkata':
                df['Source_Kolkata'] = 1
        elif key == 'Destination':
            if value == 'Kolkata':
                df['Destination_Kolkata'] = 1
            if value == 'Cochin':
                df['Destination_Cochin'] = 1
            if value == 'Hyderabad':
                df['Destination_Hyderabad'] = 1
            if value == 'Delhi':
                df['Destination_Delhi'] = 1
        elif key == 'Total_Stops':
            if value == '0':
                df['Total_Stops'] = 0
            if value == '1':
                df['Total_Stops']= 1
            if value == '2':
                df['Total_Stops'] = 2
            if value == '3':
                df['Total_Stops'] = 3
            if value == '4':
                df['Total_Stops'] = 4
        elif key == 'Journey_Month':
            df['Journey_Month'] = value
        elif key == 'Journey_Date':
            df['Journey_Day'] = value
        elif key == 'Dep_Hour':
            df['Dep_hour'] = value
        elif key == 'Dep_Min':
            df['Dep_min'] = value
        elif key == 'Arr_Hour':
            df['Arr_hour'] = value
        elif key == 'Arr_Min':
            df['Arr_min'] = value
        df['Duration_hours'] = calculate_duration_hours(input_dict['Dep_Hour'], input_dict['Dep_Min'],input_dict['Arr_Hour'],input_dict['Arr_Min'])
    return df

def predict(input_dict):
    input_df =  preprocess_input(input_dict)
    prediction = model.predict(input_df)
    return int(prediction[0])











    


