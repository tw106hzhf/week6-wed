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

    st.subheader("2. Dataset Shape")
    st.write(f"**Number of Rows:** {df.shape[0]}")
    st.write(f"**Number of Columns:** {df.shape[1]}")

    ## When we uncomment this and have "Always rerun" selected, the page is updated on its own

    # st.subheader("3. Dataset Information")
    # info_df = pd.DataFrame({
    #     "Column Name": df.columns,
    #     "Non-Null Count": df.notnull().sum().values,
    #     "Data Type": df.dtypes.astype(str).values
    # })
    # st.dataframe(info_df)