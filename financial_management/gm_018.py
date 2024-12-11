import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def get_total_available_rooms(hotel_df):
    total_available_rooms = 0
    for hotel in hotel_df:
        for room in hotel['rooms']:
            total_available_rooms += room['rooms']
    return total_available_rooms


def calculate_revpar(transaction_df, hotel_df, period):
    total_available_rooms = get_total_available_rooms(hotel_df)

    transaction_df['booking_time'] = pd.to_datetime(transaction_df['booking_time'])
    transaction_df['month'] = transaction_df['booking_time'].dt.month
    transaction_df['week'] = transaction_df['booking_time'].dt.isocalendar().week

    total_revenue = transaction_df.groupby(period)['price'].sum().reset_index(name='total_revenue')
    total_revenue['revpar'] = total_revenue['total_revenue'] / total_available_rooms

    return total_revenue


def plot_gauge_chart(current_revpar, target_revpar):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_revpar,
        delta={'reference': target_revpar, 'position': "top"},
        gauge={
            'axis': {'range': [0, target_revpar * 1.5]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, target_revpar * 0.5], 'color': "lightgray"},
                {'range': [target_revpar * 0.5, target_revpar], 'color': "yellow"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target_revpar}
        },
        title={'text': "Current RevPAR"}
    ))
    return fig

def plot_bar_chart(revpar_data, period_name):
    fig = px.bar(
        revpar_data,
        x=period_name,
        y='revpar',
        labels={period_name: period_name.capitalize(), 'revpar': 'RevPAR'},
        title=f"{period_name.capitalize()} RevPAR",
        text='revpar'
    )
    fig.update_layout(
        xaxis_title=period_name.capitalize(),
        yaxis_title='RevPAR',
        showlegend=False
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig

def gm_018(transactions_df, rooms_df, hotel_df, selected_hotel):
    

    room_types = ['All'] + [room['room_type'] for hotel in hotel_df for room in hotel['rooms']]
    selected_room_type = st.selectbox("Select Room Type", room_types)

    if selected_room_type != "All":
        filtered_transaction_df = transactions_df[transactions_df['room_type'] == selected_room_type]
    else:
        filtered_transaction_df = transactions_df

    monthly_revpar = calculate_revpar(filtered_transaction_df, hotel_df, period='month')

    current_revpar = monthly_revpar['revpar'].iloc[-1]
    target_revpar = 500000

    st.write("### Current RevPAR")
    gauge_fig = plot_gauge_chart(current_revpar, target_revpar)
    st.plotly_chart(gauge_fig)

    st.write("### Monthly RevPAR")
    monthly_fig = plot_bar_chart(monthly_revpar, 'month')
    st.plotly_chart(monthly_fig)