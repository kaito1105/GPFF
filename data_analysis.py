import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import gspread
from google.oauth2 import service_account # web app
from google.oauth2.service_account import Credentials # localhost

########################### Set up ###########################
# Web app creds
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)

# Localhost creds
# scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# creds = Credentials.from_service_account_file("credentials.json",
#                                               scopes=scopes)

client = gspread.authorize(creds)
sheet_id = "1K9uav-ldWAqZIyuoKdsAEB3i3ElNka2le7buThgkp7w"
sheet = client.open_by_key(sheet_id).sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

for i, col in enumerate(df.columns):
  new_col = col.strip().replace(" ", "_").replace("-", "_")
  new_col = new_col.lower()
  df.columns.values[i] = new_col
df = df.replace("", np.nan)

########################### Data Analysis ###########################
# Web app
row_and_column = "Total Row and Column: "
st.title("GPFF Analysis Dashboard")
st.subheader("Raw Data")
st.write(df.head())
st.write(row_and_column, df.shape)
st.write(df.dtypes)

# Data clean
st.subheader("Cleaned Data")
st.write("Only July data for this case.")
df.timestamp = pd.to_datetime(df.timestamp, errors="coerce")
july_df = df[df.timestamp.dt.month == 7]
# st.write(july_df.head())
st.write(row_and_column, july_df.shape)

july_pre_df = july_df[july_df.survey_name == "Presentation Pre-Survey"]
july_post_df = july_df[july_df.survey_name == "Presentation Post-Survey"]
st.write(row_and_column, july_pre_df.shape, "in pre-survey")
st.write(row_and_column, july_post_df.shape, "in post-survey")

# Boxplot
st.subheader("Boxplot")
demographic_list = [
  "gender", "race", "education", "religious", "substance_use"
]
n = len(demographic_list)
fig, axes = plt.subplots(nrows=n, ncols=2, figsize=(14, n*6.0))
fig.subplots_adjust(hspace=1.2)

for i, demo in enumerate(demographic_list):
    # Alphabetical order for categories
    categories = sorted(july_pre_df[demo].dropna().unique())
    
    # Pre-test
    sns.boxplot(
        x=demo,
        y="test_score",
        data=july_pre_df,
        ax=axes[i,0],
        order=categories,
        color="lightcoral"
    )
    axes[i,0].set_title(f"Pre-test Score by {demo}")
    axes[i,0].set_xlabel("")
    axes[i,0].set_ylabel("")
    axes[i,0].set_ylim(bottom=0)
    axes[i,0].tick_params(axis="x", rotation=45)

    # Overlay mean dots
    grouped = july_pre_df.groupby(demo)["test_score"].mean()
    means_pre = grouped.reindex(categories)
    axes[i,0].scatter(
        x=np.arange(len(categories)),
        y=means_pre.values,
        color="black",
        s=50,
        zorder=10,
        label="Mean"
    )

    # Post-test
    sns.boxplot(
        x=demo,
        y="test_score",
        data=july_post_df,
        ax=axes[i,1],
        order=categories,
        color="skyblue"
    )
    axes[i,1].set_title(f"Post-test Score by {demo}")
    axes[i,1].set_xlabel("")
    axes[i,1].set_ylabel("")
    axes[i,1].set_ylim(bottom=0)
    axes[i,1].tick_params(axis="x", rotation=45)

    # Overlay mean dots
    grouped = july_post_df.groupby(demo)["test_score"].mean()
    means_post = grouped.reindex(categories)
    axes[i,1].scatter(
        x=np.arange(len(categories)),
        y=means_post.values,
        color="black",
        s=50,
        zorder=10,
        label="Mean"
    )

fig.tight_layout()
st.pyplot(fig)