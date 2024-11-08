import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def two_b(transactions_df, rooms_df, selected_hotel):
    st.title('Average Length of Stay (ALOS).')
    st.write('Menampilkan dalam bentuk grafik rata-rata lama tamu menginap per bulannya dalam rentang 1 tahun')

    if selected_hotel == 'All':
        df = transactions_df
    else:
        df = transactions_df[transactions_df['hotel_name'] == selected_hotel]

    selected_year = st.selectbox("Year", df['check_in_time'].dt.year.unique().tolist(), key='two_b_year')

    df = df[df['check_in_time'].dt.year == selected_year]

    monthly_alos = {}

    for month in range(1, 13):
        monthly_data = df[df['check_in_time'].dt.month == month]
        
        total_night_stays = monthly_data['night_stay'].sum()

        total_bookings = len(monthly_data)

        if total_bookings > 0:
            alos = total_night_stays / total_bookings
        else:
            alos = 0

        month_name = calendar.month_name[month]
        monthly_alos[month_name] = alos

    month_alos_counts = pd.DataFrame(list(monthly_alos.items()), columns=['month_name', 'alos'])

    month_alos_counts['month_name'] = pd.Categorical(month_alos_counts['month_name'], 
                                                    categories=calendar.month_name[1:], 
                                                    ordered=True)
    month_alos_counts = month_alos_counts.sort_values('month_name')

    fig = px.bar(month_alos_counts, 
                x='month_name', 
                y='alos', 
                labels={'month_name': 'Month', 'alos': 'Average Length of Stay (ALOS)'},
                title=f"Average Length of Stay (ALOS) per Month in {selected_year}")

    st.plotly_chart(fig)

    st.divider()