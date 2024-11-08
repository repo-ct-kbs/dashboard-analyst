import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def two_c(transactions_df, rooms_df, selected_hotel):
    st.title('Daily revenue and ADR (Average Daily Rate).')
    st.write('Menampilkan dalam bentuk grafik jumlah pendapatan dan  rata-rata pendapatan dari seluruh kamar yang terisi pada hari berjalan (dihitung dari yang checkin pada hari tersebut)')

    selected_hotel = st.selectbox("Select Hotel", transactions_df['hotel_name'].unique())
    df = transactions_df[transactions_df['hotel_name'] == selected_hotel]

    selected_year = st.selectbox("Year", df['check_in_time'].dt.year.unique().tolist())
    df = df[df['check_in_time'].dt.year == selected_year]

    color_map = {
        'Family': 'red',
        'Deluxe': 'blue',
        'Suite': 'purple',
        'Standard': 'orange',
        'Regular': 'green',
        'Fancy': 'purple',
        'Presidential': 'brown',
        'Double': 'cyan'
    }

    monthly_revenue_data = []
    for month in range(1, 13):
        monthly_data = df[df['check_in_time'].dt.month == month]
        if not monthly_data.empty:
            month_name = calendar.month_name[month]
            
            for room_type in monthly_data['room_type'].unique():
                room_type_data = monthly_data[monthly_data['room_type'] == room_type]
                total_revenue = (room_type_data['price'] * room_type_data['night_stay']).sum()
                adr = total_revenue / room_type_data['night_stay'].sum() if room_type_data['night_stay'].sum() > 0 else 0
                monthly_revenue_data.append({'Month': month_name, 'Room Type': room_type, 'Total Revenue': total_revenue, 'ADR': adr})

    monthly_revenue_df = pd.DataFrame(monthly_revenue_data)

    fig = px.bar(
        monthly_revenue_df,
        x='Month',
        y='Total Revenue',
        color='Room Type',
        barmode='group',
        color_discrete_map=color_map,
        labels={'Total Revenue': 'Revenue (IDR)'},
        title=f"Daily Revenue and ADR by Room Type for {selected_year}"
    )
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

    annual_revenue_by_room_type = monthly_revenue_df.groupby('Room Type')['Total Revenue'].sum().reset_index()
    fig_pie = px.pie(
        annual_revenue_by_room_type,
        names='Room Type',
        values='Total Revenue',
        title=f"Revenue Share by Room Type for {selected_year}",
        hole=0.4
    )

    fig_pie.for_each_trace(lambda trace: trace.update(marker=dict(colors=[color_map[room] for room in annual_revenue_by_room_type['Room Type']])))

    fig_pie.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig_pie)


    st.divider()