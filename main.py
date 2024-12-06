import streamlit as st

pages = {
    "Operational Overview": [
        st.Page("views/operational_overview.py",),
    ],
    "Financial Management": [
        st.Page("views/financial_management.py",)
    ]
}

pg = st.navigation(pages)
pg.run()
