import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

def generate_housekeeping_data(num_staff=10):
    random.seed(42)
    staff_names = [f"Staff {i}" for i in range(1, num_staff + 1)]
    data = []
    for staff in staff_names:
        rooms_cleaned = random.randint(5, 30)
        tasks_completed = random.randint(rooms_cleaned, rooms_cleaned + 10)
        avg_cleaning_time = round(random.uniform(10, 30), 2)
        guest_rating = round(random.uniform(3.0, 5.0), 2)
        data.append({
            "staff_name": staff,
            "rooms_cleaned": rooms_cleaned,
            "tasks_completed": tasks_completed,
            "avg_cleaning_time": avg_cleaning_time,
            "guest_rating": guest_rating
        })
    return pd.DataFrame(data)

def gm_010(transactions_df, rooms_df, hotel_df, selected_hotel):
    housekeeping_df = generate_housekeeping_data()

    fig_cleaned = px.bar(
        housekeeping_df,
        x='rooms_cleaned',
        y='staff_name',
        orientation='h',
        title='Rooms Cleaned by Housekeeping Staff',
        labels={'rooms_cleaned': 'Rooms Cleaned', 'staff_name': 'Staff Name'},
        text='rooms_cleaned'
    )
    fig_cleaned.update_traces(textposition='outside')
    st.plotly_chart(fig_cleaned)

    fig_scatter = px.scatter(
        housekeeping_df,
        x='avg_cleaning_time',
        y='guest_rating',
        size='tasks_completed',
        color='staff_name',
        title='Average Cleaning Time vs Guest Rating',
        labels={
            'avg_cleaning_time': 'Average Cleaning Time (minutes/room)',
            'guest_rating': 'Guest Satisfaction Rating'
        },
        hover_data=['rooms_cleaned', 'tasks_completed']
    )
    st.plotly_chart(fig_scatter)

    fig_gauges = make_subplots(
        rows=2, cols=5, 
        specs=[[{'type': 'indicator'}] * 5, [{'type': 'indicator'}] * 5],
        subplot_titles=housekeeping_df['staff_name'].tolist()
    )

    for i, row in housekeeping_df.iterrows():
        fig_gauges.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=row['tasks_completed'],
                title={'text': "Completed"},
                gauge={'axis': {'range': [0, max(housekeeping_df['tasks_completed'])]}}
            ),
            row=(i // 5) + 1, col=(i % 5) + 1
        )

    fig_gauges.update_layout(height=800, title_text="Housekeeping Staff Task Performance")
    st.plotly_chart(fig_gauges)

