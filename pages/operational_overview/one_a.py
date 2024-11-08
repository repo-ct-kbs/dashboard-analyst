import calendar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import fixed_range

def calculate_occupancy(selected_date, start_of_day, end_of_day, days_in_range, selected_hotel, transactions_df, rooms_df):
    selected_bookings = transactions_df[
        (transactions_df['check_in_time'].dt.date <= end_of_day) &
        (transactions_df['check_out_time'].dt.date >= start_of_day)
    ]

    if selected_hotel == 'All':
        filtered_booking = selected_bookings
    else:
        filtered_booking = selected_bookings[selected_bookings['hotel_name'] == selected_hotel]

    # st.write(filtered_bookingr)

    if not filtered_booking.empty:
        filtered_booking['nights_in_range'] = filtered_booking.apply(
            lambda row: (min(row['check_out_time'].date(), end_of_day) - max(row['check_in_time'].date(), start_of_day)).days, axis=1
        )

        filtered_booking['check_in_time'] = pd.to_datetime(filtered_booking['check_in_time'])
        filtered_booking['check_out_time'] = pd.to_datetime(filtered_booking['check_out_time'])

        date_range_occupancy = filtered_booking.groupby(['hotel_name', 'room_type'])['nights_in_range'].sum().reset_index(name='rooms_filled')
        date_range_availability = pd.merge(date_range_occupancy, rooms_df, on=['hotel_name', 'room_type'], how='outer').fillna(0)

        date_range_availability['capacity'] = date_range_availability['room_available'] * days_in_range
        date_range_availability['occupancy'] = date_range_availability['rooms_filled']

        total_capacity_range = date_range_availability['capacity'].sum()
        if selected_hotel != 'All':
            date_range_availability = date_range_availability[date_range_availability['hotel_name'] == selected_hotel]
            total_capacity_range = date_range_availability['capacity'].sum()

        total_days_for_occupancy = 0
        for _, row in filtered_booking.iterrows():
            check_in = row['check_in_time'].date()
            check_out = row['check_out_time'].date()

            if check_out >= start_of_day and check_in <= end_of_day:
                start_date = max(check_in, start_of_day)
                end_date = min(check_out, end_of_day)

                if end_date == check_out:
                    days_count = (end_date - start_date).days
                else:
                    days_count = (end_date - start_date).days + 1

                total_days_for_occupancy += days_count


        occupancy_percentage_range = (total_days_for_occupancy / total_capacity_range * 100) if total_capacity_range > 0 else 0

        st.subheader(f'Date range: {start_of_day} to {end_of_day}')
        col = st.columns(3)
        with col[0]:
            st.subheader(f'Total Capacity')
            st.header(total_capacity_range)
        with col[1]:
            st.subheader(f'Total Occupancy')
            st.header(total_days_for_occupancy)
        with col[2]:
            st.subheader(f'Occupancy Percentage')
            st.header(f'{occupancy_percentage_range:.2f} %')
    else:
        difference_in_days = (end_of_day - start_of_day).days + 1
        total_rooms = rooms_df[rooms_df['hotel_name'] == selected_hotel]['room_available'].sum()
        total_capacity_range = difference_in_days * total_rooms

        col = st.columns(3)
        with col[0]:
            st.subheader(f'Total Capacity')
            st.header(total_capacity_range)
        with col[1]:
            st.subheader(f'Total Occupancy')
            st.header('0')
        with col[2]:
            st.subheader(f'Occupancy Percentage')
            st.header(f'0 %')


def get_last_year_range(selected_date):
    start_of_year = datetime(selected_date.year - 1, 1, 1).date()
    end_of_year = datetime(selected_date.year - 1, 12, 31).date()
    days_in_range = (end_of_year - start_of_year).days + 1
    return start_of_year, end_of_year, days_in_range


