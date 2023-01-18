import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
from gsheetsdb import connect

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

sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
sheets_df = pd.DataFrame(run_query(f'SELECT * FROM "{sheet_url}"'))

st.header('2023 On The Door Forecasts')
st.markdown("""---""")

st.header('Title Chances!')
fig = px.pie(sheets_df, values='prob', names='Team', title='Before Wild Card Week')
st.plotly_chart(fig, use_container_width=True)

# Update with Wild Card Results
wc_sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
wc_df = pd.DataFrame(run_query(f'SELECT * FROM "{wc_sheet_url}"'))

fig = px.pie(wc_df, values='prob', names='Team', title='Before Wild Card Week')
st.plotly_chart(fig, use_container_width=True)
