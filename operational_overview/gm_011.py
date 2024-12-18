import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from plotly.subplots import make_subplots


# def generate_daily_sales_data(month='2024-12', service_types=None, time_sessions=None, num_days=31):
#     if service_types is None:
#         service_types = ['In-room dining', 'Restaurant', 'Poolside']
#     if time_sessions is None:
#         time_sessions = ['Breakfast', 'Lunch', 'Dinner']
    
#     date_range = pd.date_range(f'{month}-01', f'{month}-{num_days}')
#     data = []
    
#     for date in date_range:
#         for service in service_types:
#             for session in time_sessions:
#                 revenue = round(random.uniform(100, 1000), 2)
#                 data.append({
#                     'date': date,
#                     'service_type': service,
#                     'time_session': session,
#                     'total_revenue': revenue
#                 })
    
#     return pd.DataFrame(data)


# def gm_011(transactions_df, rooms_df, hotel_df, selected_hotel):
#     sales_data = generate_daily_sales_data()

#     st.write("### Daily Sales Report")
#     selected_service = st.selectbox("Filter by Service Type", sales_data['service_type'].unique())
#     selected_session = st.selectbox("Filter by Time Session", sales_data['time_session'].unique())

#     filtered_data = sales_data[
#         (sales_data['service_type'] == selected_service) &
#         (sales_data['time_session'] == selected_session)
#     ]
#     st.dataframe(filtered_data)

#     sales_summary = filtered_data.groupby('date')['total_revenue'].sum().reset_index()

#     fig_sales = px.bar(
#         sales_summary,
#         x='date',
#         y='total_revenue',
#         title=f'{selected_session} Sales for {selected_service} (December 2024)',
#         labels={'total_revenue': 'Total Revenue', 'date': 'Date'},
#         color='total_revenue',
#         color_continuous_scale='Blues',
#         text='total_revenue'
#     )

#     fig_sales.update_traces(textposition='outside')
#     st.plotly_chart(fig_sales)

def gm_011(transactions_df, rooms_df, hotel_df, selected_hotel):
    data = {
        "Outlet": ["Outlet A", "Outlet B", "Outlet C"] * 3,
        "Session": ["Breakfast", "Lunch", "Dinner"] * 3,
        "Date": ["2024-12-18"] * 9,
        "Revenue": [5000, 7000, 6000, 8000, 9000, 7500, 3000, 4000, 3500],
    }

    trend_data = {
        "Date": pd.date_range(start="2024-12-01", end="2024-12-31"),
        "Breakfast": [x * 100 for x in range(1, 32)],
        "Lunch": [x * 150 for x in range(1, 32)],
        "Dinner": [x * 120 for x in range(1, 32)],
    }

    daily_sales_df = pd.DataFrame(data)
    monthly_trend_df = pd.DataFrame(trend_data)

    outlet_revenue = daily_sales_df.groupby("Outlet")["Revenue"].sum().reset_index()

    for index, row in outlet_revenue.iterrows():
        st.metric(label=f"Revenue at {row['Outlet']}", value=f"${row['Revenue']:,}")

    st.write("### Revenue Breakdown per Meal Session (Stacked Bar Chart)")
    fig_stacked_bar = px.bar(
        daily_sales_df,
        x="Outlet",
        y="Revenue",
        color="Session",
        title="Revenue Breakdown by Session (Today)",
        labels={"Revenue": "Revenue (USD)", "Outlet": "Outlet"},
        barmode="stack",
    )
    st.plotly_chart(fig_stacked_bar)

    st.write("### Monthly Sales Trends (Line Graph)")
    monthly_trend_df_melted = monthly_trend_df.melt(id_vars=["Date"], var_name="Session", value_name="Revenue")

    fig_line = px.line(
        monthly_trend_df_melted,
        x="Date",
        y="Revenue",
        color="Session",
        title="Monthly Sales Trends by Session",
        labels={"Revenue": "Revenue (USD)", "Date": "Date"},
    )
    st.plotly_chart(fig_line)