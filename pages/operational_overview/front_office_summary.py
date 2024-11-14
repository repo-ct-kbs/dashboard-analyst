import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import df_hotels, df_transactions
from pages.operational_overview.two_a import two_a
from pages.operational_overview.two_b import two_b
from pages.operational_overview.two_c import two_c


transactions_df = df_transactions()
rooms = df_hotels()
rooms_df = rooms[0]

hotel_names = ['All'] + [hotel['name'] for hotel in rooms[1]]
selected_hotel = st.selectbox("Select a Hotel", hotel_names, key='')
st.divider()


two_a(transactions_df, rooms_df, selected_hotel)

two_b(transactions_df, rooms_df, selected_hotel)

two_c(transactions_df, rooms_df, selected_hotel)