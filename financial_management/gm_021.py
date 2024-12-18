import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def gm_021(transactions_df, rooms_df, hotel_df, selected_hotel):
    data = {
        "Category": ["Staffing", "Utilities", "Supplies", "Others"],
        "Cost": [5000000, 2000000, 1500000, 1000000],
    }

    df_costs = pd.DataFrame(data)

    st.write("### Percentage of Operational Costs")
    fig = px.pie(
        df_costs,
        values="Cost",
        names="Category",
        title="Operational Costs Breakdown",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
    )

    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig)