import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta


def gm_005(transactions_df, rooms_df, hotel_df):
    x_months = st.slider("Select number of months for ALOS calculation", min_value=1, max_value=12, value=6)

    today = datetime.today()
    start_date = today - timedelta(days=30 * x_months)

    filtered_df = transactions_df[
        transactions_df['check_in_time'].dt.date >= start_date.date()
    ]

    filtered_df['Month-Year'] = filtered_df['check_in_time'].dt.to_period('M').astype(str)

    alos_df = filtered_df.groupby('Month-Year')['night_stay'].mean().reset_index()
    alos_df.rename(columns={'night_stay': 'ALOS'}, inplace=True)

    alos_df['Month-Year'] = pd.to_datetime(alos_df['Month-Year'])
    alos_df = alos_df.sort_values(by='Month-Year')

    alos_df['Month-Year'] = alos_df['Month-Year'].dt.strftime('%b %Y')

    fig = px.line(
        alos_df,
        x='Month-Year',
        y='ALOS',
        title=f"Average Length of Stay (Last {x_months} Months)",
        labels={'ALOS': 'Average Length of Stay (Days)', 'Month-Year': 'Month'},
        line_shape='spline',
        markers=True,
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title='ALOS (Days)', showgrid=True),
        xaxis=dict(title='Month', showgrid=False),
        hovermode='x unified',
    )

    st.plotly_chart(fig)