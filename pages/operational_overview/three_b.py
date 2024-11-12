import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def three_b(transactions_df, rooms_df, selected_hotel):
    st.title('Maintenance requests and their statuses.')
    st.write('Menampilkan dalam bentuk card, jumlah request maintenance dan jumlah di setiap status maintenancenya serta dalam bentuk tabel untuk detail maintenance')

    maintenance_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'request_time': ['2024-11-01 09:00', '2024-11-01 11:30', '2024-11-02 14:00', '2024-11-03 10:15', '2024-11-03 15:45', '2024-11-04 12:00'],
        'status': ['Pending', 'Completed', 'In Progress', 'Pending', 'In Progress', 'Completed'],
        'description': ['Fix air conditioner', 'Repair light fixture', 'Unclog drain', 'Replace window', 'Paint walls', 'Clean roof'],
        'priority': ['High', 'Medium', 'Low', 'Medium', 'High', 'Low'],
        'assigned_to': ['John', 'Jane', 'Mike', 'Sara', 'Tom', 'Ana']
    })

    total_requests = len(maintenance_data)
    status_counts = maintenance_data['status'].value_counts().to_dict()

    st.write("Maintenance Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Requests", total_requests)
    col2.metric("Pending", status_counts.get("Pending", 0))
    col3.metric("In Progress", status_counts.get("In Progress", 0))
    col4.metric("Completed", status_counts.get("Completed", 0))

    st.write("Maintenance Details")
    st.dataframe(maintenance_data)

    st.divider()