import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing Data (1990)", layout="wide")

st.title("California Housing Data (1990)")
st.markdown("### Explore Median House Value in California Housing Data")

@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

min_price = int(df["median_house_value"].min())
max_price = int(df["median_house_value"].max())

price_filter = st.slider(
    "Select Minimum Median House Value",
    min_price,
    max_price,
    200000  
)

filtered_df = df[df["median_house_value"] >= price_filter]

st.sidebar.header("Filters")

location_types = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    "Choose Location Type",
    options=location_types,
    default=location_types
)

filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

income_level = st.sidebar.radio(
    "Choose Income Level",
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
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(
    filtered_df["median_house_value"],
    bins=30,
    color="#2E86C1",     
    edgecolor="white",    
    linewidth=0.8,
    alpha=0.9
)
ax.set_title("Distribution of Median House Value", fontsize=14, weight="bold")
ax.set_xlabel("Median House Value ($)", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.grid(alpha=0.3)

st.pyplot(fig)

st.markdown("---")
st.markdown("**Filters Applied:**")
st.write(f"- Minimum Median House Value: ${price_filter}")
st.write(f"- Location Type: {', '.join(selected_locations)}")
st.write(f"- Income Level: {income_level}")

st.markdown("Use the sidebar to explore California housing data interactively!")
