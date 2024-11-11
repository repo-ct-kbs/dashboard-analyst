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

    st.divider()