import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def three_a(transactions_df, hotel_df, selected_hotel, rooms):
    st.title('Room cleaning status (clean, dirty, in progress). ')
    st.write(' Menampilkan dalam bentuk pie chart, jumlah total kamar, jumlah dirty, jumlah cleaning, jumlah in progress pada hari berjalan. \nRekomendasi Visualisasi:\nPie Chart atau Donut Chart: Menunjukkan persentase dari total kamar untuk setiap status (clean, dirty, in progress).\nBar Chart: Menunjukkan jumlah kamar per status dengan opsi filter by room type atau floor')

    cleaning_filter = st.columns(2)
    with cleaning_filter[0]:
        hotel_options = ["All"] + [hotel['name'] for hotel in rooms]
        selected_hotel = st.selectbox("Select Hotel", hotel_options)

    with cleaning_filter[1]:
        if selected_hotel == "All":
            room_types = ["All"]
        else:
            room_types = ["All"] + [room['room_type'] for hotel in rooms if hotel['name'] == selected_hotel for room in hotel['rooms']]
        selected_room_type = st.selectbox("Select Room Type", room_types)

    if selected_hotel == "All" and selected_room_type == "All":
        room_status = [status for hotel in rooms for room in hotel['rooms'] for status in room['status']]
    elif selected_hotel == "All":
        room_status = [status for hotel in rooms for room in hotel['rooms'] if room['room_type'] == selected_room_type for status in room['status']]
    elif selected_room_type == "All":
        room_status = [status for hotel in rooms if hotel['name'] == selected_hotel for room in hotel['rooms'] for status in room['status']]
    else:
        room_status = [status for hotel in rooms if hotel['name'] == selected_hotel for room in hotel['rooms'] if room['room_type'] == selected_room_type for status in room['status']]

    color_mapping = {
        "Cleaned": "green",
        "Dirty": "red",
        "In Progress Cleaning": "blue"
    }
    status_df = pd.DataFrame(room_status)
    status_summary = status_df.groupby('status', as_index=False).sum()

    fig_pie = px.pie(status_summary, names='status', values='rooms', title=f"{selected_hotel} - {selected_room_type} Room Cleaning Status",
                 color='status', color_discrete_map=color_mapping)
    st.plotly_chart(fig_pie)
    
    fig_bar = px.bar(status_summary, x='status', y='rooms', title=f"{selected_hotel} - {selected_room_type} Room Cleaning Status",
                 labels={'rooms': 'Number of Rooms', 'status': 'Room Status'},
                 color='status', color_discrete_map=color_mapping)
    st.plotly_chart(fig_bar)

    st.divider()