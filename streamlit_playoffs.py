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
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.index} has a :{row.chance}:")

st.header('Wide Right Playoffs')
st.markdown("""---""")

st.header('Championship Bracket')
champ = pd.DataFrame({
     'Team': ["The Van Buren Boys", "Moneyballers"],
     'Win Probability': [53.86, 46.14]
     })
fig = px.pie(champ, values='Win Probability', names='Team', title='Championship Game')
st.plotly_chart(fig, use_container_width=True)

third = pd.DataFrame({
     'Team': ["Brooklyn Big Blue", "The Uncaught Exceptions"],
     'Win Probability': [61.71, 38.29]
     })
fig = px.pie(third, values='Win Probability', names='Team', title='Third Place')
st.plotly_chart(fig, use_container_width=True)

# st.header('Road to the Title!')
# fig = go.Figure(data=[go.Sankey(

#     # Define nodes
#     node = dict(
#       pad = 50,
#       thickness = 5,
#       line = dict(color = "black", width = 0.5),
#       label =  ["Brooklyn Big Blue", "The Uncaught Exceptions", "Moneyballers", "The Van Buren Boys", "Championship Game", "Consolation Game", \
#               "1st Place", "2nd Place", "3rd Place", "4th Place"],
#       color =  ["Blue", "Red", "Green", "Purple"]
#     ),
#     # Add links
#     link = dict(
#       source =  [0, 0, 1, 1, 2, 2, 3, 3, 4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,],
#       target =  [4, 5, 4, 5, 4, 5, 4, 5, 6,7,8,9, 6,7,8,9, 6,7,8,9, 6,7,8,9],
#       value =  [70, 30, 65, 35, 35, 65, 30, 70, 47, 23, 21, 9, 29, 36, 19, 16, 11, 24, 26, 39, 13, 17, 34, 36 ],
#       label =  ["Brooklyn Big Blue Wins", "Brooklyn Big Blue Loses", "The Uncaught Exceptions Wins", "The Uncaught Exceptions Loses", \
#                "Moneyballers Wins", "Moneyballers Loses", "The Van Buren Boys Wins", "The Van Buren Boys",
#                "Brooklyn Big Blue 1st", "Brooklyn Big Blue 2nd", "Brooklyn Big Blue 3rd", "Brooklyn Big Blue 4th", \
#                "The Uncaught Exceptions 1st", "The Uncaught Exceptions 2nd", "The Uncaught Exceptions 3rd", "The Uncaught Exceptions 4th", \
#                "Moneyballers 1st", "Moneyballers 2nd", "Moneyballers 3rd", "Moneyballers 4th", \
#                "The Van Buren Boys 1st", "The Van Buren Boys 2nd", "The Van Buren Boys 3rd", "The Van Buren Boys 4th"   ],
#       color =  ["Blue", "Blue", "Red", "Red", "Green", "Green", "Purple", "Purple", \
#                   "Blue", "Blue", "Blue", "Blue", "Red", "Red", "Red", "Red", \
#                     "Green", "Green", "Green", "Green",  "Purple", "Purple", "Purple", "Purple"]
# ))])
   
# fig.update_layout(title_text="Championship Bracket",
#                   font_size=10)
# st.plotly_chart(fig, use_container_width=False)

# st.header('This Week\'s Games')

# wc1 = pd.DataFrame({
#      'Team': ["Maize 'N Blue", "Moneyballers"],
#      'Win Probability': [56.37, 43.63]
#      })
# fig = px.pie(wc1, values='Win Probability', names='Team', title='Wild Card 1')
# st.plotly_chart(fig, use_container_width=True)

# wc2 = pd.DataFrame({
#      'Team': ["The Gurley Tates", "The Van Buren Boys"],
#      'Win Probability': [37.09, 62.91]
#      })
# fig = px.pie(wc2, values='Win Probability', names='Team', title='Wild Card 2')
# st.plotly_chart(fig, use_container_width=True)

# # Add consolation bracket games?

# st.markdown("""---""")
# st.header('Title Chances')
# df_ch = pd.DataFrame({
#      'Team': ["Moneyballers",  "The Van Buren Boys",  "Brooklyn Big Blue", "The Uncaught Exceptions"],
#      'Probability': [11.44, 13.11, 46.95, 28.50]
#      })

# st.bar_chart(df_ch, x='Team', y='Probability')

st.markdown("""---""")
st.header('Expected Playoff Winnings')
df_money = pd.DataFrame({
     'Team': [ "Moneyballers", "The Van Buren Boys",  "Brooklyn Big Blue", "The Uncaught Exceptions"],
     '$$': [241, 254, 37, 23]
     })
st.bar_chart(df_money, x='Team', y='$$')


st.markdown("""---""")
st.header('Extra Pick!')
# dfl = pd.DataFrame({
#      'Team': ["You Carr'd Be Kidding", "Hidden Talents", "Hurricane",  "Shoot em Into the Sun"],
#      'Probability': [37.05, 33.88, 21.13, 7.94]
#      })
# st.bar_chart(dfl, x='Team', y='Probability')

pick = pd.DataFrame({
     'Team': ["Hidden Talents", "Hurricane"],
     'Win Probability': [52, 48]
     })
fig = px.pie(pick, values='Win Probability', names='Team', title='Extra Pick')
st.plotly_chart(fig, use_container_width=True)

####################




