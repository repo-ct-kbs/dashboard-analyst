import random
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_019(transactions_df, rooms_df, hotel_df, selected_hotel):
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    historical_rates = 1000 + np.sin(np.linspace(0, 12 * np.pi, len(dates))) * 200 + np.random.normal(0, 50, len(dates))
    forecast_dates = pd.date_range(start="2024-01-01", end="2024-03-31", freq="D")
    forecast_rates = 1100 + np.sin(np.linspace(0, 3 * np.pi, len(forecast_dates))) * 200 + np.random.normal(0, 50, len(forecast_dates))
    confidence_intervals = np.random.uniform(50, 100, len(forecast_dates))

    historical_data = pd.DataFrame({"Date": dates, "Rate": historical_rates, "Type": "Historical"})
    forecast_data = pd.DataFrame({
        "Date": forecast_dates,
        "Rate": forecast_rates,
        "Lower": forecast_rates - confidence_intervals,
        "Upper": forecast_rates + confidence_intervals,
        "Type": "Forecast"
    })

    combined_data = pd.concat([historical_data, forecast_data])

    st.write("### Line Chart: Historical and Forecasted Room Rates")
    fig_line = go.Figure()

    fig_line.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["Rate"],
            mode="lines",
            name="Historical Rates",
            line=dict(color="blue"),
        )
    )

    fig_line.add_trace(
        go.Scatter(
            x=forecast_data["Date"],
            y=forecast_data["Rate"],
            mode="lines",
            name="Forecasted Rates",
            line=dict(color="orange"),
        )
    )

    fig_line.add_trace(
        go.Scatter(
            x=pd.concat([forecast_data["Date"], forecast_data["Date"][::-1]]),
            y=pd.concat([forecast_data["Upper"], forecast_data["Lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(255,165,0,0.2)",
            line=dict(color="rgba(255,165,0,0)"),
            name="Confidence Interval",
        )
    )

    fig_line.update_layout(
        title="Room Rate Forecasting vs Historical Data",
        xaxis_title="Date",
        yaxis_title="Room Rate (Currency)",
        legend_title="Type",
    )
    st.plotly_chart(fig_line)

    st.write("### Heatmap: Seasonal Trends in Room Rates")
    historical_data["Month"] = historical_data["Date"].dt.month
    historical_data["Day"] = historical_data["Date"].dt.day

    heatmap_data = historical_data.pivot_table(
        index="Month", columns="Day", values="Rate", aggfunc="mean"
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale="Viridis",
        title="Seasonal Room Rate Trends",
        labels={"color": "Room Rate (Currency)"},
        x=list(range(1, 32)),
        y=list(range(1, 13)),
    )

    fig_heatmap.update_layout(
        xaxis_title="Day of the Month",
        yaxis_title="Month",
        coloraxis_colorbar=dict(title="Room Rate"),
    )

    st.plotly_chart(fig_heatmap)