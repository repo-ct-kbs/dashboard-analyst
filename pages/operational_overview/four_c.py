import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def four_c(transactions_df, rooms_df, selected_hotel):
    st.title('Popular items and seasonal trends.')
    st.write('Menampilkan dalam bentuk tabel, item/produk yang populer (penjualan banyak) dan trend penjualan berdasarkan season (q1, q2, dll)\n\nRekomendasi Visualisasi:\nBar Chart atau Column Chart: Menampilkan item terpopuler berdasarkan jumlah unit atau revenue.\nLine Graph: Untuk menunjukkan tren penjualan berdasarkan musim atau bulan (menunjukkan popularitas item musiman).')

    st.divider()