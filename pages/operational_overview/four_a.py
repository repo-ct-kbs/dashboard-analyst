import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def four_a(transactions_df, rooms_df, selected_hotel):
    st.title('Daily sales reports (breakfast, lunch, dinner).')
    st.write('Menampilkan dalam bentuk card, jumlah revenue dari penjualan item yang terjadi  di setiap oulet pada hari berjalan\n\nRekomendasi Visualisasi:\nStacked Bar Chart: Menampilkan revenue per sesi makan (breakfast, lunch, dinner) setiap hari.\nLine Graph: Untuk melihat tren penjualan harian dalam sebulan dengan breakdown per sesi makan.')

    st.divider()