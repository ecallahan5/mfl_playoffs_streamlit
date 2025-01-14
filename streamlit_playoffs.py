import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
from gsheetsdb import connect

# round_select = st.radio(
#     "Choose the Round to View",
#     ('Wild Card', 'Divisional', 'Conference', 'Super Bowl'))

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
wc_sheet_url = st.secrets["gsheets"]["wc_data_url"]
div_sheet_url = st.secrets["gsheets"]["div_data_url"]
conf_sheet_url = st.secrets["gsheets"]["conf_data_url"]

sheets_df = pd.DataFrame(run_query(f'SELECT * FROM "{sheet_url}"'))

st.header('2025 On The Door Forecasts')
st.divider()

st.header('Title Chances!')

# fig = px.pie(sheets_df, values='prob', names='Team')
# st.plotly_chart(fig, use_container_width=True)

# sheets_df = sheets_df.rename(columns={"franchise_name" : "Team", "Champ" : "Probability"})
# st.bar_chart(sheets_df, x='Team', y='title_chance')

# # Update with Wild Card Results
wc_df = pd.DataFrame(run_query(f'SELECT * FROM "{wc_sheet_url}"'))
st.subheader('Before Divisional Week')

# fig1 = px.pie(wc_df, values='title_chance', names='Team', title='Before Divisional Week')
st.plotly_chart(fig1, use_container_width=True)
st.bar_chart(wc_df, x='Team', y='title_chance')

# # Update with Division Round Results
# div_df = pd.DataFrame(run_query(f'SELECT * FROM "{div_sheet_url}"'))

# st.subheader('Before Conference Championship Week')
# fig2 = px.pie(div_df, values='title_chance', names='Team', title='Before Conference Champ Week')
# st.bar_chart(div_df, x='Team', y='title_chance')


# # Update with Conference Final Results

# conf_df = pd.DataFrame(run_query(f'SELECT * FROM "{conf_sheet_url}"'))

# fig3 = px.pie(conf_df, values='title_chance', names='Team', title='Before Super Bowl')

# if round_select == 'Wild Card':
#     st.plotly_chart(fig, use_container_width=True)
# if round_select == 'Divisional':
#         st.plotly_chart(fig1, use_container_width=True)
# if round_select == 'Conference':
#         st.plotly_chart(fig2, use_container_width=True)
# else:
#     st.plotly_chart(fig3, use_container_width=True)
