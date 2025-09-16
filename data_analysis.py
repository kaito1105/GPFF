import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
import gspread
from google.oauth2 import service_account

# Set up
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)

sheet_id = "1K9uav-ldWAqZIyuoKdsAEB3i3ElNka2le7buThgkp7w"
sheet = client.open_by_key(sheet_id).sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

# Web app
st.title("Presentation Analysis")
st.subheader("Raw Data")
st.write(df.head())
st.write("Total Rows: ", df.shape[0])
st.write("Total Columns: ", df.shape[1])
