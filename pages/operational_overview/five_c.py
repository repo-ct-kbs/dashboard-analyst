import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def five_c(transactions_df, rooms_df, selected_hotel):
    st.title('Room status updates')
    st.write('Melacak status kamar secara real-time, seperti ketersediaan, kebersihan, atau maintenance yang sedang berjalan.\nVisualisasi: Status board yang menunjukkan setiap kamar dengan warna berbeda (siap ditempati, sedang dibersihkan, dalam perbaikan), dan indikator real-time untuk perubahan status.')

    st.divider()