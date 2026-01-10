import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
import collections
import collections.abc
# Patch for collections.Iterable compatibility with Python 3.10+
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable
from gsheetsdb import connect

round_select = st.radio(
    "Choose the Round to View",
    ('Wild Card', 'Divisional', 'Conference', 'Super Bowl'))

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)
# @st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def process_round_results(sheet_url, title):
    df = pd.DataFrame(run_query(f'SELECT * FROM "{sheet_url}"'))
    st.subheader(title)
    fig = px.pie(df, values='title_chance', names='Team', title=title)
    st.plotly_chart(fig, use_container_width=True)
    st.bar_chart(df, x='Team', y='title_chance')
    return df, fig

sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
wc_sheet_url = st.secrets["gsheets"]["wc_data_url"]
div_sheet_url = st.secrets["gsheets"]["div_data_url"]
conf_sheet_url = st.secrets["gsheets"]["conf_data_url"]

sheets_df = pd.DataFrame(run_query(f'SELECT * FROM "{sheet_url}"'))

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
