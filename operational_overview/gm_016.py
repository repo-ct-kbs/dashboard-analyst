import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_016(transactions_df, rooms_df, hotel_df, selected_hotel):
    room_data = []
    
    for hotel in hotel_df:
        hotel_name = hotel['name']
        for room in hotel['rooms']:
            room_type = room['room_type']
            for status_info in room['status']:
                status = status_info['status']
                room_count = status_info['rooms']
                for _ in range(room_count):
                    room_data.append({
                        'hotel': hotel_name,
                        'room_type': room_type,
                        'status': status
                    })
    
    df = pd.DataFrame(room_data)
    
    status_color_map = {
        'Cleaned': '#3DD56D', 
        'In Progress Cleaning': '#FFBD45', 
        'Dirty': '#FF6C6C'
    }
    
    df['color'] = df['status'].map(status_color_map)
    
    pivot_df = df.pivot_table(index='hotel', columns='room_type', aggfunc='size', fill_value=0)
    
    fig = px.imshow(pivot_df, 
                    color_continuous_scale='Viridis',
                    labels={'color': 'Room Count'},
                    title="Room Status Overview")
    fig.update_layout(
        xaxis_title='Room Type',
        yaxis_title='Hotel',
        showlegend=False
    )
    st.plotly_chart(fig)


    room_data = []

    for hotel in hotel_df:
        hotel_name = hotel['name']
        for room in hotel['rooms']:
            room_type = room['room_type']
            for status_info in room['status']:
                status = status_info['status']
                room_count = status_info['rooms']
                room_data.append({
                    'hotel': hotel_name,
                    'room_type': room_type,
                    'status': status,
                    'count': room_count
                })
    
    df = pd.DataFrame(room_data)

    fig = px.bar(df, x='room_type', y='count', color='status', barmode='group',
                 facet_col='hotel', height=400,
                 labels={'count': 'Number of Rooms', 'status': 'Room Status'},
                 title="Room Status by Hotel and Room Type")
    fig.update_layout(
        showlegend=True,
        xaxis_title='Room Type',
        yaxis_title='Room Count'
    )

    st.plotly_chart(fig)