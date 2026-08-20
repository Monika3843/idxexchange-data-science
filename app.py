import streamlit as st
import pandas as pd
import joblib

model_package = joblib.load('outputs/xgb_model_package.pkl')
model = model_package['model']
feature_cols = model_package['feature_cols']
feature_defaults = model_package['feature_defaults']

st.title('California Home Price Predictor')
st.write('Enter property details below to get an estimated sale price.')

living_area = st.number_input('Living Area (sq ft)', min_value=200, max_value=15000, value=1800, step=50)
bedrooms = st.number_input('Bedrooms', min_value=1, max_value=10, value=3, step=1)
bathrooms = st.number_input('Bathrooms', min_value=1, max_value=10, value=2, step=1)
lot_size = st.number_input('Lot Size (acres)', min_value=0.01, max_value=10.0, value=0.2, step=0.01)

if st.button('Predict Price'):
    input_row = feature_defaults.copy()
    input_row['LivingArea'] = living_area
    input_row['BedroomsTotal'] = bedrooms
    input_row['BathroomsTotalInteger'] = bathrooms
    input_row['LotSizeAcres'] = lot_size

    X_input = pd.DataFrame([input_row])[feature_cols]
    prediction = model.predict(X_input)[0]

    st.success(f'Estimated Price: ${prediction:,.0f}')
    st.caption('Note: this estimate uses median values for location and other '
               'details not entered here (e.g. school district, property age), '
               'so accuracy is best for a "typical" property.')