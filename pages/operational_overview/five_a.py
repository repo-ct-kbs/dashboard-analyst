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

    st.divider()