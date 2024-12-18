import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

# def generate_inventory_data():
#     item_types = ['Food', 'Beverage', 'Room Supplies']
#     outlets = ['Kitchen', 'Bar', 'Housekeeping']
#     items = {
#         'Food': ['Bread', 'Eggs', 'Meat', 'Vegetables', 'Fruits'],
#         'Beverage': ['Wine', 'Beer', 'Juice', 'Soda', 'Water'],
#         'Room Supplies': ['Towels', 'Shampoo', 'Soap', 'Toilet Paper', 'Laundry Bags']
#     }
    
#     data = []
#     for outlet in outlets:
#         for item_type, item_list in items.items():
#             for item in item_list:
#                 initial_units = random.randint(50, 200)
#                 units_added = random.randint(0, 100)
#                 units_sold_or_used = random.randint(10, 150)
#                 current_units = initial_units + units_added - units_sold_or_used
#                 data.append({
#                     'outlet': outlet,
#                     'item_type': item_type,
#                     'item': item,
#                     'initial_units': initial_units,
#                     'units_added': units_added,
#                     'units_sold_or_used': units_sold_or_used,
#                     'current_units': max(current_units, 0)
#                 })
#     return pd.DataFrame(data)


# def gm_012(transactions_df, rooms_df, hotel_df, selected_hotel):
#     inventory_data = generate_inventory_data()

#     selected_item_type = st.selectbox("Filter by Item Type", inventory_data['item_type'].unique())
#     selected_outlet = st.selectbox("Filter by Outlet", inventory_data['outlet'].unique())

#     filtered_inventory = inventory_data[
#         (inventory_data['item_type'] == selected_item_type) &
#         (inventory_data['outlet'] == selected_outlet)
#     ]

#     st.dataframe(filtered_inventory)

#     bar_data = filtered_inventory[['item', 'current_units']]

#     fig_bar = px.bar(
#         bar_data,
#         x='item',
#         y='current_units',
#         title=f'Stock Levels for {selected_item_type} in {selected_outlet}',
#         labels={'current_units': 'Stock Count', 'item': 'Item'},
#         color='current_units',
#         color_continuous_scale='Greens',
#         text='current_units'
#     )

#     fig_bar.update_traces(textposition='outside')
#     st.plotly_chart(fig_bar)

#     low_stock_items = filtered_inventory[filtered_inventory['current_units'] < 30]

#     for _, row in low_stock_items.iterrows():
#         fig_gauge = go.Figure(go.Indicator(
#             mode="gauge+number",
#             value=row['current_units'],
#             title={'text': f"Stock for {row['item']}"},
#             gauge={
#                 'axis': {'range': [0, 200]},
#                 'bar': {'color': "red" if row['current_units'] < 10 else "orange"},
#                 'steps': [
#                     {'range': [0, 50], 'color': "lightcoral"},
#                     {'range': [50, 150], 'color': "yellow"},
#                     {'range': [150, 200], 'color': "lightgreen"}
#                 ],
#             }
#         ))
#         st.plotly_chart(fig_gauge)


def gm_012(transactions_df, rooms_df, hotel_df, selected_hotel):
    data = {
        "Outlet": ["Outlet A", "Outlet A", "Outlet B", "Outlet B", "Outlet C", "Outlet C"],
        "Item": ["Rice", "Chicken", "Rice", "Chicken", "Rice", "Chicken"],
        "Category": ["Grains", "Meat", "Grains", "Meat", "Grains", "Meat"],
        "Stock": [50, 10, 30, 5, 70, 20],
        "Reorder_Level": [20, 5, 15, 3, 25, 10],
    }

    heatmap_data = {
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Rice": [80, 60, 40, 20],
        "Chicken": [50, 30, 15, 5],
    }

    stock_df = pd.DataFrame(data)
    heatmap_df = pd.DataFrame(heatmap_data)

    st.dataframe(stock_df)

    st.write("### Horizontal Bar Chart: Stock Levels by Item")
    fig_bar = px.bar(
        stock_df,
        x="Stock",
        y="Item",
        color="Outlet",
        title="Stock Levels by Item",
        orientation="h",
        labels={"Stock": "Stock (Units)", "Item": "Item Name"},
        barmode="group",
    )
    st.plotly_chart(fig_bar)

    st.write("### Gauge Chart: Stock Level Indicators")
    for index, row in stock_df.iterrows():
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["Stock"],
                title={"text": f"{row['Item']} at {row['Outlet']}"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green" if row["Stock"] > row["Reorder_Level"] else "red"},
                    "steps": [
                        {"range": [0, row["Reorder_Level"]], "color": "orange"},
                        {"range": [row["Reorder_Level"], 100], "color": "lightgreen"},
                    ],
                },
            )
        )
        st.plotly_chart(fig_gauge)

    st.write("### Heatmap: Weekly Stock Levels")
    heatmap_df_melted = heatmap_df.melt(id_vars=["Week"], var_name="Item", value_name="Stock")

    fig_heatmap = px.density_heatmap(
        heatmap_df_melted,
        x="Week",
        y="Item",
        z="Stock",
        color_continuous_scale="Viridis",
        title="Weekly Stock Levels",
        labels={"Stock": "Stock Level", "Week": "Week", "Item": "Item"},
    )
    st.plotly_chart(fig_heatmap)

    st.divider()

    data = {
        "Item": ["Rice", "Oil", "Chicken", "Vegetables", "Spices", "Milk"],
        "Stock Level (%)": [25, 55, 75, 10, 40, 85],
        "Category": ["Grains", "Cooking", "Meat", "Produce", "Seasoning", "Dairy"],
        "Outlet": ["Outlet A", "Outlet A", "Outlet A", "Outlet A", "Outlet A", "Outlet A"],
    }

    df_stock = pd.DataFrame(data)

    def get_stock_color(stock_level):
        if stock_level <= 30:
            return "red"
        elif 30 < stock_level <= 60:
            return "yellow"
        else:
            return "green"

    df_stock["Stock Level Color"] = df_stock["Stock Level (%)"].apply(get_stock_color)

    st.write("### Stock Conditions by Outlet v2")
    st.write(df_stock[["Item", "Stock Level (%)", "Category", "Outlet"]])

    fig = px.bar(
        df_stock,
        x="Stock Level (%)",
        y="Item",
        color="Stock Level Color",
        title="Stock Levels by Item",
        text="Stock Level (%)",
        orientation="h",
        color_discrete_map={"red": "red", "yellow": "yellow", "green": "green"},
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis=dict(range=[0, 100]), showlegend=False)

    st.plotly_chart(fig)