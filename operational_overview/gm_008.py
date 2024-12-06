import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def gm_008(transactions_df, rooms_df, hotel_df, selected_hotel):
    if selected_hotel == "All":
        room_types = ["All"] + [room['room_type'] for hotel in hotel_df if hotel['name'] == selected_hotel for room in hotel['rooms']]
    else:
        room_types = ["All"] + [room['room_type'] for hotel in hotel_df if hotel['name'] == selected_hotel for room in hotel['rooms']]
    selected_room_type = st.selectbox("Select Room Type", room_types)

    if selected_hotel == "All" and selected_room_type == "All":
        room_status = [status for hotel in hotel_df for room in hotel['rooms'] for status in room['status']]
    elif selected_hotel == "All":
        room_status = [status for hotel in hotel_df for room in hotel['rooms'] if room['room_type'] == selected_room_type for status in room['status']]
    elif selected_room_type == "All":
        room_status = [status for hotel in hotel_df if hotel['name'] == selected_hotel for room in hotel['rooms'] for status in room['status']]
    else:
        room_status = [status for hotel in hotel_df if hotel['name'] == selected_hotel for room in hotel['rooms'] if room['room_type'] == selected_room_type for status in room['status']]

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