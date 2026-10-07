import streamlit as st
import pandas as pd

# Set the main page title
st.title("🚢 Data Explorer App - Part 1")
st.write("Upload a CSV file to inspect the raw data and summary statistics.")

# File Uploader Component
uploaded_file = st.file_uploader("Choose a CSV file:", type=["csv"])
st.write(uploaded_file)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")