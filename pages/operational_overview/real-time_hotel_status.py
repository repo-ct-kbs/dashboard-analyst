import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import df_hotels, df_transactions, render_image
from pages.operational_overview.one_a import one_a, one_a_b
from pages.operational_overview.one_b import one_b
from pages.operational_overview.one_c import one_c

transactions_df = df_transactions()
rooms = df_hotels()
rooms_df = rooms[0]

hotel_names = ['All'] + [hotel['name'] for hotel in rooms[1]]
selected_hotel = st.selectbox("Select a Hotel", hotel_names, key='Room Availability and Occupancy per Selected Date-selected_hotel')
st.divider()

def calculate_stay_days(check_in, check_out, start_range, end_range):
    check_in = max(check_in, start_range)
    check_out = min(check_out, end_range)
    
    if check_in <= check_out:
        return (check_out - check_in).days + 1
    else:
        return 0
    

one_a(selected_hotel, transactions_df, rooms_df)

if selected_hotel == 'All':
    transactions_df = transactions_df
else:
    transactions_df = transactions_df[transactions_df['hotel_name'] == selected_hotel]

one_a_b(transactions_df)
one_b(transactions_df, rooms_df, selected_hotel)
one_c(transactions_df)