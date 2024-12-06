import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_004(transactions_df, rooms_df, hotel_df):
    today = datetime.today().date()
    end_of_week = today + timedelta(days=7)

    current_week_reservations = transactions_df[
        (transactions_df['check_in_time'].dt.date >= today) &
        (transactions_df['check_in_time'].dt.date <= end_of_week)
    ]

    current_reservations = current_week_reservations[
        (current_week_reservations['check_in_time'].dt.date <= today) &
        (current_week_reservations['check_out_time'].dt.date >= today)
    ]

    upcoming_reservations = current_week_reservations[
        current_week_reservations['check_in_time'].dt.date > today
    ]

    current_count = current_reservations.shape[0]
    upcoming_count = upcoming_reservations.shape[0]

    data = pd.DataFrame({
        'Status': ['Current Reservations', 'Upcoming Reservations'],
        'Count': [current_count, upcoming_count]
    })

    fig = px.pie(
        data,
        values='Count',
        names='Status',
        color='Status',
        color_discrete_map={
            'Current Reservations': 'blue',
            'Upcoming Reservations': 'green'
        },
        title='Guest Reservations Summary (This Week)'
    )

    fig.update_traces(
        textinfo='label+percent',
        hoverinfo='label+value',
        hole=0.4
    )

    st.title("Front Office Summary (This Week)")
    st.plotly_chart(fig)

    st.write(f"**Current Reservations:** {current_count}")
    st.write(f"**Upcoming Reservations:** {upcoming_count}")