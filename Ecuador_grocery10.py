import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import datetime

# Define the preprocess_inputs function
def preprocess_inputs(date, store_nbr, family, onpromotion, city, store_type, cluster, transactions, dcoilwtico, holiday_type):
    # Combine the inputs into a dictionary
    inputs = {'date': date, 'store_nbr': store_nbr, 'family': family, 'onpromotion': onpromotion, 'city': city, 'store_type': store_type, 'cluster': cluster, 'transactions': transactions, 'dcoilwtico': dcoilwtico, 'holiday_type': holiday_type}

    # Create a pandas DataFrame from the dictionary
    input_df = pd.DataFrame(inputs, index=[0])
    scaler = StandardScaler()
    input_df[num_cols] = scaler.fit_transform(input_df[num_cols])

    # Load the StandardScaler and OneHotEncoder from scikit-learn
    with open('encoder.pkl', 'rb') as file:
        encoder = pickle.load(file)

    cat_cols = ['store_nbr', 'family', 'city', 'store_type', 'cluster', 'holiday_type']
    encoded_data = encoder.transform(input_df[cat_cols]).toarray()
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names(cat_cols))
    final_df = pd.concat([input_df[num_cols], encoded_df], axis=1)
    return final_df

# Define the predict_sales function

def predict_sales(date, store_nbr, family, onpromotion, city, store_type, cluster, transactions, dcoilwtico, holiday_type):
    # preprocess the inputs
    num_cols = ['onpromotion', 'transactions', 'dcoilwtico']
    inputs = preprocess_inputs(date, store_nbr, family, onpromotion, city, store_type, cluster, transactions, dcoilwtico, holiday_type, num_cols)

    # Load the saved model from disk
    with open('best_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # initialize prediction to None
    prediction = None
    if model is not None:
        # predict using the model
        prediction = model.predict(inputs)

    return prediction

def app():
    # Add a title
    # Set the page title and header
    st.set_page_config(page_title='Sales Prediction App', page_icon=':bar_chart:', layout='wide')
    st.title('Sales Prediction App')

    # Add a subtitle
    st.subheader("Enter the details to predict sales")

    # Add the input fields
    date = st.date_input("Date", datetime.date(2017, 1, 1))
    store_nbr = st.selectbox("Store number", [i for i in range(1, 55)])
    family = st.selectbox("Family", ['Others', 'Food', 'Beverages', 'Personal Care', 'Clothing', 'Home and Kitchen'])
    #sales = st.number_input("Sales")
    onpromotion = st.selectbox("On Promotion", [i for i in range(0, 200)])
    city = st.selectbox("City", ['Quito', 'Santo Domingo', 'Cayambe', 'Latacunga', 'Riobamba', 'Ibarra', 'Guaranda', 'Ambato', 'Puyo', 'Loja', 'Machala', 'Cuenca'])
    store_type = st.selectbox("Store type", ['A', 'D', 'B', 'C', 'E'])
    cluster = st.selectbox("Cluster", [i for i in range(1, 18)])
    transactions = st.number_input("Transactions")
    dcoilwtico = st.number_input("Crude Oil Price")
    holiday_type = st.selectbox("Holiday Type", ['Holiday', 'Additional', 'Transfer'])

    # Add a button to predict the sales
    if st.button("Predict"):
        prediction = predict_sales(date, store_nbr, family, onpromotion, city, store_type, cluster, transactions, dcoilwtico, holiday_type)
        if prediction is not None:
            st.write("The predicted  for the given input is:", round(prediction[0], 2))

if __name__ == '__main__':
            app()
