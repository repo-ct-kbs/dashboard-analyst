from config import df_hotels, df_transactions
import streamlit as st

from operational_overview.gm_001 import gm_001
from operational_overview.gm_002 import gm_002
from operational_overview.gm_003 import gm_003
from operational_overview.gm_004 import gm_004
from operational_overview.gm_005 import gm_005
from operational_overview.gm_006 import gm_006
from operational_overview.gm_007 import gm_007
from operational_overview.gm_008 import gm_008
from operational_overview.gm_009 import gm_009
from operational_overview.gm_010 import gm_010
from operational_overview.gm_011 import gm_011
from operational_overview.gm_012 import gm_012
from operational_overview.gm_013 import gm_013
from operational_overview.gm_014 import gm_014
from operational_overview.gm_015 import gm_015
from operational_overview.gm_016 import gm_016


datas = df_transactions()
transactions_df = datas[0]
rooms = df_hotels()
rooms_df = rooms[0]
hotel_df = rooms[1]
selected_hotel = datas[1]


st.header('Real-time Hotel Status')

st.subheader('Occupancy rates (current, historical, and projected)')
gm_001(transactions_df, rooms_df, hotel_df)
st.divider()

st.subheader('Room availability')
gm_002(transactions_df, rooms_df, hotel_df)
st.divider()

st.subheader('Guest check-ins and check-outs.')
gm_003(transactions_df, rooms_df, hotel_df)
st.divider()


st.divider()
st.divider()

st.header('Front Office Summary')

st.subheader('Guest reservations (current and upcoming).')
gm_004(transactions_df, rooms_df, hotel_df)
st.divider()

st.subheader('Average Length of Stay (ALOS).')
gm_005(transactions_df, rooms_df, hotel_df)
st.divider()

st.subheader('Daily revenue and ADR (Average Daily Rate).')
gm_006(transactions_df, rooms_df, hotel_df)
st.divider()

st.subheader('Pending tasks for the front office team.')
gm_007(transactions_df, rooms_df, hotel_df)
st.divider()

st.divider()
st.divider()

st.header('Housekeeping & Maintenance')

st.subheader('Room cleaning status (clean, dirty, in progress).')
gm_008(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Maintenance requests and their statuses.')
gm_009(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Housekeeping staff performance metrics.')
gm_010(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.divider()
st.divider()

st.header('Food & Beverage Operations')

st.subheader('Daily sales reports (breakfast, lunch, dinner).')
gm_011(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Stock and inventory levels.')
gm_012(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Popular items and seasonal trends.')
gm_013(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.divider()
st.divider()

st.header('Room Management')

st.subheader('Room assignments')
gm_014(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Housekeeping schedules')
gm_015(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Room status updates')
gm_016(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()
