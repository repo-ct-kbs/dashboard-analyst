import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def plot_daily(transaction_df, selected_room_type):
    transaction_df['booking_time'] = pd.to_datetime(transaction_df['booking_time'])

    one_week_ago = pd.Timestamp.now() - pd.Timedelta(days=7)
    filtered_df = transaction_df[transaction_df['booking_time'] >= one_week_ago]

    if selected_room_type != 'All':
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]

    filtered_df['date'] = filtered_df['booking_time'].dt.date
    revenue_by_date = filtered_df.groupby('date')['price'].sum().reset_index()

    fig = px.bar(
        revenue_by_date,
        x='date',
        y='price',
        labels={'date': 'Date', 'price': 'Revenue'},
        title='Daily Revenue for the Past Week',
        text='price'
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Amount of Revenue',
        showlegend=False
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig


def plot_weekly(transaction_df, selected_year, selected_room_type):
    transaction_df['booking_time'] = pd.to_datetime(transaction_df['booking_time'])
    transaction_df = transaction_df[transaction_df['booking_time'].dt.year == selected_year]
    transaction_df['week'] = transaction_df['booking_time'].dt.to_period('W-SUN').apply(lambda r: r.start_time)

    if selected_room_type != "All":
        transaction_df = transaction_df[transaction_df['room_type'] == selected_room_type]

    weekly_revenue = transaction_df.groupby('week')['price'].sum().reset_index()
    fig = px.bar(
        weekly_revenue,
        x='week',
        y='price',
        labels={'week': 'Week', 'price': 'Weekly Revenue'},
        title=f'Weekly Revenue - {selected_year}',
        text='price'
    )
    fig.update_layout(
        xaxis_title='Week',
        yaxis_title='Revenue',
        showlegend=False
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig

def plot_monthly(transaction_df, selected_year, selected_room_type):
    transaction_df['booking_time'] = pd.to_datetime(transaction_df['booking_time'])
    transaction_df = transaction_df[transaction_df['booking_time'].dt.year == selected_year]
    transaction_df['month'] = transaction_df['booking_time'].dt.to_period('M').astype(str)

    if selected_room_type != "All":
        transaction_df = transaction_df[transaction_df['room_type'] == selected_room_type]

    monthly_revenue = transaction_df.groupby('month')['price'].sum().reset_index()
    fig = px.bar(
        monthly_revenue,
        x='month',
        y='price',
        labels={'month': 'Month', 'price': 'Monthly Revenue'},
        title=f'Monthly Revenue - {selected_year}',
        text='price'
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Revenue',
        showlegend=False
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig




def gm_017(transactions_df, rooms_df, hotel_df, selected_hotel):
    room_types = ['All'] + transactions_df['room_type'].unique().tolist()
    selected_room_type = st.selectbox("Select Room Type", room_types)

    fig = plot_daily(transactions_df, selected_room_type)
    st.plotly_chart(fig)

    years = transactions_df['booking_time'].dt.year.unique().tolist()
    selected_year = st.selectbox("Select Year", years, key='gm_0017_year')

    fig_weekly = plot_weekly(transactions_df, selected_year, selected_room_type)
    st.plotly_chart(fig_weekly)

    fig_monthly = plot_monthly(transactions_df, selected_year, selected_room_type)
    st.plotly_chart(fig_monthly)
