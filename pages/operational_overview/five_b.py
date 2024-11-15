import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def five_b(transactions_df, rooms_df, selected_hotel):
    st.title('Housekeeping schedules')
    st.write('Menampilkan jadwal kebersihan kamar untuk efisiensi dan ketersediaan kamar secara optimal.\nVisualisasi: Gantt chart untuk jadwal housekeeping per kamar, dengan warna atau indikator untuk status (bersih, sedang dibersihkan, selesai).')

    df = pd.DataFrame([
        dict(Task="Job A", Start='2023-11-01', Finish='2023-11-10', Resource="Alex", Status="Completed"),
        dict(Task="Job B", Start='2023-11-05', Finish='2023-11-15', Resource="Alex", Status="In Progress"),
        dict(Task="Job C", Start='2023-11-10', Finish='2023-11-20', Resource="Max", Status="Not Started"),
        dict(Task="Job D", Start='2023-11-12', Finish='2023-11-25', Resource="Max", Status="Completed"),
        dict(Task="Job E", Start='2023-11-15', Finish='2023-11-22', Resource="Sam", Status="In Progress"),
    ])

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Status",
        hover_name="Resource",
        title="Project Gantt Chart with Status"
    )

    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig)

    st.divider()