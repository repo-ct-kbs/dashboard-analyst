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

    st.divider()