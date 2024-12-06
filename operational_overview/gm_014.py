import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from plotly_calplot import calplot, month_calplot


def gm_014(transactions_df, rooms_df, hotel_df, selected_hotel):
    top_col1, top_col2 = st.columns(2)
    bottom_col1, bottom_col2 = st.columns(2)

    hotel_filter = top_col1.multiselect("Hotel Name", transactions_df['hotel_name'].unique().tolist(), default=transactions_df['hotel_name'].unique().tolist())
    room_filter = top_col2.multiselect("Room Type", transactions_df['room_type'].unique().tolist(), default=transactions_df['room_type'].unique().tolist())
    year_filter = bottom_col1.multiselect("Year", sorted(transactions_df['check_in_schedule'].dt.year.unique().tolist()), default=sorted(transactions_df['check_in_schedule'].dt.year.unique().tolist()))
    month_filter = bottom_col2.multiselect("Month", list(range(1, 13)), default=list(range(1, 13)))

    filtered_df = transactions_df.copy()

    if hotel_filter:
        filtered_df = filtered_df[filtered_df['hotel_name'].isin(hotel_filter)]

    if room_filter:
        filtered_df = filtered_df[filtered_df['room_type'].isin(room_filter)]

    if year_filter:
        filtered_df = filtered_df[filtered_df['check_in_schedule'].dt.year.isin(year_filter)]

    if month_filter:
        filtered_df = filtered_df[filtered_df['check_in_schedule'].dt.month.isin(month_filter)]

    daily_data = filtered_df.groupby('check_in_schedule').size().reset_index(name='occupancy')


    fig = calplot(
        daily_data,
        x='check_in_schedule',
        y='occupancy',
        dark_theme=False,
        text="occupancy",
        years_title=True,
        month_lines_width=1.5,
        month_lines_color='red',
        gap=2,
        space_between_plots=0.08,
        showscale=True,
        title="Each Week"
    )

    st.plotly_chart(fig)

    fig = month_calplot(
        daily_data,
        x='check_in_schedule',
        y='occupancy',
        dark_theme=False,
        gap=2,
        showscale=True,
        title="Each Month"
    )

    st.plotly_chart(fig)


    st.divider()