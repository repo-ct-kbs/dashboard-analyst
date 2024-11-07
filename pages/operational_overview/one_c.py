import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def one_c(transactions_df):
    st.title('Guest check-ins and check-outs.')
    st.write('Menampilkan dalam bentuk grafik jumlah guest check in dan check out di setiap harinya dalam rentang 1 bulan')

    filter_col = st.columns(2)
    with filter_col[0]:
        selected_year = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist(), key='year_3')
    with filter_col[1]:
        selected_month = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], key='month_3')

    df = transactions_df
    df['check_in_time'] = pd.to_datetime(df['check_in_time'])
    df['check_out_time'] = pd.to_datetime(df['check_out_time'])

    month_num = list(calendar.month_name[1:]).index(selected_month) + 1
    df_filtered = df[(df['check_in_time'].dt.year == selected_year) & (df['check_in_time'].dt.month == month_num)]

    start_of_month = datetime(selected_year, month_num, 1)
    end_of_month = datetime(selected_year, month_num, calendar.monthrange(selected_year, month_num)[1])
    date_range = pd.date_range(start=start_of_month, end=end_of_month, freq='D')

    check_in_counts = df_filtered['check_in_time'].dt.floor('D').value_counts().reindex(date_range, fill_value=0)
    check_out_counts = df_filtered['check_out_time'].dt.floor('D').value_counts().reindex(date_range, fill_value=0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=check_in_counts.index,
        y=check_in_counts.values,
        name="Check-ins",
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=check_out_counts.index,
        y=check_out_counts.values,
        name="Check-outs",
        marker_color='red'
    ))

    fig.update_layout(
        title=f"Daily Check-ins and Check-outs for {selected_month} {selected_year}",
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