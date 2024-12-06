import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def generate_popular_items_data():
    categories = ['Food', 'Beverage', 'Spa']
    items = {
        'Food': ['Bread', 'Pizza', 'Pasta', 'Burger', 'Salad'],
        'Beverage': ['Wine', 'Beer', 'Juice', 'Soda', 'Cocktail'],
        'Spa': ['Massage', 'Facial', 'Sauna', 'Manicure', 'Pedicure']
    }
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='MS')
    seasons = {
        'Winter': ['January', 'February', 'December'],
        'Spring': ['March', 'April', 'May'],
        'Summer': ['June', 'July', 'August'],
        'Fall': ['September', 'October', 'November']
    }

    data = []
    for month in months:
        for category, item_list in items.items():
            for item in item_list:
                units_sold = random.randint(50, 300)
                revenue = units_sold * random.uniform(10, 50)
                season = next(
                    s for s, months in seasons.items()
                    if month.strftime('%B') in months
                )
                data.append({
                    'month': month,
                    'season': season,
                    'category': category,
                    'item': item,
                    'units_sold': units_sold,
                    'revenue': round(revenue, 2)
                })
    return pd.DataFrame(data)



def gm_013(transactions_df, rooms_df, hotel_df, selected_hotel):
    popular_items_data = generate_popular_items_data()

    st.write("### Popular Items and Seasonal Trends")

    time_filter = st.radio("Filter by Time", ['Per Month', 'Per Season'])
    category_filter = st.selectbox("Filter by Category", popular_items_data['category'].unique())

    if time_filter == 'Per Month':
        selected_time = st.selectbox(
            "Select Month", 
            popular_items_data['month'].dt.strftime('%B %Y').unique()
        )
        filtered_data = popular_items_data[
            (popular_items_data['category'] == category_filter) &
            (popular_items_data['month'].dt.strftime('%B %Y') == selected_time)
        ]
    else:
        selected_time = st.selectbox(
            "Select Season", 
            popular_items_data['season'].unique()
        )
        filtered_data = popular_items_data[
            (popular_items_data['category'] == category_filter) &
            (popular_items_data['season'] == selected_time)
        ]

    st.write(f"Data for {category_filter} in {selected_time}")
    st.dataframe(filtered_data)

    chart_metric = st.radio("Select Metric", ['units_sold', 'revenue'])
    chart_title = "Units Sold" if chart_metric == 'units_sold' else "Revenue"

    bar_chart_data = filtered_data.groupby('item')[chart_metric].sum().reset_index()

    fig_bar = px.bar(
        bar_chart_data,
        x='item',
        y=chart_metric,
        title=f"{chart_title} for {category_filter} in {selected_time}",
        labels={chart_metric: chart_title, 'item': 'Item'},
        color=chart_metric,
        color_continuous_scale='Blues',
        text=chart_metric
    )

    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar)

