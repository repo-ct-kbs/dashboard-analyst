import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_020(transactions_df, rooms_df, hotel_df, selected_hotel):
    data = {
        "Segment": ["Room", "F&B", "Services", "Others"],
        "Revenue": [5000000, 3000000, 1500000, 1000000],
    }

    df_revenue = pd.DataFrame(data)

    st.write("### Revenue by Segment")
    fig = px.bar(
        df_revenue,
        x="Segment",
        y="Revenue",
        text="Revenue",
        title="Revenue Segmentation",
        labels={"Revenue": "Revenue (Currency)", "Segment": "Segment"},
        color="Segment",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig.update_layout(yaxis=dict(title="Revenue (Currency)"), xaxis=dict(title="Segment"))
    st.plotly_chart(fig)