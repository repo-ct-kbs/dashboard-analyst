import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def five_c(transactions_df, rooms_df, selected_hotel):
    st.title('Room status updates')
    st.write('Melacak status kamar secara real-time, seperti ketersediaan, kebersihan, atau maintenance yang sedang berjalan.\nVisualisasi: Status board yang menunjukkan setiap kamar dengan warna berbeda (siap ditempati, sedang dibersihkan, dalam perbaikan), dan indikator real-time untuk perubahan status.')

    rooms_df = pd.DataFrame([
        {"Room": "101", "Type": "Deluxe", "Status": "Ready"},
        {"Room": "102", "Type": "Deluxe", "Status": "Cleaning"},
        {"Room": "103", "Type": "Suite", "Status": "Under Maintenance"},
        {"Room": "104", "Type": "Family", "Status": "Ready"},
        {"Room": "105", "Type": "Family", "Status": "Cleaning"},
        {"Room": "106", "Type": "Standard", "Status": "Under Maintenance"},
    ])

    room_options = rooms_df['Room'].unique()
    selected_room = st.selectbox("Select Room to Update Status", room_options)
    new_status = st.selectbox("Update Status", ["Ready", "Cleaning", "Under Maintenance"])
    if st.button("Update Room Status"):
        rooms_df.loc[rooms_df['Room'] == selected_room, 'Status'] = new_status

    status_colors = {
        "Ready": "green",
        "Cleaning": "orange",
        "Under Maintenance": "red"
    }
    rooms_df['Color'] = rooms_df['Status'].map(status_colors)

    fig = px.scatter(
        rooms_df,
        x="Room",
        y="Type",
        color="Status",
        color_discrete_map=status_colors,
        symbol="Status",
        size_max=20,
        title="Room Status Board",
        labels={"Room": "Room Number", "Type": "Room Type"}
    )
    fig.update_traces(marker=dict(size=20))
    st.plotly_chart(fig)
    st.divider()