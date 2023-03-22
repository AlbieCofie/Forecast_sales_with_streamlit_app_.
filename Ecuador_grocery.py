import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('rfm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the test data
test_data = pd.read_csv('main_final_test.csv')

# Define options for the family dropdown
family_options = ['family_Beverages', 'family_Clothing', 'family_Food', 'family_Home_and_Kitchen', 'family_Others', 'family_Personal_Care']

# Define options for the day type dropdown
day_type_options = ['Holiday', 'Workday']

# Define options for the store and cluster dropdowns
store_options = list(range(1, 55))
cluster_options = list(range(1, 17))

# Define the date range for the calendar
date_range = pd.date_range(start='2017-08-16', end='2017-08-31')

# Create the streamlit app
st.title('Sales Prediction App')

input_values = []


# Sidebar for user input
with st.sidebar:
    st.write('## Input Parameters')

    # Date selector
    selected_date = st.date_input('Select a date:', date_range[0], min_value=date_range[0], max_value=date_range[-1])

    # Store selector
    selected_store = st.selectbox('Select a store:', store_options)

    # Sales cluster selector
    selected_cluster = st.selectbox('Select a sales cluster:', cluster_options)

    # Family dropdown
    selected_family = st.selectbox('Select a family:', family_options)

    # Day type selector
    selected_day_type = st.selectbox('Select a day type:', day_type_options)

    # Predict button
    if st.button('Predict'):
        # Filter the test data for the selected date and store
        selected_data = test_data.loc[(test_data.index == pd.to_datetime(selected_date)) & (test_data['store_nbr'] == selected_store), :]

        # Set the input values for the model
        input_values = [
            selected_data['cluster'].iloc[0],
            selected_data['week'].iloc[0],
            selected_data['quarter'].iloc[0],
            selected_data['month'].iloc[0],
            selected_data['weekday'].iloc[0],
            selected_data['week_lag_1'].iloc[0],
            selected_data['next_day_sales'].iloc[0],
            selected_data['week_ma_7'].iloc[0],
            selected_data['week_ma_14'].iloc[0],
            selected_data['week_ma_30'].iloc[0],
            selected_data['diff_1'].iloc[0],
            selected_data['pct_change'].iloc[0],
            selected_data['Min'].iloc[0],
            selected_data['Max'].iloc[0],
            selected_data['onpromotion_encoded'].iloc[0],
            selected_data[selected_family].iloc[0],
            selected_data['Promotions_bin_0'].iloc[0],
            selected_data['Promotions_bin_1'].iloc[0],
            selected_data['Promotions_bin_2'].iloc[0],
            selected_data['Promotions_bin_3'].iloc[0],
            selected_data['Store_type_A'].iloc[0],
            selected_data['Store_type_B'].iloc[0],
            selected_data['Store_type_C'].iloc[0],
            selected_data['Store_type_D'].iloc[0],
            selected_data['Store_type_E'].iloc[0],
            selected_data['city_Ambato'].iloc[0],
            selected_data['city_Babahoyo'].iloc[0],
            selected_data['city_Cayambe'].iloc[0],
            selected_data['city_Cuenca'].iloc[0],
            selected_data['city_Daule'].iloc[0],
            selected_data['city_El_Carmen'].iloc[0],
            selected_data['city_Esmeraldas'].iloc[0],
            selected_data['city_Guaranda'].iloc[0],
            selected_data['city_Guayaquil'].iloc[0],
            selected_data['city_Ibarra'].iloc[0],
            selected_data['city_Latacunga'].iloc[0],
            selected_data['city_Libertad'].iloc[0],
            selected_data['city_Loja'].iloc[0],
            selected_data['city_Machala'].iloc[0],
            selected_data['city_Manta'].iloc[0],
            selected_data['city_Playas'].iloc[0],
            selected_data['city_Puyo'].iloc[0],
            selected_data['city_Quevedo'].iloc[0],
            selected_data['city_Quito'].iloc[0],
            selected_data['city_Riobamba'].iloc[0],
            selected_data['city_Salinas'].iloc[0],
            selected_data['city_Santo_Domingo'].iloc[0]
            ]

    if selected_day_type == 'Holiday':
        input_values.extend([1, 0])
    else:
        input_values.extend([0, 1])

    # Make the prediction with the loaded model
    prediction = model.predict([input_values])[0]

    # Display the prediction to the user
    st.write('## Sales Prediction')
    st.write(f'The predicted sales for {selected_date} at store {selected_store} for family {selected_family} are ${prediction:.2f}.')
