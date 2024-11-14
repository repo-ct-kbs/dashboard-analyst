import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import df_hotels, df_transactions
from pages.operational_overview.four_a import four_a
from pages.operational_overview.four_b import four_b
from pages.operational_overview.four_c import four_c


transactions_df = df_transactions()
rooms = df_hotels()
rooms_df = rooms[0]

hotel_names = ['All'] + [hotel['name'] for hotel in rooms[1]]
selected_hotel = st.selectbox("Select a Hotel", hotel_names, key='')
st.divider()


four_a(transactions_df, rooms_df, selected_hotel)

four_b(transactions_df, rooms_df, selected_hotel)

four_c(transactions_df, rooms_df, selected_hotel)