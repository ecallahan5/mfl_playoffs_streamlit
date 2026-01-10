import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
import requests
import re
import io
from google.auth.transport.requests import Request

round_select = st.radio(
    "Choose the Round to View",
    ('Wild Card', 'Divisional', 'Conference', 'Super Bowl'))

# Helper function to get spreadsheet ID
def get_spreadsheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    return match.group(1) if match else None

# Function to load data from Google Sheets via CSV export
@st.cache_data(ttl=600)
def load_data(sheet_url):
    spreadsheet_id = get_spreadsheet_id(sheet_url)
    if not spreadsheet_id:
        st.error(f"Invalid Google Sheet URL: {sheet_url}")
        return pd.DataFrame()

    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )

    if not credentials.valid:
        credentials.refresh(Request())

    token = credentials.token

    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(export_url, headers=headers)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def process_round_results(sheet_url, title):
    df = load_data(sheet_url)
    st.subheader(title)
    fig = px.pie(df, values='title_chance', names='Team', title=title)
    st.plotly_chart(fig, use_container_width=True)
    st.bar_chart(df, x='Team', y='title_chance')
    return df, fig

sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
wc_sheet_url = st.secrets["gsheets"]["wc_data_url"]
div_sheet_url = st.secrets["gsheets"]["div_data_url"]
conf_sheet_url = st.secrets["gsheets"]["conf_data_url"]

sheets_df = load_data(sheet_url)

st.header('2026 On The Door Forecasts')
st.divider()

st.header('Title Chances!')

fig = px.pie(sheets_df, values='prob', names='Team')
st.plotly_chart(fig, use_container_width=True)

sheets_df = sheets_df.rename(columns={"franchise_name" : "Team", "Champ" : "Probability"})
st.bar_chart(sheets_df, x='Team', y='title_chance')

# Update with Wild Card Results
wc_df, fig1 = process_round_results(wc_sheet_url, 'Before Divisional Week')

# Update with Division Round Results
div_df, fig2 = process_round_results(div_sheet_url, 'Before Conference Championship Week')

# Update with Conference Final Results
conf_df, fig3 = process_round_results(conf_sheet_url, 'Before Super Bowl')

if round_select == 'Wild Card':
    st.plotly_chart(fig, use_container_width=True)
elif round_select == 'Divisional':
    st.plotly_chart(fig1, use_container_width=True)
elif round_select == 'Conference':
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.plotly_chart(fig3, use_container_width=True)
