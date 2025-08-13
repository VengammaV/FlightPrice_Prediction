import streamlit as st
from prediction_helper import predict # type: ignore
from cust_prediction_helper import cust_predict # type: ignore
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit App Title
st.set_page_config(page_title="Data Analysis", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Flight Price Prediction",  "Customer Satisfaction"])

# -------------------------------- PAGE 1: --------------------------------
if page == "Flight Price Prediction":
    st.title("🛬 Flight Price Prediction & Analysis")
    st.subheader("📊 A Streamlit App for Visual analysis and Price Prediction for flights")
    st.write("""
    This project analyzes and predicts the flight price for different Airlines,cities,duration and date of journey using RandomForest Regressor Machine Learning Algorithm
    """)
    
    categorical_options = {
      'Airline': ['Jet Airways', 'IndiGo','Air India','Multiple carriers','SpiceJet','Vistara','Air Asia','GoAir','Multiple carriers Premium economy','Jet Airways Business','Vistara Premium economy','Trujet'],
      'Source': ['Kolkata', 'Banglore','Delhi','Chennai','Mumbai'],
      'Destination': ['Delhi', 'Cochin','Kolkata','Banglore','Hyderabad'],
       'Total_stops': ['0', '1', '2','3','4']   
    }

    tab1, tab2 = st.tabs(["📈Flight Price Prediction"," 📊 Visualization"]) 

    css = '''
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.5rem;
        }
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    with tab1:
# Create four rows of three columns each
        row1 = st.columns(3)
        row2 = st.columns(3)
        row3 = st.columns(4)
        row4 = st.columns(2)

        with row1[0]:
            Airline = st.selectbox('Airline', categorical_options['Airline'])
        with row1[1]:
            Source = st.selectbox('Source', categorical_options['Source'])
        with row1[2]:
            Destination = st.selectbox('Destination', categorical_options['Destination'])

        with row2[0]:
            Stops = st.selectbox('Stops', categorical_options['Total_stops'])
        with row2[1]:
            Journey_date = st.number_input('Journey Date', min_value=1, step=1, max_value=31)
        with row2[2]:
            Journey_month = st.number_input('Journey Month', min_value=1, step=1, max_value=12)

        with row3[0]:
            dep_time_hour = st.number_input('Dep Time_Hour', min_value=0, step=1, max_value=24)
        with row3[1]:
            dep_time_min = st.number_input('Dep Time_Minute', min_value=0, step=5, max_value=60)
        with row3[2]:
            arr_time_hour = st.number_input('Arrival Time_Hour', min_value=0, step=1, max_value=24)
        with row3[3]:
            arr_time_min = st.number_input('Arrival Time_Minute', min_value=0, step=5, max_value=60)

#Create dictionary for input values

        input_dict = {
            'Airline': Airline,
            'Source': Source,
            'Destination': Destination,
            'Total_Stops': Stops,
            'Journey_Date': Journey_date,
            'Journey_Month': Journey_month,
            'Dep_Hour': dep_time_hour,
            'Dep_Min': dep_time_min,
            'Arr_Hour': arr_time_hour,
            'Arr_Min': arr_time_min,
            }

        if st.button('Predict'):
            prediction = predict(input_dict)
            st.success(f'Predicted Flight Price: {prediction} ')

# Content for Tab 2
    with tab2:
        #st.subheader('Flight Price Analysis')
        df = pd.read_csv("output.csv")
        fig, ax = plt.subplots(figsize=(4,2))
        sns.histplot(df['Price'], kde=True)
        plt.title('Flight Price Distribution', fontsize=6)
        plt.xlabel('Flight Price', fontsize=4)
        plt.ylabel('Frequency', fontsize=4)
        plt.xticks(fontsize=4)
        plt.yticks(fontsize=4)   
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(9,5) )
        ax = sns.barplot(df, x = 'Airline', y='Price', ax=ax, width=0.3)
        plt.title('Airline Vs Flight Price Distribution', fontsize=10)
        plt.xticks(rotation=90)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)  
        st.pyplot(fig)

        # Count airline frequencies
        airline_counts = df['Airline'].value_counts().reset_index()
        airline_counts.columns = ['Airline', 'Count']
        # Plot
        fig = px.bar(airline_counts, x='Airline', y='Count',
                    title='Number of Flights by Airline',
                    labels={'Count': 'Number of Flights', 'Airline': 'Airline'},
                    #color='Airline'
                    )
        # Display in Streamlit
        st.plotly_chart(fig)

        fig, ax = plt.subplots(figsize=(4,2))
        sns.barplot(df, x = 'Total_Stops' , y = 'Price', width = 0.4)
        plt.title('Total Stops Vs Flight Price Distribution', fontsize=6)
        plt.xticks(fontsize=4)
        plt.yticks(fontsize=4)
        plt.xlabel('Total Stops',fontsize=6)
        plt.ylabel('Price',fontsize=6)  
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(9,5) )
        ax = sns.barplot(df, x = 'Source', y='Price', ax=ax, width=0.3)
        plt.title('Source Vs Flight Price Distribution', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)  
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(9,5) )
        ax = sns.barplot(df, x = 'Destination', y='Price', ax=ax, width=0.3)
        plt.title('Destination Vs Flight Price Distribution', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)  
        st.pyplot(fig)

        st.subheader("[Day, Month, Arrival and Departure Time, Duration] Vs Price")
        # List of numerical columns
        numerical_cols = ['Journey_Day', 'Journey_Month', 'Dep_hour',  
                        'Arr_hour', 'Duration_hours']

        # Let the user select which column to visualize
        selected_col = st.selectbox("Select a numerical column to visualize:", numerical_cols)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x= df[selected_col], y=df['Price'], ax=ax, color='skyblue')
        ax.set_title(f'Distribution of {selected_col}')
        ax.set_xlabel(selected_col)
        ax.set_ylabel('Price')


        st.pyplot(fig)
    
# -------------------------------- PAGE 2: --------------------------------
elif page == "Customer Satisfaction":
    st.title('Customer Satisfaction Survey')
    st.subheader("📊 A Streamlit App for Customer Satisfaction Prediction and Analysis for Flight Passengers")
    st.write("""
            This project analyzes and predicts the customer satisfaction based on the ratings for various amenities and services provided by Airlines. 
            The prediction uses the Gradient Boosting Machine Learning Algorithm
             """)
    
    categorical_options =  { 'Customer_Type': ['Loyal Customer', 'disloyal Customer'],
      'Type_of_Travel':  ['Personal Travel','Business travel'],
      'Class':  ['Eco Plus' , 'Business',  'Eco']
        }     

    tab4, tab5 = st.tabs(["📈Customer Satisfaction Prediction"," 📊 Visualization"]) 

    css = '''
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.5rem;
        }
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    with tab4:
    # Create four rows of three columns each
        row1 = st.columns(3)
        row2 = st.columns(4)
        row3 = st.columns(4)
        row4 = st.columns(4)
        row5 = st.columns(5)

        with row1[0]:
            Customer_Type = st.selectbox('Customer Type', categorical_options['Customer_Type'])
        with row1[1]:
            Type_of_Travel = st.selectbox('Type of Travel', categorical_options['Type_of_Travel'])
        with row1[2]:
            Class = st.selectbox('Class', categorical_options['Class'])

        with row2[0]:
            Age = st.number_input('Age', min_value=1, step=5, max_value=110)
        with row2[1]:
            Flight_Distance = st.number_input('Flight_Distance', min_value=100, step=150, max_value=5000)
        with row2[2]:
            Inflight_wifi_service = st.number_input('Inflight_wifi_service', min_value=1, step=1, max_value=5)
        with row2[3]:
            Departure_Arrival_time_convenient = st.number_input('Dep/Arr time convenient', min_value=1, step=1, max_value=5)

        with row3[0]:
            Ease_of_Online_booking = st.number_input('Ease of Online booking', min_value=1, step=1, max_value=5)
        with row3[1]:
            Gate_location = st.number_input('Gate location', min_value=1, step=1, max_value=5)
        with row3[2]:
            Food_and_drink = st.number_input('Food and drink', min_value=1, step=1, max_value=5)
        with row3[3]:
            Online_boarding = st.number_input('Online boarding', min_value=1, step=1, max_value=5)

        with row4[0]:
            Seat_comfort = st.number_input('Seat_comfort', min_value=1, step=1, max_value=5)
        with row4[1]:
            Inflight_entertainment = st.number_input('Inflight_entertainment', min_value=1, step=1, max_value=5)
        with row4[2]:
            On_board_service = st.number_input('On-board_service', min_value=1, step=1, max_value=5)
        with row4[3]:
            Leg_room_service = st.number_input('Leg_room_service', min_value=1, step=1, max_value=5)

        with row5[0]:
            Baggage_handling = st.number_input('Baggage_handling', min_value=1, step=1, max_value=5)
        with row5[1]:
            Checkin_service = st.number_input('Checkin_service', min_value=1, step=1, max_value=5)
        with row5[2]:
            Inflight_service = st.number_input('Inflight_service', min_value=1, step=1, max_value=5)
        with row5[3]:
            Cleanliness = st.number_input('Cleanliness', min_value=1, step=1, max_value=5)
        with row5[4]:
            Arrival_Delay_in_Minutes = st.number_input('Arrival_Delay_in_Minutes', min_value=0, step=30, max_value=2000)

        #Create dictionary for input values

        input_dict = {
            'Customer_Type': Customer_Type,
            'Type_of_Travel': Type_of_Travel,
            'Class': Class,
            'Age': Age,
            'Flight_Distance': Flight_Distance,
            'Inflight_wifi_service': Inflight_wifi_service,
            'Departure/Arrival_time_convenient': Departure_Arrival_time_convenient,
            'Ease_of_Online_booking': Ease_of_Online_booking,
            'Gate_location': Gate_location,
            'Food_and_drink': Food_and_drink,
            'Online_boarding': Online_boarding,
            'Seat_comfort': Seat_comfort,
            'Inflight_entertainment': Inflight_entertainment,
            'On-board_service': On_board_service,
            'Leg_room_service': Leg_room_service,
            'Baggage_handling': Baggage_handling,
            'Checkin_service': Checkin_service,
            'Inflight_service': Inflight_service,
            'Cleanliness': Cleanliness,
            'Arrival_Delay_in_Minutes':Arrival_Delay_in_Minutes
            }

        if st.button('Predict'):
            prediction = cust_predict(input_dict)
            if prediction == 0:
                st.success(f'Predicted Customer Satisfaction: Satisfied')
            elif prediction == 1:
                st.success(f'Predicted Customer Satisfaction: Neutral or Dissatisfied')
    
    # Content for Tab 2
    with tab5:
        df = pd.read_csv("cust_output.csv")
      
        
        fig = px.histogram(df, x='Age', nbins=30, histnorm='percent', title='Customer Age Distribution (Percentage)')
        # Format hover text to show percentage with 2 decimal places
        fig.update_traces(hovertemplate='Age: %{x}<br>Percent: %{y:.2f}%')

        # Optional: update axes font sizes
        fig.update_layout(
            xaxis_title='Age',
            yaxis_title='Percentage',
            title_font=dict(size=24),
            xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
            yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14))
        )
        
        st.plotly_chart(fig)
        
        st.subheader("Class Distribution")
        st.bar_chart(df['Class'].value_counts())

        columns_categorical = ['Customer_Type', 'Type_of_Travel', 'Class']
        st.subheader('Customer Satisfaction Analysis')
        st.write("Categorical Column Countplots:")
        # Let the user select which categorical column to visualize
        selected_col = st.selectbox("Select a categorical column to visualize:", columns_categorical)
        # Create the plot
        fig, ax = plt.subplots(figsize=(4, 2))
        sns.countplot(data=df, x=selected_col, hue='satisfaction', ax=ax, width=0.3)
        plt.legend(title='Satisfaction (0=Sat, 1=Not Sat)')
        # Reduce font sizes
        ax.set_xlabel(selected_col, fontsize=4)
        ax.set_ylabel("Count", fontsize=4)
        # Resize tick labels
        ax.tick_params(axis='x', labelsize=4)
        ax.tick_params(axis='y', labelsize=4)
        # Resize legend
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_fontsize(3)
            legend.set_title(legend.get_title().get_text(), prop={'size': 3})
        st.pyplot(fig)

        fig = px.histogram(df, x='Flight_Distance', nbins=50, title='Flight Distance Distribution')
        # Increase font sizes
        fig.update_layout(
            title_font=dict(size=24),
            xaxis_title='Flight Distance',
            yaxis_title='Count',
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            legend=dict(font=dict(size=14))
        )
        st.plotly_chart(fig)

        st.subheader("Arrival Delay Distribution")
        fig, ax = plt.subplots(figsize=(4, 2))    
        sns.kdeplot(df['Arrival_Delay_in_Minutes'].dropna(), shade=True, ax=ax)
        #ax.set_title("Arrival Delay Distribution", fontsize=6)
        ax.set_xlabel("Arrival_Delay_in_Minutes", fontsize=6)
        ax.set_ylabel("Density", fontsize=6)
        ax.tick_params(axis='x', labelsize=4)
        ax.tick_params(axis='y', labelsize=4)
        st.pyplot(fig)

        st.subheader("Services & Ratings Distribution")
        columns_continuous = [ 
            'Inflight_wifi_service', 'Ease_of_Online_booking', 'Gate_location',
               'Food_and_drink', 'Online_boarding', 'Seat_comfort', 
               'Inflight_entertainment', 'On-board_service', 'Leg_room_service',
               'Baggage_handling', 'Checkin_service', 'Inflight_service', 'Cleanliness'
             ]
        num_plots = len(columns_continuous)
        num_cols = 4  # Number of plots per row
        num_rows = (num_plots + num_cols - 1) // num_cols  # Calculate the number of rows needed

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 5 * num_rows))  # Adjust the figure size as needed
        axes = axes.flatten()  # Flatten the axes array for easier indexing

        for i, col in enumerate(columns_continuous):
            sns.histplot(df[col], ax=axes[i], bins = 20)
            axes[i].set_title(col)  # Set the title to the name of the variable

        # If there are any empty plots (if the number of plots isn't a perfect multiple of num_cols), hide the axes
        for j in range(i + 1, num_rows * num_cols):
            axes[j].axis('off')

        plt.tight_layout()
        st.pyplot(fig)
        
        rating_cols = ['Inflight_wifi_service', 'Ease_of_Online_booking', 'Gate_location',
               'Food_and_drink', 'Online_boarding', 'Seat_comfort', 
               'Inflight_entertainment', 'On-board_service', 'Leg_room_service',
               'Baggage_handling', 'Checkin_service', 'Inflight_service', 'Cleanliness']

        avg_rating = df.groupby('satisfaction')[rating_cols].mean().T

        st.subheader("Average Ratings of Services by Satisfaction(0=Sat, 1=Not Sat)")
        st.dataframe(avg_rating)

        fig = px.bar(avg_rating, barmode='group', title="Average Ratings by Satisfaction(0=Sat, 1=Not Sat)")
        st.plotly_chart(fig)      