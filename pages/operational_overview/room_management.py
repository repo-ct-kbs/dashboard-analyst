import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import df_hotels, df_transactions
from pages.operational_overview.five_a import five_a
from pages.operational_overview.five_b import five_b
from pages.operational_overview.five_c import five_c

transactions_df = df_transactions()
rooms = df_hotels()
rooms_df = rooms[0]

hotel_names = ['All']
selected_hotel = st.selectbox("Select a Hotel", hotel_names, key='')
st.divider()

five_a(transactions_df, rooms_df, selected_hotel)

five_b(transactions_df, rooms_df, selected_hotel)

five_c(transactions_df, rooms_df, selected_hotel)