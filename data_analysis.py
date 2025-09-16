import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Set up
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
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
