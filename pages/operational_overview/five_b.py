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

    st.divider()