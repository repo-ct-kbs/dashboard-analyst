import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

def calculate_room_availability(transactions_df, rooms_df, start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    room_availability = []

    for day in date_range:
        booked_rooms = transactions_df[
            (transactions_df["check_in_schedule"] <= day) &
            (transactions_df["check_out_schedule"] > day)
        ]["adults"].sum()

        total_rooms = rooms_df["room_available"].sum()
        available_rooms = total_rooms - booked_rooms
        room_availability.append({
            "date": day,
            "available": max(available_rooms, 0),
            "booked": booked_rooms
        })
    
    return pd.DataFrame(room_availability)

def gm_002(transactions_df, rooms_df, hotel_df):
    filter_options = ["Today", "This Week", "This Month"]
    selected_filter = st.selectbox("Select Filter", filter_options)

    today = datetime.now()
    if selected_filter == "Today":
        start_date = end_date = today
    elif selected_filter == "This Week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    else:
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    room_availability_df = calculate_room_availability(transactions_df, rooms_df, start_date, end_date)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=room_availability_df["date"],
        y=room_availability_df["available"],
        name="Available",
        marker_color="green",
        text=room_availability_df["available"],
        textposition="inside"
    ))

    fig.add_trace(go.Bar(
        x=room_availability_df["date"],
        y=room_availability_df["booked"],
        name="Booked",
        marker_color="red",
        text=room_availability_df["booked"],
        textposition="inside"
    ))

    fig.update_layout(
        title="Room Availability",
        barmode="stack",
        xaxis_title="Date",
        yaxis_title="Room Count",
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=-45
        ),
        legend_title="Room Status",
        uniformtext_minsize=10,
        uniformtext_mode="hide"
    )

    st.plotly_chart(fig, use_container_width=True)

