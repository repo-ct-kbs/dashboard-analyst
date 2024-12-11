from config import df_hotels, df_transactions
import streamlit as st

from financial_management.gm_017 import gm_017
from financial_management.gm_018 import gm_018
from financial_management.gm_019 import gm_019
from financial_management.gm_020 import gm_020
from financial_management.gm_021 import gm_021
from financial_management.gm_022 import gm_022
from financial_management.gm_023 import gm_023
from financial_management.gm_024 import gm_024
from financial_management.gm_025 import gm_025
from financial_management.gm_026 import gm_026
from financial_management.gm_027 import gm_027
from financial_management.gm_028 import gm_028
from financial_management.gm_029 import gm_029
from financial_management.gm_030 import gm_030

datas = df_transactions()
transactions_df = datas[0]
rooms = df_hotels()
rooms_df = rooms[0]
hotel_df = rooms[1]
selected_hotel = datas[1]


st.header('Revenue Management')

st.subheader('Daily, weekly, monthly revenue reports.')
gm_017(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Real-time RevPAR (Revenue Per Available Room) data.')
gm_018(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Room rate forecasting and comparison with historical data.')
gm_019(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Revenue segmentation (room, F&B, services, etc.).')
gm_020(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.divider()
st.divider()

st.header('Expense Management')

st.subheader('Breakdown of operational costs (staffing, utilities, supplies).')
gm_021(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Profit margin analysis.')
gm_022(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Forecast vs. actual expense tracking.')
gm_023(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.divider()
st.divider()

st.header('Budget & Forecast')

st.subheader('Budget comparison (budgeted vs. actual financials).')
gm_024(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Cash flow reports.')
gm_025(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Financial forecasting tools.')
gm_026(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.divider()
st.divider()

st.header('Accounts Receivable & Payable')

st.subheader('Payment status (pending, received, overdue).')
gm_027(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Supplier and vendor management.')
gm_028(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Invoice tracking and approval workflows Guest Reservation')
gm_029(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()

st.subheader('Invoice tracking and approval workflows Supplier. ')
gm_030(transactions_df, rooms_df, hotel_df, selected_hotel)
st.divider()
