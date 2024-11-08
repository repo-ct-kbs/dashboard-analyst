import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def two_a(transactions_df, rooms_df, selected_hotel):
    st.title('Guest reservations (current and upcoming).')
    st.write('Menampilkan dalam bentuk grafik jumlah reservasi yang terjadi di setiap harinya dalam rentang 1 bulan')

    if selected_hotel == 'All':
        df = transactions_df
    else:
        df = transactions_df[transactions_df['hotel_name'] == selected_hotel]


    filter_col = st.columns(2)
    with filter_col[0]:
        selected_year = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist(), key='two_a_1_year')
    with filter_col[1]:
        selected_month = st.selectbox("Month", list(calendar.month_name[1:]), key='two_a_1_month')
    
    df['check_in_schedule'] = pd.to_datetime(df['check_in_schedule'])
    month_num = list(calendar.month_name[1:]).index(selected_month) + 1
    df_filtered = df[(df['check_in_schedule'].dt.year == selected_year) & (df['check_in_schedule'].dt.month == month_num)]

    start_of_month = datetime(selected_year, month_num, 1)
    end_of_month = datetime(selected_year, month_num, calendar.monthrange(selected_year, month_num)[1])
    date_range = pd.date_range(start=start_of_month, end=end_of_month, freq='D')

    check_in_counts = df_filtered['check_in_schedule'].dt.floor('D').value_counts().reindex(date_range, fill_value=0)

    colors = ['green' if date.date() > datetime.now().date() else 'blue' for date in check_in_counts.index]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=check_in_counts.index,
        y=check_in_counts.values,
        name="Check-ins",
        marker_color=colors
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers', marker=dict(color='blue'),
        name='Past/Current Dates'
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers', marker=dict(color='green'),
        name='Future Dates'
    ))

    fig.update_layout(
        title=f"Daily Check-ins for {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis_title="Count",
        xaxis=dict(
            tickmode='array',
            tickvals=date_range,
            ticktext=[date.strftime('%d') for date in date_range]
        ),
        bargap=0.3,
        bargroupgap=0,
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