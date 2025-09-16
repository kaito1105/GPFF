import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
import gspread
from google.oauth2 import service_account # web app
from google.oauth2.service_account import Credentials # localhost

################### Set up ###################
# Web app creds
# creds = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=["https://www.googleapis.com/auth/spreadsheets",
#             "https://www.googleapis.com/auth/drive"]
# )

# Localhost creds
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json",
                                              scopes=scopes)

client = gspread.authorize(creds)
sheet_id = "1K9uav-ldWAqZIyuoKdsAEB3i3ElNka2le7buThgkp7w"
sheet = client.open_by_key(sheet_id).sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

################### Data Analysis ###################
# Web app
row_and_column = "Total Row and Column: "
st.title("GPFF Analysis Dashboard")
st.subheader("Raw Data")
st.write(df.head())
st.write(row_and_column, df.shape)
st.write(df.dtypes)

# Data clean
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
july_df = df[df["Timestamp"].dt.month == 7]

st.subheader("Cleaned Data")
st.write("Only July data for this case.")
# st.write(july_df.head())
st.write(row_and_column, july_df.shape)

july_pre_df = july_df[july_df["Survey Name"] == "Presentation Pre-Survey"]
july_post_df = july_df[july_df["Survey Name"] == "Presentation Post-Survey"]
st.write(row_and_column, july_pre_df.shape, "in pre-survey")
st.write(row_and_column, july_post_df.shape, "in post-survey")