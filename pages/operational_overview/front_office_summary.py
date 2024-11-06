import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import df_hotels, df_transactions


transactions_df = df_transactions()
rooms = df_hotels()
rooms_df = rooms[0]

hotel_names = ['All'] + [hotel['name'] for hotel in rooms[1]]
selected_hotel = st.selectbox("Select a Hotel", hotel_names, key='Room Availability and Occupancy per Selected Date-selected_hotel')
st.divider()

st.title('Guest reservations (current and upcoming).')
st.write('Menampilkan dalam bentuk grafik jumlah reservasi yang terjadi di setiap harinya dalam rentang 1 bulan')
st.divider()

st.title('Average Length of Stay (ALOS).')
st.write('Menampilkan dalam bentuk grafik rata-rata lama tamu menginap per bulannya dalam rentang 1 tahun')
st.divider()

st.title('Daily revenue and ADR (Average Daily Rate).')
st.write('Menampilkan dalam bentuk grafik jumlah pendapatan dan  rata-rata pendapatan dari seluruh kamar yang terisi pada hari berjalan (dihitung dari yang checkin pada hari tersebut)')
st.divider()