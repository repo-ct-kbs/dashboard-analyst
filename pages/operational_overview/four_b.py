import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def four_b(transactions_df, rooms_df, selected_hotel):
    st.title('Stock and inventory levels.')
    st.write('Menampilkan dalam bentuk tabel kondisi stok bahan di setiap outlet pada hari berjalan\n\nRekomendasi Visualisasi:\nHorizontal Bar Chart: Menampilkan jumlah stok yang tersisa per item atau kategori barang.\nGauge Chart: Mengindikasikan level stok (misalnya, jika mendekati habis).\nHeatmap: Menunjukkan level stok secara berkala (misal, mingguan) untuk mengidentifikasi tren penggunaan barang.')

    st.divider()