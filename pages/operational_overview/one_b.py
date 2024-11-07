import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def one_b(transactions_df, rooms_df, selected_hotel):
    st.title('Room availability')
    st.write('Menampilkan dalam bentuk grafik jumlah ketersedian kamar di setiap harinya dalam rentang 1 bulan')
    filter_col = st.columns(2)
    with filter_col[0]:
        year_selection = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist(), key='year_2')
    with filter_col[1]:
        month_selection = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], key='month_2')

    df_filtered = transactions_df[transactions_df['check_in_time'].dt.year == year_selection]
    df_filtered = df_filtered[df_filtered['check_in_time'].dt.month_name() == month_selection]

    month_number = datetime.strptime(month_selection, "%B").month
    days_in_month = (datetime(year_selection, month_number % 12 + 1, 1) - pd.DateOffset(days=1)).day

    day_occupancy_counts = []

    for _, row in df_filtered.iterrows():
        check_in = row['check_in_time'].date()
        check_out = row['check_out_time'].date()

        start_of_month = datetime(year_selection, month_number, 1).date()
        end_of_month = datetime(year_selection, month_number, days_in_month).date()

        for day in pd.date_range(start=start_of_month, end=end_of_month):
            if check_in <= day.date() < check_out:
                day_occupancy_counts.append({'day': day.date(), 'hotel_name': row['hotel_name'], 'occupancy_count': 1})

    day_occupancy_counts_df = pd.DataFrame(day_occupancy_counts)

    day_occupancy_counts_df = day_occupancy_counts_df.groupby(['day', 'hotel_name'])['occupancy_count'].sum().reset_index()

    all_days = pd.date_range(start=start_of_month, end=end_of_month).date
    all_days_df = pd.DataFrame({'day': all_days})

    full_day_occupancy_df = pd.merge(all_days_df, day_occupancy_counts_df, on='day', how='left').fillna({'occupancy_count': 0})

    room_df_filtered = rooms_df.groupby('hotel_name')['room_available'].sum().reset_index()

    full_day_occupancy_df = pd.merge(full_day_occupancy_df, room_df_filtered, on='hotel_name', how='left')

    full_day_occupancy_df['remaining_rooms'] = full_day_occupancy_df['room_available'] - full_day_occupancy_df['occupancy_count']

    fig = px.line(full_day_occupancy_df,
                x='day',
                y='remaining_rooms',
                color='hotel_name',
                labels={'day': 'Day of the Month', 'remaining_rooms': 'Remaining Rooms'},
                title=f"Remaining Rooms per Day for {month_selection} {year_selection}",
                )

    fig.update_xaxes(tickmode='array', tickvals=full_day_occupancy_df['day'], ticktext=[str(d.day) for d in full_day_occupancy_df['day']])
    fig.update_layout(
    
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig)
    st.divider()