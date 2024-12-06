import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

def get_current_week():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def filter_transactions_for_week(transactions_df, start_of_week, end_of_week):
    return transactions_df[
        (transactions_df['check_in_schedule'] <= end_of_week) &
        (transactions_df['check_out_schedule'] >= start_of_week)
    ]

def calculate_daily_occupancy(filtered_transactions, rooms_df, start_of_week):
    dates = [start_of_week + timedelta(days=i) for i in range(7)]
    total_rooms = rooms_df['room_available'].sum()
    
    daily_occupancy = []
    for date in dates:
        occupied_rooms = filtered_transactions[
            (filtered_transactions['check_in_schedule'] <= date) &
            (filtered_transactions['check_out_schedule'] > date)
        ]['room_type'].count()
        occupancy_rate = (occupied_rooms / total_rooms) * 100
        daily_occupancy.append(occupancy_rate)
    return dates, daily_occupancy

def plot_occupancy_chart(dates, occupancy_rates):
    today = datetime.today().date()
    colors = ['red' if date.date() == today else 'blue' for date in dates]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[date.strftime('%A') for date in dates],
            y=occupancy_rates,
            marker_color=colors,
        )
    ])
    fig.update_layout(
        title='Occupancy Rates (This Week)',
        xaxis_title='Days of the Week',
        yaxis_title='Occupancy Rate (%)',
        yaxis=dict(range=[0, 100]),
    )
    return fig

def calculate_occupancy(transactions_df, rooms_df, start_date, end_date):
    filtered = transactions_df[
        (transactions_df["check_in_schedule"] <= end_date) &
        (transactions_df["check_out_schedule"] > start_date)
    ]

    total_rooms = rooms_df["room_available"].sum()
    total_occupancy_days = sum(
        (min(row["check_out_schedule"], end_date) - max(row["check_in_schedule"], start_date)).days
        for _, row in filtered.iterrows()
    )
    total_possible_days = total_rooms * (end_date - start_date).days
    occupancy_rate = (total_occupancy_days / total_possible_days) * 100 if total_possible_days else 0
    return total_occupancy_days, occupancy_rate

def create_percentage_chart(percentage):
    fig = go.Figure(go.Pie(
        values=[percentage, 100 - percentage],
        hole=0.7,
        sort=False,
        direction="clockwise",
        marker=dict(colors=["#636EFA", "#E1E5ED"])
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(
            text=f"{percentage:.1f}%",
            x=0.5, y=0.5, font_size=20, showarrow=False
        )]
    )
    return fig


def gm_001(transactions_df, rooms_df, hotel_df):
    st.title("Hotel Dashboard - Occupancy Rates")
    
    start_of_week, end_of_week = get_current_week()
    filtered_transactions = filter_transactions_for_week(transactions_df, start_of_week, end_of_week)
    
    dates, occupancy_rates = calculate_daily_occupancy(filtered_transactions, rooms_df, start_of_week)
    
    fig = plot_occupancy_chart(dates, occupancy_rates)
    st.plotly_chart(fig)


    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)

    today_occupancy, today_rate = calculate_occupancy(transactions_df, rooms_df, today, today)
    week_occupancy, week_rate = calculate_occupancy(transactions_df, rooms_df, start_of_week, end_of_week)
    month_occupancy, month_rate = calculate_occupancy(transactions_df, rooms_df, start_of_month, end_of_month)
    year_occupancy, year_rate = calculate_occupancy(transactions_df, rooms_df, start_of_year, end_of_year)

    col = st.columns(4)
    with col[0]:
        st.write('### Today Occupancy')
        st.plotly_chart(create_percentage_chart(today_rate), use_container_width=True)
        st.write(f"**{today_occupancy} rooms occupied**")

    with col[1]:
        st.write('### This Week Occupancy')
        st.plotly_chart(create_percentage_chart(week_rate), use_container_width=True)
        st.write(f"**{week_occupancy} rooms occupied**")
    
    with col[2]:
        st.write('### This Month Occupancy')
        st.plotly_chart(create_percentage_chart(month_rate), use_container_width=True)
        st.write(f"**{month_occupancy} rooms occupied**")
    
    with col[3]:
        st.write('### This Year Occupancy')
        st.plotly_chart(create_percentage_chart(year_rate), use_container_width=True)
        st.write(f"**{year_occupancy} rooms occupied**")
