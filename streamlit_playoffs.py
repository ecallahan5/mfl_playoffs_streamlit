import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.header('2023 On The Door Forecasts')
st.markdown("""---""")

st.header('Title Chances!)
champ = pd.DataFrame({
     'Team': ["01", "02", "03", "04", "05", "06", "07"],
     'Win Probability': [10, 20, 10, 15, 25, 5, 15]
     })
fig = px.pie(champ, values='Win Probability', names='Team', title='Title Chances')
st.plotly_chart(fig, use_container_width=True)