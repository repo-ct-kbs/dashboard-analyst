import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def generate_inventory_data():
    item_types = ['Food', 'Beverage', 'Room Supplies']
    outlets = ['Kitchen', 'Bar', 'Housekeeping']
    items = {
        'Food': ['Bread', 'Eggs', 'Meat', 'Vegetables', 'Fruits'],
        'Beverage': ['Wine', 'Beer', 'Juice', 'Soda', 'Water'],
        'Room Supplies': ['Towels', 'Shampoo', 'Soap', 'Toilet Paper', 'Laundry Bags']
    }
    
    data = []
    for outlet in outlets:
        for item_type, item_list in items.items():
            for item in item_list:
                initial_units = random.randint(50, 200)
                units_added = random.randint(0, 100)
                units_sold_or_used = random.randint(10, 150)
                current_units = initial_units + units_added - units_sold_or_used
                data.append({
                    'outlet': outlet,
                    'item_type': item_type,
                    'item': item,
                    'initial_units': initial_units,
                    'units_added': units_added,
                    'units_sold_or_used': units_sold_or_used,
                    'current_units': max(current_units, 0)
                })
    return pd.DataFrame(data)


def gm_012(transactions_df, rooms_df, hotel_df, selected_hotel):
    inventory_data = generate_inventory_data()

    st.write("### Stock and Inventory Levels")

    selected_item_type = st.selectbox("Filter by Item Type", inventory_data['item_type'].unique())
    selected_outlet = st.selectbox("Filter by Outlet", inventory_data['outlet'].unique())

    filtered_inventory = inventory_data[
        (inventory_data['item_type'] == selected_item_type) &
        (inventory_data['outlet'] == selected_outlet)
    ]

    st.dataframe(filtered_inventory)

    bar_data = filtered_inventory[['item', 'current_units']]

    fig_bar = px.bar(
        bar_data,
        x='item',
        y='current_units',
        title=f'Stock Levels for {selected_item_type} in {selected_outlet}',
        labels={'current_units': 'Stock Count', 'item': 'Item'},
        color='current_units',
        color_continuous_scale='Greens',
        text='current_units'
    )

    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar)

    low_stock_items = filtered_inventory[filtered_inventory['current_units'] < 30]

    for _, row in low_stock_items.iterrows():
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row['current_units'],
            title={'text': f"Stock for {row['item']}"},
            gauge={
                'axis': {'range': [0, 200]},
                'bar': {'color': "red" if row['current_units'] < 10 else "orange"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 150], 'color': "yellow"},
                    {'range': [150, 200], 'color': "lightgreen"}
                ],
            }
        ))
        st.plotly_chart(fig_gauge)

