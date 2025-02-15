'''
In this project, we'll build a simple application 
to explore some properties of a used car dataset

'''
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pyarrow as pa

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

df = df.reset_index(drop=True)

# Remove rows with non-positive prices
df = df[df['price'] > 0]
# Ensure 'price' is numeric and convert to float
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(float)

# Fill missing values in 'days_listed' and ensure integer type
df['days_listed'] = df['days_listed'].fillna(0).astype(int)

# Convert 'model_year' to string to handle compatibility issues
df['model_year'] = df['model_year'].astype(str)

# Remove non-numeric entries in 'model_year' if any
df = df[df['model_year'].str.isnumeric()]

# Convert 'model_year' back to float for processing
df['model_year'] = df['model_year'].astype(float)

df = df[df['model_year'] > 0]

df = df.reset_index(drop=True)

# create a text header above the dataframe
st.header('Car Sales Advertisements') 

st.dataframe(df)

st.header('Car Condition by Milage')

# create a plotly histogram figure
fig = px.histogram(df, x='odometer', color='condition')

# display the figure with streamlit
st.write(fig)

st.header('Model condition by Year')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

# Filters
manufacturer_filter = st.multiselect(
    'Select Manufacturer', options=df['manufacturer'].unique(), default=df['manufacturer'].unique()
)
min_year, max_year = st.slider('Select Model Year Range', min_value=int(df['model_year'].min()), max_value=int(df['model_year'].max()), value=(int(df['model_year'].min()), int(df['model_year'].max())))
price_filter = st.slider('Select Price Range', min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))
odometer_filter = st.slider('Select Milage Range', min_value=int(df['odometer'].min()), max_value=int(df['odometer'].max()), value=(int(df['odometer'].min()), int(df['odometer'].max())))

# Apply Filters
filtered_df = df[
    (df['manufacturer'].isin(manufacturer_filter)) &
    (df['model_year'] >= min_year) &
    (df['model_year'] <= max_year) &
    (df['price'] >= price_filter[0]) &
    (df['price'] <= price_filter[1]) &
    (df['odometer'] >= odometer_filter[0]) &
    (df['odometer'] <= odometer_filter[1])
]

# Display Filtered Table
st.write("Filtered Table:")
st.dataframe(filtered_df)
