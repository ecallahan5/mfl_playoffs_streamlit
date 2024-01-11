import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
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

sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
sheets_df = pd.DataFrame(run_query(f'SELECT * FROM "{sheet_url}"'))

st.header('2023 On The Door Forecasts')
st.markdown("""---""")

st.header('Title Chances!')
fig = px.pie(sheets_df, values='prob', names='Team', title='Before Wild Card Week')
st.plotly_chart(fig, use_container_width=True)


# # Update with Wild Card Results
# wc_sheet_url = st.secrets["gsheets"]["wc_data_url"]
# wc_df = pd.DataFrame(run_query(f'SELECT * FROM "{wc_sheet_url}"'))

# fig1 = px.pie(wc_df, values='title_chance', names='Team', title='Before Divisional Week')
# # st.plotly_chart(fig1, use_container_width=True)

# # Update with Division Round Results
# div_sheet_url = st.secrets["gsheets"]["div_data_url"]
# div_df = pd.DataFrame(run_query(f'SELECT * FROM "{div_sheet_url}"'))

# fig2 = px.pie(div_df, values='title_chance', names='Team', title='Before Conference Champ Week')

# # Update with Conference Final Results

# conf_sheet_url = st.secrets["gsheets"]["conf_data_url"]
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
