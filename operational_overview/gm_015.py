import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar as st_calendar


def generate_housekeeping_schedule(hotel_df):
    schedule = []
    colors = {'Cleaned': '#3DD56D', 'In Progress Cleaning': '#FFBD45', 'Dirty': '#FF6C6C'}

    start_date = pd.Timestamp('2024-12-01')
    end_date = pd.Timestamp('2024-12-31')

    for hotel in hotel_df:
        hotel_name = hotel['name']
        for room in hotel['rooms']:
            room_type = room['room_type']
            for status_info in room['status']:
                status = status_info['status']
                room_count = status_info['rooms']
                
                for _ in range(room_count):
                    cleaning_day = start_date + pd.Timedelta(days=random.randint(0, 30))
                    task_duration = random.randint(1, 2)
                    task_end_date = cleaning_day + pd.Timedelta(days=task_duration)
                    
                    schedule.append({
                        'hotel': hotel_name,
                        'room_type': room_type,
                        'status': status,
                        'title': f"{status} - {room_type} ({hotel_name})",
                        'start': cleaning_day.strftime('%Y-%m-%d'),
                        'end': task_end_date.strftime('%Y-%m-%d'),
                        'color': colors[status]
                    })
    
    return pd.DataFrame(schedule)



def gm_015(transactions_df, rooms_df, hotel_df, selected_hotel):
    housekeeping_schedule = generate_housekeeping_schedule(hotel_df)

    calendar_events = [
        {
            "allDay": True,
            "title": row["title"],
            "start": row["start"],
            "end": row["end"],
            "backgroundColor": row["color"],
            "borderColor": row["color"],
            "resourceId": f"{row['hotel']}-{row['room_type']}"
        }
        for _, row in housekeeping_schedule.iterrows()
    ]

    custom_css = """
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """

    st_calendar(events=calendar_events, custom_css=custom_css)