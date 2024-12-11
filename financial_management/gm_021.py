import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_021(transactions_df, rooms_df, hotel_df, selected_hotel):
    print()