import streamlit as st
import pandas as pd

# Set the main page title
st.title("🚢 Data Explorer App - Part 1")
st.write("Upload a CSV file to inspect the raw data and summary statistics.")

# File Uploader Component
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("1. Raw Data Preview")
    st.write("You can click on column headers to sort the data!")
    st.dataframe(df)