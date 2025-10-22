import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

st.set_page_config(
    page_title="California Housing Data",
    page_icon="🏠",
    layout="wide"
)

st.title("California Housing Data (1990)")
st.markdown("**by Your Name**")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('housing.csv')
    except:
        url = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"
        df = pd.read_csv(url)
    return df

df = load_data()

st.sidebar.header("See more filters in the sidebar:")

st.sidebar.subheader("Location Type")
location_options = df['ocean_proximity'].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Select location types:",
    options=location_options,
    default=location_options
)

st.sidebar.subheader("Income Level")
income_level = st.sidebar.radio(
    "Select income level:",
    options=["Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (≥4.5)"]
)

st.subheader("Minimal Median House Price")
price_range = st.slider(
    "Select price range:",
    min_value=0,
    max_value=500001,
    value=(0, 500001),
    step=1000
)

def filter_data(df, price_range, selected_locations, income_level):
    filtered_df = df[
        (df['median_house_value'] >= price_range[0]) & 
        (df['median_house_value'] <= price_range[1])
    ]
    
    filtered_df = filtered_df[filtered_df['ocean_proximity'].isin(selected_locations)]
    
    if income_level == "Low (≤2.5)":
        filtered_df = filtered_df[filtered_df['median_income'] <= 2.5]
    elif income_level == "Medium (>2.5 & <4.5)":
        filtered_df = filtered_df[
            (filtered_df['median_income'] > 2.5) & 
            (filtered_df['median_income'] < 4.5)
        ]
    elif income_level == "High (≥4.5)":
        filtered_df = filtered_df[filtered_df['median_income'] >= 4.5]
    
    return filtered_df

filtered_df = filter_data(df, price_range, selected_locations, income_level)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", len(filtered_df))
with col2:
    st.metric("Average Price", f"${filtered_df['median_house_value'].mean():,.0f}")
with col3:
    st.metric("Average Income", f"${filtered_df['median_income'].mean():.2f}")

st.subheader("Housing Data Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_df,
    get_position=["longitude", "latitude"],
    get_color=[255, 0, 0, 160],
    get_radius=1000,
    pickable=True
)

view_state = pdk.ViewState(
    longitude=filtered_df['longitude'].mean(),
    latitude=filtered_df['latitude'].mean(),
    zoom=5,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Median Value:</b> {median_house_value} <br/> "
                "<b>Income:</b> {median_income} <br/> "
                "<b>Location:</b> {ocean_proximity}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
)

st.pydeck_chart(r)

st.subheader("Median House Value Distribution")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(filtered_df['median_house_value'], bins=30, alpha=0.7, color='steelblue', edgecolor='black')
ax.set_xlabel('Median House Value ($)')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Median House Values')
ax.grid(True, alpha=0.3)

mean_price = filtered_df['median_house_value'].mean()
median_price = filtered_df['median_house_value'].median()
ax.axvline(mean_price, color='red', linestyle='--', label=f'Mean: ${mean_price:,.0f}')
ax.axvline(median_price, color='green', linestyle='--', label=f'Median: ${median_price:,.0f}')
ax.legend()

st.pyplot(fig)

with st.expander("View Raw Data"):
    st.dataframe(filtered_df)

st.sidebar.markdown("---")
st.sidebar.subheader("Current Filters")
st.sidebar.write(f"**Price Range:** ${price_range[0]:,} - ${price_range[1]:,}")
st.sidebar.write(f"**Location Types:** {', '.join(selected_locations)}")
st.sidebar.write(f"**Income Level:** {income_level}")
st.sidebar.write(f"**Filtered Records:** {len(filtered_df)}")

st.markdown("---")
st.markdown("Data Source: California Housing Data (1990)")