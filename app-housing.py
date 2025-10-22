import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="California Housing Data (1990)", layout="wide")

st.title("California Housing Data (1990) by Zhao Ziyu")
st.markdown("### Minimal Median House Value")


@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

min_price = int(df["median_house_value"].min())
max_price = int(df["median_house_value"].max())

price_filter = st.slider(
    "Select Minimal Median House Value",
    min_price,
    max_price,
    200000
)

filtered_df = df[df["median_house_value"] >= price_filter]

st.markdown("### See more filters in the sidebar:")
st.sidebar.header("Filters")

location_types = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

income_level = st.sidebar.radio(
    "Choose income level",
    ("Low", "Medium", "High")
)

if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)
    ]
else:
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]


st.subheader("House Locations on Map")
st.map(filtered_df[["latitude", "longitude"]])
st.subheader("Histogram of Median House Value")

sns.set(style="darkgrid")  
plt.figure(figsize=(10, 6))

plt.hist(
    filtered_df["median_house_value"],
    bins=30,
    color="#1f77b4",   
    edgecolor="none"
)

plt.xlabel("Median House Value ($)")
plt.ylabel("Count")
plt.grid(True)

st.pyplot(plt.gcf())
