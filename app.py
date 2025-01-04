'''
In this project, we'll build a simple application 
to explore some properties of a used car dataset

'''
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# Cleaning and validating the dataset

df['price'] = df['price'].astype(float)

# Drop rows with missing values in 'model_year'
df = df.dropna(subset=['model_year'])

# Filter for plausible model years (e.g., 1950 to 2025)
df = df[(df['model_year'] >= 1950) & (df['model_year'] <= 2025)]

# Ensure 'model_year' is numeric (if further conversion is needed)
df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce')

# Reset index to clean up the DataFrame
df = df.reset_index(drop=True)

# Remove rows with non-positive prices
df = df[df['price'] > 0]

# Fill missing values in 'days_listed' and ensure integer type
df['days_listed'] = df['days_listed'].fillna(0).astype(int)

# Fill missing 'model_year' with 0 and convert to integer
df['model_year'] = df['model_year'].fillna(0).astype(int)

# create a text header above the dataframe
st.header('Car Sales Advertisements') 

# display the dataframe with streamlit
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
