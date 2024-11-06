import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import dataframe, render_image

df = dataframe()
st.title('Guest reservations (current and upcoming).')
st.write('Menampilkan dalam bentuk grafik jumlah reservasi yang terjadi di setiap harinya dalam rentang 1 bulan')
df['month'] = df['date'].dt.to_period('M')
monthly_data = df.groupby('month')[['room_available', 'room_filled']].sum().reset_index()
monthly_data['month'] = monthly_data['month'].dt.strftime('%B %Y')
monthly_data['filled_percentage'] = (monthly_data['room_filled'] / monthly_data['room_available']) * 100
month_list = monthly_data['month'].tolist()
selected_month = st.selectbox(
    "Bulan",
    month_list,
)
new_df = df[df['date'].dt.strftime('%B %Y') == selected_month].reset_index(drop=True)
new_df['guest_reservations'] = np.random.randint(0, new_df['room_available'] + 1, size=len(new_df))
fig = px.bar(
    new_df,
    x='date',
    y='guest_reservations',
    title='Daily Guest Reservations for ' + selected_month,
    labels={'guest_reservations': 'Number of Guest Reservations', 'date': 'Date'},
    color_discrete_sequence=['green']
)
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of Reservations',
    xaxis=dict(tickmode='linear', dtick='1D'),
    xaxis_tickangle=-90,
)
render_image('', fig)

st.divider()

st.title('Average Length of Stay (ALOS).')
st.write('Menampilkan dalam bentuk grafik rata-rata lama tamu menginap per bulannya dalam rentang 1 tahun')
df['length_of_stay'] = np.random.randint(1, 8, len(df))
monthly_alos = df.groupby(df['date'].dt.to_period('M'))['length_of_stay'].mean().reset_index()
monthly_alos['month'] = monthly_alos['date'].dt.strftime('%B %Y')
monthly_alos.rename(columns={'length_of_stay': 'average_length_of_stay'}, inplace=True)
fig = px.bar(
    monthly_alos,
    x='month',
    y='average_length_of_stay',
    title='Average Length of Stay (ALOS) per Month',
    labels={'average_length_of_stay': 'Average Length of Stay (Days)', 'month': 'Month'},
    color_discrete_sequence=['orange']
)
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Average Length of Stay (Days)',
)
render_image('', fig)
fig_pie = px.pie(
    monthly_alos,
    values='average_length_of_stay',
    names='month',
    title='Average Length of Stay (ALOS) Distribution per Month',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_pie.update_traces(textinfo='percent+label')
# render_image('', fig_pie)