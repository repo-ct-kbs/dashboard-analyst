import streamlit as st

pages = {
    "Operational Overview": [
        st.Page("pages/operational_overview/real-time_hotel_status.py", title=""),
        st.Page("pages/operational_overview/front_office_summary.py", title=""),
        st.Page("pages/operational_overview/housekeeping_&_maintenance.py", title=""),
        st.Page("pages/operational_overview/food_&_beverage_operations.py", title=""),
        st.Page("pages/operational_overview/room_management.py", title=""),
    ],
    # "Financial Management": [
    #     st.Page("pages/financial_management/.py", title=""),
    # ],
    # "Sales and Marketing Performance": [
    #     st.Page("pages/sales_and_marketing_performance/.py", title=""),
    # ],
    # "Human Resources and Staff Management": [
    #     st.Page("pages/human_resources_and_staff_management/.py", title=""),
    # ],
    # "Guest Experience Management": [
    #     st.Page("pages/guest_experience_management/.py", title=""),
    # ],
    # "Security and Compliance Monitoring": [
    #     st.Page("pages/security_and_compliance_monitoring/.py", title=""),
    # ],
    # "Strategic Insights and Reporting": [
    #     st.Page("pages/strategic_insights_and_reporting/.py", title=""),
    # ],
    # "Property Management System (PMS) Integration": [
    #     st.Page("pages/property_management_system_(pms)_integration/.py", title=""),
    # ],
    # "Environment and Sustainability Monitoring": [
    #     st.Page("pages/environment_and_sustainability_monitoring/.py", title=""),
    # ],
    # "Alerts and Notifications": [
    #     st.Page("pages/alerts_and_notifications/.py", title=""),
    # ],
    # "Business Intelligence and Analytics": [
    #     st.Page("pages/business_intelligence_and_analytics/.py", title=""),
    # ],
    # "Mobile Accessibility": [
    #     st.Page("pages/mobile_accessibility.py", title=""),
    # ],
}

pg = st.navigation(pages)
pg.run()
