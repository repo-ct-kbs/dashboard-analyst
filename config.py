import json
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

fixed_range = datetime.datetime(day=31, month=12, year=2024)
selected_hotel = 'All'

def render_image(title, fig):
    st.plotly_chart(fig)


def df_transactions():
    global selected_hotel
    rooms = df_hotels()
    rooms_df = rooms[0]
    hotel_df = rooms[1]
    
    df = pd.read_json('hotel_booking_history-4.json')

    hotel_options = ["All"] + [hotel['name'] for hotel in hotel_df]
    selected_hotel = st.selectbox("Select Hotel", hotel_options)

    df['booking_time'] = pd.to_datetime(df['booking_time'])
    df['check_in_time'] = pd.to_datetime(df['check_in_time'])
    df['check_out_time'] = pd.to_datetime(df['check_out_time'])
    df['check_in_schedule'] = pd.to_datetime(df['check_in_schedule'])
    df['check_out_schedule'] = pd.to_datetime(df['check_out_schedule'])

    if selected_hotel == "All":
        df = df
    else:
        df = df[df['hotel_name'] == selected_hotel]

    # df = df[(df['booking_time'] >= pd.Timestamp(start_date)) & (df['booking_time'] <= pd.Timestamp(end_date))]
    return [df, selected_hotel]

def df_hotels():
    global selected_hotel
    with open('hotel_set.json', 'r') as file:
        datas = json.load(file)
    
        rooms_df = pd.DataFrame([
            {"hotel_name": hotel["name"], "room_type": room["room_type"], "room_available": room["rooms"]}
            for hotel in datas for room in hotel["rooms"]
        ])

        if selected_hotel == 'All':
            return [rooms_df, datas]
        else:
            rooms_df = rooms_df[rooms_df['hotel_name'] == selected_hotel]
            datas = datas
            return [rooms_df, datas]

def daterange():
    start_year = 2018
    today = fixed_range
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