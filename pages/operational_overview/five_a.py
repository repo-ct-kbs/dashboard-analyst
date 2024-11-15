import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def five_a(transactions_df, rooms_df, selected_hotel):
    st.title('Room assignments')
    st.write('Melacak penugasan kamar yang sesuai dengan preferensi tamu, memastikan alokasi kamar yang optimal.\n\nRekomendasi Visualisasi: \nGrid view atau gantt chart untuk kamar yang sudah ditempati atau tersedia, serta pie chart untuk tipe kamar yang paling banyak dipesan. Menunjukkan room assignments berdasarkan tipe kamar dan tanggal.\nCalendar Heatmap: Untuk melihat pattern okupansi kamar per hari dalam sebulan.')

    assignments_data = pd.DataFrame([
        {"Room Type": "Deluxe", "Start": "2024-11-01", "End": "2024-11-05", "Guest": "Alice"},
        {"Room Type": "Suite", "Start": "2024-11-03", "End": "2024-11-07", "Guest": "Bob"},
        {"Room Type": "Standard", "Start": "2024-11-04", "End": "2024-11-06", "Guest": "Charlie"},
        {"Room Type": "Deluxe", "Start": "2024-11-08", "End": "2024-11-10", "Guest": "David"},
        {"Room Type": "Family", "Start": "2024-11-09", "End": "2024-11-12", "Guest": "Eve"}
    ])

    bookings_data = pd.DataFrame([
        {"Room Type": "Deluxe", "Count": 15},
        {"Room Type": "Suite", "Count": 10},
        {"Room Type": "Standard", "Count": 8},
        {"Room Type": "Family", "Count": 12}
    ])

    dates = pd.date_range("2024-11-01", "2024-11-30")
    occupancy_data = pd.DataFrame({
        "Date": dates,
        "Occupancy": [50, 45, 60, 55, 70, 40, 80, 65, 60, 75, 55, 50, 45, 55, 65, 70, 85, 60, 55, 50, 60, 75, 85, 90, 70, 65, 50, 60, 55, 70]
    })

    assignments_data["Start"] = pd.to_datetime(assignments_data["Start"])
    assignments_data["End"] = pd.to_datetime(assignments_data["End"])

    fig_gantt = px.timeline(assignments_data, x_start="Start", x_end="End", y="Room Type", color="Room Type", title="Room Assignments Gantt Chart")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt)

    fig_pie = px.pie(bookings_data, names="Room Type", values="Count", title="Most Booked Room Types")
    st.plotly_chart(fig_pie)

    occupancy_data['Weekday'] = occupancy_data['Date'].dt.day_name()
    occupancy_data['Week'] = occupancy_data['Date'].dt.isocalendar().week

    heatmap_data = occupancy_data.pivot_table(values="Occupancy", index="Week", columns="Weekday")

    heatmap_data = heatmap_data[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Viridis",
        colorbar_title="Occupancy"
    ))

    fig_heatmap.update_layout(
        title="Room Occupancy Calendar Heatmap",
        xaxis_title="Day of the Week",
        yaxis_title="Week Number"
    )

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        y=heatmap_data.index,
        colorscale="Viridis",
    ))

    fig_heatmap.update_layout(
        title="Room Occupancy Calendar Heatmap",
        xaxis_title="Day of the Week",
        yaxis_title="Week Number"
    )

    st.plotly_chart(fig_heatmap)

    st.divider()