import json
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_image(title, fig):
    st.plotly_chart(fig)


def df_transactions():
    st.title('Pilih Rentang Tanggal')
    
    df = pd.read_json('hotel_booking_history-2.json')
    df['booking_time'] = pd.to_datetime(df['booking_time'])
    df['check_in_time'] = pd.to_datetime(df['check_in_time'])
    df['check_out_time'] = pd.to_datetime(df['check_out_time'])

    start_date, end_date = daterange()
    df = df[(df['booking_time'] >= pd.Timestamp(start_date)) & (df['booking_time'] <= pd.Timestamp(end_date))]
    return df

def df_hotels():
    with open('hotel_set.json', 'r') as file:
        datas = json.load(file)
    
        rooms_df = pd.DataFrame([
            {"hotel_name": hotel["name"], "room_type": room["room_type"], "room_available": room["rooms"]}
            for hotel in datas for room in hotel["rooms"]
        ])
        return [rooms_df, datas]

def daterange():
    start_year = 2020
    today = datetime.datetime.now()
    current_year = today.year

    col = st.columns(2)

    with col[0]:
        start_date = st.date_input(
            "Start Date",
            datetime.date(start_year, 1, 1),
            min_value=datetime.date(start_year, 1, 1),
            max_value=datetime.date(current_year, 12, 31),
            format="DD.MM.YYYY",
        )

    with col[1]:
        end_date = st.date_input(
            "End Date",
            datetime.date.today(),
            min_value=start_date,
            max_value=datetime.date(current_year, 12, 31),
            format="DD.MM.YYYY",
        )

    return start_date, end_date