import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def generate_task_data(rooms_df, num_tasks=50):
    task_types = ["Room Cleaning", "Maintenance Check", "Key Replacement", "Guest Request"]
    task_statuses = ["Pending", "In Progress", "Completed"]
    random.seed(42)
    tasks = []
    for _ in range(num_tasks):
        room = random.choice(rooms_df['room_type'].unique())
        task = {
            "room_name": room,
            "task_type": random.choice(task_types),
            "status": random.choice(task_statuses),
            "assigned_to": f"Staff {random.randint(1, 10)}",
            "due_date": pd.Timestamp.today() + pd.Timedelta(days=random.randint(0, 7))
        }
        tasks.append(task)
    return pd.DataFrame(tasks)

def gm_007(transactions_df, rooms_df, hotel_df):
    
    tasks_df = generate_task_data(rooms_df)
    pending_tasks_df = tasks_df[tasks_df['status'] == 'Pending']

    task_counts = pending_tasks_df.groupby(['room_name', 'task_type']).size().reset_index(name='count')

    fig = px.bar(
        task_counts, 
        x='room_name', 
        y='count', 
        color='task_type', 
        title="Pending Tasks by Room and Task Type",
        labels={'count': 'Number of Tasks', 'room_name': 'Room Name'},
        text='count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(barmode='stack', xaxis_tickangle=-45)

    st.plotly_chart(fig)
