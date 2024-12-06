from config import df_hotels, df_transactions
import streamlit as st


datas = df_transactions()
transactions_df = datas[0]
rooms = df_hotels()
rooms_df = rooms[0]
hotel_df = rooms[1]
selected_hotel = datas[1]


st.header('Revenue Management')

st.subheader('Daily, weekly, monthly revenue reports.')
st.divider()

st.subheader('Real-time RevPAR (Revenue Per Available Room) data.')
st.divider()

st.subheader('Room rate forecasting and comparison with historical data.')
st.divider()

st.subheader('Revenue segmentation (room, F&B, services, etc.).')
st.divider()

st.divider()
st.divider()

st.header('Expense Management')

st.subheader('Breakdown of operational costs (staffing, utilities, supplies).')
st.divider()

st.subheader('Profit margin analysis.')
st.divider()

st.subheader('Forecast vs. actual expense tracking.')
st.divider()

st.divider()
st.divider()

st.header('Budget & Forecast')

st.subheader('Budget comparison (budgeted vs. actual financials).')
st.divider()

st.subheader('Cash flow reports.')
st.divider()

st.subheader('Financial forecasting tools.')
st.divider()

st.divider()
st.divider()

st.header('Accounts Receivable & Payable')

st.subheader('Payment status (pending, received, overdue).')
st.divider()

st.subheader('Supplier and vendor management.')
st.divider()

st.subheader('Invoice tracking and approval workflows Guest Reservation')
st.divider()

st.subheader('Invoice tracking and approval workflows Supplier. ')
st.divider()
