import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def three_c(transactions_df, rooms_df, selected_hotel):
    st.title('Housekeeping staff performance metrics.')
    st.write('Menampilkan dalam bentuk tabel, total pekerjaan maintenance yang sedang dan telah dikerjakan oleh setiap staf dalam rentang 1 bulan')

    filter_col = st.columns(2)
    with filter_col[0]:
        selected_year = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist(), key='two_a_1_year')
    with filter_col[1]:
        selected_month = st.selectbox("Month", list(calendar.month_name[1:]), key='two_a_1_month')
    
    maintenance_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'request_time': ['2024-11-01 09:00', '2024-11-01 11:30', '2024-11-02 14:00', '2024-11-03 10:15', '2024-11-03 15:45', '2024-11-04 12:00'],
        'status': ['Pending', 'Completed', 'In Progress', 'Completed', 'In Progress', 'Completed'],
        'assigned_to': ['John', 'Jane', 'Mike', 'Sara', 'Tom', 'Ana']
    })

    maintenance_data['request_time'] = pd.to_datetime(maintenance_data['request_time'])

    end_date = maintenance_data['request_time'].max()
    start_date = end_date - timedelta(days=30)
    filtered_data = maintenance_data[(maintenance_data['request_time'] >= start_date) & (maintenance_data['request_time'] <= end_date)]

    staff_options = ["All"] + filtered_data['assigned_to'].unique().tolist()
    selected_staff = st.selectbox("Select Staff", staff_options)

    if selected_staff != "All":
        filtered_data = filtered_data[filtered_data['assigned_to'] == selected_staff]

    status_counts = filtered_data['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']

    for status in ["Pending", "In Progress", "Completed"]:
        if status not in status_counts['status'].values:
            status_counts = pd.concat([status_counts, pd.DataFrame([[status, 0]], columns=['status', 'count'])], ignore_index=True)

    fig = px.pie(
        status_counts,
        names='status',
        values='count',
        title=f"Maintenance Work Status ({selected_staff if selected_staff != 'All' else 'All Staff'})",
    )

    st.plotly_chart(fig)

    st.divider()