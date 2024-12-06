import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import plotly.express as px

def generate_additional_revenue(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    data = {
        "date": date_range,
        "lunch": np.random.randint(100, 500, len(date_range)) * 1000,
        "pool_access": np.random.randint(50, 300, len(date_range)) * 1000,
        "breakfast": np.random.randint(100, 600, len(date_range)) * 1000,
        "buffet": np.random.randint(200, 700, len(date_range)) * 1000,
        "night_bar_access": np.random.randint(150, 500, len(date_range)) * 1000,
    }
    return pd.DataFrame(data)

def gm_006(transactions_df, rooms_df, hotel_df):
    selected_month = st.selectbox("Select Month", [datetime.now().strftime('%B')] + list(pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%B')))
    selected_year = st.selectbox("Select Year", [2024, 2023, 2022])

    selected_date = datetime.strptime(f"01-{selected_month}-{selected_year}", "%d-%B-%Y")
    month_start = selected_date.replace(day=1)
    month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    filtered_df = transactions_df[
        (transactions_df['check_in_time'].dt.date >= month_start.date()) &
        (transactions_df['check_in_time'].dt.date <= month_end.date())
    ]

    filtered_df['check_in_date'] = filtered_df['check_in_time'].dt.date
    daily_revenue = filtered_df.groupby('check_in_date').agg(
        total_revenue=('price', 'sum'),
        adr=('price', 'mean')
    ).reset_index()

    additional_revenue = generate_additional_revenue(month_start, month_end)

    daily_revenue['check_in_date'] = pd.to_datetime(daily_revenue['check_in_date'])
    additional_revenue['date'] = pd.to_datetime(additional_revenue['date'])

    combined_revenue = pd.merge(
        daily_revenue, 
        additional_revenue, 
        left_on='check_in_date', 
        right_on='date', 
        how='outer'
    ).fillna(0)

    combined_revenue['total_revenue_with_additional'] = (
        combined_revenue['total_revenue'] +
        combined_revenue['lunch'] +
        combined_revenue['pool_access'] +
        combined_revenue['breakfast'] +
        combined_revenue['buffet'] +
        combined_revenue['night_bar_access']
    )

    combined_revenue['heatmap_color'] = combined_revenue['total_revenue_with_additional']

    fig = px.bar(
        combined_revenue,
        x='check_in_date',
        y='total_revenue_with_additional',
        color='heatmap_color',
        color_continuous_scale='Viridis',
        title=f"Daily Revenue and ADR - {selected_month} {selected_year}",
        labels={'check_in_date': 'Date', 'total_revenue_with_additional': 'Total Revenue (Including Add-ons)', 'heatmap_color': 'Revenue Heatmap'}
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Date: %{x}</b><br>"
            "Revenue (Total): %{y}<br>"
            "ADR: %{customdata[0]:.2f}<br>"
            "Lunch: %{customdata[1]}<br>"
            "Pool Access: %{customdata[2]}<br>"
            "Breakfast: %{customdata[3]}<br>"
            "Buffet: %{customdata[4]}<br>"
            "Night Bar Access: %{customdata[5]}"
        ),
        customdata=combined_revenue[['adr', 'lunch', 'pool_access', 'breakfast', 'buffet', 'night_bar_access']].to_numpy()
    )

    fig.update_layout(
        yaxis=dict(title='Revenue (IDR)', showgrid=True),
        xaxis=dict(title='Date', showgrid=False),
        hovermode='x unified'
    )

    st.plotly_chart(fig)