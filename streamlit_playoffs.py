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
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
sheets_df = run_query(f'SELECT * FROM "{sheet_url}"')


st.header('2023 On The Door Forecasts')
st.markdown("""---""")

st.header('Title Chances!')
# champ = pd.DataFrame({
#      'Team': ["01", "02", "03", "04", "05", "06", "07"],
#      'Win Probability': [10, 20, 10, 15, 25, 5, 15]
#      })
fig = px.pie(sheets_df, values='Win Probability', names='Team', title='Title Chances')
st.plotly_chart(fig, use_container_width=True)
