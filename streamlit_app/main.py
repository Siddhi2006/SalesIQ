import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SalesIQ",
    layout="wide"
)


# =========================================================
# IMPORT PAGE FUNCTIONS
# =========================================================

from dashboard import show_dashboard
from prediction import show_prediction
from decision_support import show_decision_support
from insights import show_insights


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("SalesIQ")

st.sidebar.write(
    "AI-Powered Sales Analytics and "
    "Decision Support Platform"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Dashboard",
        "Sales Prediction",
        "Decision Support",
        "Business Insights"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.title(
        "SalesIQ"
    )

    st.subheader(
        "AI-Powered Sales Analytics and "
        "Decision Support Platform"
    )

    st.write(
        "SalesIQ analyzes historical sales data, "
        "predicts sales using Machine Learning, "
        "generates business insights and supports "
        "what-if decision making."
    )

    st.divider()

    st.header(
        "How SalesIQ Works"
    )

    st.write(
        "Historical Data -> "
        "Data Processing -> "
        "Machine Learning -> "
        "Sales Prediction -> "
        "Business Insights -> "
        "Decision Support"
    )

    st.divider()

    st.header(
        "Main Features"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Analytics Dashboard"
        )

        st.write(
            "Analyze sales, profit, products, "
            "regions, cities and order trends."
        )

        st.subheader(
            "Sales Prediction"
        )

        st.write(
            "Predict expected sales using a "
            "trained Random Forest model."
        )

        st.subheader(
            "Business Insights"
        )

        st.write(
            "Automatically identify important "
            "patterns and business performance."
        )

    with col2:

        st.subheader(
            "Decision Support"
        )

        st.write(
            "Compare current and proposed scenarios "
            "to understand expected sales changes."
        )

        st.subheader(
            "Machine Learning"
        )

        st.write(
            "SalesIQ uses historical retail data "
            "and supervised Machine Learning "
            "for sales prediction."
        )

        st.subheader(
            "Flask API"
        )

        st.write(
            "The Flask backend provides the prediction "
            "API used by the Streamlit application."
        )

    st.divider()

    st.info(
        "Use the navigation menu to explore "
        "different SalesIQ modules."
    )


# =========================================================
# DASHBOARD
# =========================================================

elif page == "Dashboard":

    show_dashboard()


# =========================================================
# SALES PREDICTION
# =========================================================

elif page == "Sales Prediction":

    show_prediction()


# =========================================================
# DECISION SUPPORT
# =========================================================

elif page == "Decision Support":

    show_decision_support()


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "Business Insights":

    show_insights()