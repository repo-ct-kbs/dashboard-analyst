import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta



def gm_003(transactions_df, rooms_df, hotel_df):
    today = datetime.today().date()

    current_check_in = transactions_df[transactions_df['check_in_time'].dt.date == today]
    current_check_out = transactions_df[transactions_df['check_out_time'].dt.date == today]

    check_in_count = current_check_in.shape[0]
    check_out_count = current_check_out.shape[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Current Check-ins", value=str(check_in_count), delta=f"{check_in_count} Today")

    with col2:
        st.metric(label="Current Check-outs", value=str(check_out_count), delta=f"{check_out_count} Today")