def one_a(selected_hotel, transactions_df, rooms_df):
    st.title('Occupancy rates (current, historical, and projected).')
    st.write('Menampilkan dalam bentuk grafik, persentase rata-rata kamar yang ditempati di setiap bulannya dalam rentang satu tahun, serta dalam bentuk card untuk persentase harian, mingguan, bulanan dan tahunan')

    selected_date = st.date_input("Select a Date", fixed_range)
    filter_selection = st.selectbox("Filter", ["Today", "This week", "Last 7 days", "Last week", "This month", "Last 30 days", "Last month", "This year", "Last 365 days", "Last year"])


    if filter_selection == "Today":
        today = selected_date
        start_of_day = today
        end_of_day = today
        days_in_range = 1
        calculate_occupancy(selected_date, start_of_day, end_of_day, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "This week":
        today = selected_date
        start_of_day = today - timedelta(days=today.weekday())
        end_of_day = today
        days_in_range = (end_of_day - start_of_day).days + 1
        calculate_occupancy(selected_date, start_of_day, end_of_day, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last 7 days":
        today = selected_date
        start_of_day = today - timedelta(days=6)
        end_of_day = today
        days_in_range = (end_of_day - start_of_day).days + 1
        calculate_occupancy(selected_date, start_of_day, end_of_day, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last week":
        today = selected_date
        start_of_last_week = today - timedelta(days=today.weekday() + 7)
        end_of_last_week = start_of_last_week + timedelta(days=6)
        days_in_range = (end_of_last_week - start_of_last_week).days + 1
        calculate_occupancy(selected_date, start_of_last_week, end_of_last_week, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "This month":
        today = selected_date
        start_of_month = today.replace(day=1)
        end_of_month = today
        days_in_range = (end_of_month - start_of_month).days + 1
        calculate_occupancy(selected_date, start_of_month, end_of_month, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last 30 days":
        today = selected_date
        start_of_period = today - timedelta(days=30)
        end_of_period = today
        days_in_range = 30
        calculate_occupancy(selected_date, start_of_period, end_of_period, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last month":
        today = selected_date
        first_of_current_month = today.replace(day=1)
        last_of_previous_month = first_of_current_month - timedelta(days=1)
        first_of_previous_month = last_of_previous_month.replace(day=1)
        start_of_period = first_of_previous_month
        end_of_period = last_of_previous_month
        days_in_range = (end_of_period - start_of_period).days + 1
        calculate_occupancy(selected_date, start_of_period, end_of_period, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "This year":
        today = selected_date
        first_of_current_year = today.replace(month=1, day=1)
        start_of_period = first_of_current_year
        end_of_period = today
        days_in_range = (end_of_period - start_of_period).days + 1
        calculate_occupancy(selected_date, start_of_period, end_of_period, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last 365 days":
        today = selected_date
        start_of_period = today - timedelta(days=365)
        end_of_period = today
        days_in_range = (end_of_period - start_of_period).days + 1    
        calculate_occupancy(selected_date, start_of_period, end_of_period, days_in_range, selected_hotel, transactions_df, rooms_df)


    if filter_selection == "Last year":
        start_of_year, end_of_year, days_in_range = get_last_year_range(selected_date)
        calculate_occupancy(selected_date, start_of_year, end_of_year, days_in_range, selected_hotel, transactions_df, rooms_df)

    st.divider()


def one_a_b(transactions_df):
    option_col = st.columns(2)
    with option_col[0]:
        selected_filter = st.selectbox('Select Range', ['Yearly', 'Monthly', 'Weekly', 'Daily'])
    with option_col[1]:
        if selected_filter == 'Daily':
            day_option = st.columns(2)
            with day_option[0]:
                year_selection = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist())
            with day_option[1]:
                month_selection = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

            df_filtered = transactions_df[transactions_df['check_in_time'].dt.year == year_selection]
            df_filtered = df_filtered[df_filtered['check_in_time'].dt.month_name() == month_selection]

            month_number = datetime.strptime(month_selection, "%B").month
            days_in_month = (datetime(year_selection, month_number % 12 + 1, 1) - pd.DateOffset(days=1)).day

            day_occupancy_counts = []

            for _, row in df_filtered.iterrows():
                check_in = row['check_in_time'].date()
                check_out = row['check_out_time'].date()

                start_of_month = datetime(year_selection, month_number, 1).date()
                end_of_month = datetime(year_selection, month_number, days_in_month).date()

                for day in pd.date_range(start=start_of_month, end=end_of_month):
                    if check_in <= day.date() < check_out:
                        day_occupancy_counts.append({'day': day.date(), 'occupancy_count': 1})

            day_occupancy_counts_df = pd.DataFrame(day_occupancy_counts)
            
            day_occupancy_counts_df = day_occupancy_counts_df.groupby('day')['occupancy_count'].sum().reset_index()

            all_days = pd.date_range(start=start_of_month, end=end_of_month).date
            all_days_df = pd.DataFrame({'day': all_days})

            full_day_occupancy_df = pd.merge(all_days_df, day_occupancy_counts_df, on='day', how='left').fillna({'occupancy_count': 0})

            fig = px.line(full_day_occupancy_df,
                        x='day',
                        y='occupancy_count',
                        labels={'day': 'Day of the Month', 'occupancy_count': 'Room Occupancy'},
                        title=f"Room Occupancy per Day for {month_selection} {year_selection}")

            fig.update_xaxes(tickmode='array', tickvals=full_day_occupancy_df['day'], ticktext=[str(d.day) for d in full_day_occupancy_df['day']])

        if selected_filter == 'Weekly':
            week_option = st.columns(2)
            with week_option[0]:
                year_selection = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist())
            with week_option[1]:
                month_selection = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
            
            df_filtered = transactions_df[transactions_df['check_in_time'].dt.year == year_selection]
            df_filtered = df_filtered[df_filtered['check_in_time'].dt.month_name() == month_selection]
            
            df_filtered['week_number'] = df_filtered['check_in_time'].dt.isocalendar().week
            
            week_occupancy_counts = []
            
            for _, row in df_filtered.iterrows():
                check_in = row['check_in_time'].date()
                check_out = row['check_out_time'].date()

                start_of_day = pd.to_datetime(f"{year_selection}-{month_selection}-01")
                end_of_day = pd.to_datetime(f"{year_selection}-{month_selection}-01") + pd.DateOffset(months=1) - pd.DateOffset(days=1)
                
                total_days_for_occupancy = 0

                if check_out >= start_of_day.date() and check_in <= end_of_day.date():
                    start_date = max(check_in, start_of_day.date())
                    end_date = min(check_out, end_of_day.date())

                    if end_date == check_out:
                        days_count = (end_date - start_date).days
                    else:
                        days_count = (end_date - start_date).days + 1

                    total_days_for_occupancy += days_count
                
                week_occupancy_counts.append({'week_number': row['week_number'], 'occupancy_count': total_days_for_occupancy})

            week_occupancy_counts_df = pd.DataFrame(week_occupancy_counts)
            week_occupancy_counts_df = week_occupancy_counts_df.groupby('week_number')['occupancy_count'].sum().reset_index()
            fig = px.line(week_occupancy_counts_df, 
                        x='week_number', 
                        y='occupancy_count', 
                        labels={'week_number': 'Week Number', 'occupancy_count': 'Room Occupancy'},
                        title=f"Room Occupancy per Week for {month_selection} {year_selection}")

        if selected_filter == 'Monthly':
            year_selection = st.selectbox("Year", transactions_df['check_in_time'].dt.year.unique().tolist())
            df = transactions_df[transactions_df['check_in_time'].dt.year == year_selection]

            monthly_occupancy = {}

            for month in range(1, 13):
                start_of_month = datetime(year_selection, month, 1)
                end_of_month = datetime(year_selection, month, calendar.monthrange(year_selection, month)[1])

                total_days_for_occupancy = 0
                
                for _, row in df.iterrows():
                    check_in = row['check_in_time'].date()
                    check_out = row['check_out_time'].date()

                    if check_out >= start_of_month.date() and check_in <= end_of_month.date():
                        start_date = max(check_in, start_of_month.date())
                        end_date = min(check_out, end_of_month.date())

                        if end_date == check_out:
                            days_count = (end_date - start_date).days
                        else:
                            days_count = (end_date - start_date).days + 1

                        total_days_for_occupancy += days_count
                
                month_name = calendar.month_name[month]
                monthly_occupancy[month_name] = total_days_for_occupancy

            month_occupancy_counts = pd.DataFrame(list(monthly_occupancy.items()), columns=['month_name', 'occupancy_count'])

            month_occupancy_counts['month_name'] = pd.Categorical(month_occupancy_counts['month_name'], 
                                                                    categories=calendar.month_name[1:], 
                                                                    ordered=True)
            month_occupancy_counts = month_occupancy_counts.sort_values('month_name')

            fig = px.line(month_occupancy_counts, 
                        x='month_name', 
                        y='occupancy_count', 
                        labels={'month_name': 'Month', 'occupancy_count': 'Room Occupancy'},
                        title=f"Room Occupancy per Month ({year_selection})")

        if selected_filter == 'Yearly':
            df = transactions_df
            df['year'] = df['check_in_time'].dt.year

            year_occupancy = {}

            for year in df['year'].unique():
                df_filtered = df[df['year'] == year]

                total_days_for_occupancy = 0
                
                for _, row in df_filtered.iterrows():
                    check_in = row['check_in_time'].date()
                    check_out = row['check_out_time'].date()

                    if check_out.year >= year and check_in.year <= year:
                        start_date = max(check_in, datetime(year, 1, 1).date())
                        end_date = min(check_out, datetime(year, 12, 31).date())

                        if end_date == check_out:
                            days_count = (end_date - start_date).days
                        else:
                            days_count = (end_date - start_date).days + 1

                        total_days_for_occupancy += days_count

                year_occupancy[year] = total_days_for_occupancy

            year_occupancy_counts = pd.DataFrame(list(year_occupancy.items()), columns=['year', 'occupancy_count'])
            year_occupancy_counts = year_occupancy_counts.sort_values(by='year').reset_index(drop=True)

            fig = px.line(
                year_occupancy_counts, 
                x='year', 
                y='occupancy_count', 
                labels={'year': 'Year', 'occupancy_count': 'Room Occupancy'},
                title="Room Occupancy per Year"
            )
            fig.update_xaxes(type='category')

    st.plotly_chart(fig, key='one_a')
    st.divider()