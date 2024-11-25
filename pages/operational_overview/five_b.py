from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_calendar import calendar as st_calendar


def five_b(transactions_df, rooms_df, selected_hotel):
    st.title('Housekeeping schedules')
    st.write('Menampilkan jadwal kebersihan kamar untuk efisiensi dan ketersediaan kamar secara optimal.\nVisualisasi: Gantt chart untuk jadwal housekeeping per kamar, dengan warna atau indikator untuk status (bersih, sedang dibersihkan, selesai).')

    calendar_events = [{"allDay":True,"title":"Event 1","start":"2023-07-03","end":"2023-07-05","backgroundColor":"#FF6C6C","borderColor":"#FF6C6C","resourceId":"a"},{"allDay":True,"title":"Event 2","start":"2023-07-01","end":"2023-07-10","backgroundColor":"#FFBD45","borderColor":"#FFBD45","resourceId":"b"},{"allDay":True,"title":"Event 3","start":"2023-07-20","backgroundColor":"#FF4B4B","borderColor":"#FF4B4B","resourceId":"c"},{"allDay":True,"title":"Event 4","start":"2023-07-23","end":"2023-07-25","backgroundColor":"#FF6C6C","borderColor":"#FF6C6C","resourceId":"d"},{"allDay":True,"title":"Event 5","start":"2023-07-29","end":"2023-07-30","backgroundColor":"#FFBD45","borderColor":"#FFBD45","resourceId":"e"},{"allDay":True,"title":"Event 6","start":"2023-07-28","backgroundColor":"#FF4B4B","borderColor":"#FF4B4B","resourceId":"f"},{"allDay":False,"title":"Event 7","start":"2023-07-01T08:30:00+08:00","end":"2023-07-01T10:30:00+08:00","backgroundColor":"#FF4B4B","borderColor":"#FF4B4B","resourceId":"a"},{"allDay":False,"title":"Event 8","start":"2023-07-01T07:30:00+08:00","end":"2023-07-01T10:30:00+08:00","backgroundColor":"#3D9DF3","borderColor":"#3D9DF3","resourceId":"b"},{"allDay":False,"title":"Event 9","start":"2023-07-02T10:40:00+08:00","end":"2023-07-02T12:30:00+08:00","backgroundColor":"#3DD56D","borderColor":"#3DD56D","resourceId":"c"},{"allDay":False,"title":"Event 10","start":"2023-07-15T08:30:00+08:00","end":"2023-07-15T10:30:00+08:00","backgroundColor":"#FF4B4B","borderColor":"#FF4B4B","resourceId":"d"},{"allDay":False,"title":"Event 11","start":"2023-07-15T07:30:00+08:00","end":"2023-07-15T10:30:00+08:00","backgroundColor":"#3DD56D","borderColor":"#3DD56D","resourceId":"e"},{"allDay":False,"title":"Event 12","start":"2023-07-21T10:40:00+08:00","end":"2023-07-21T12:30:00+08:00","backgroundColor":"#3D9DF3","borderColor":"#3D9DF3","resourceId":"f"},{"allDay":False,"title":"Event 13","start":"2023-07-17T08:30:00+08:00","end":"2023-07-17T10:30:00+08:00","backgroundColor":"#FF4B4B","borderColor":"#FF4B4B","resourceId":"a"},{"allDay":False,"title":"Event 14","start":"2023-07-17T09:30:00+08:00","end":"2023-07-17T11:30:00+08:00","backgroundColor":"#3D9DF3","borderColor":"#3D9DF3","resourceId":"b"},{"allDay":False,"title":"Event 15","start":"2023-07-17T10:30:00+08:00","end":"2023-07-17T12:30:00+08:00","backgroundColor":"#3DD56D","borderColor":"#3DD56D","resourceId":"c"},{"allDay":False,"title":"Event 16","start":"2023-07-17T13:30:00+08:00","end":"2023-07-17T14:30:00+08:00","backgroundColor":"#FF6C6C","borderColor":"#FF6C6C","resourceId":"d"},{"allDay":False,"title":"Event 17","start":"2023-07-17T15:30:00+08:00","end":"2023-07-17T16:30:00+08:00","backgroundColor":"#FFBD45","borderColor":"#FFBD45","resourceId":"e"}]
    custom_css="""
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

    calendar = st_calendar(events=calendar_events,  custom_css=custom_css)
    st.write(calendar)

    st.divider()