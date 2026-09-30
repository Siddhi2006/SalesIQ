import streamlit as st
import pandas as pd
import os
import sys


# =========================================================
# PROJECT PATH
# =========================================================

base_dir = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)


from services.insights import generate_insights


def show_insights():

    # =========================================================
    # DATA PATH
    # =========================================================

    data_path = os.path.join(
        base_dir,
        "data",
        "INDIA_RETAIL_DATA.xlsx"
    )


    # =========================================================
    # LOAD DATASET
    # =========================================================

    try:

        df = pd.read_excel(
            data_path
        )

    except Exception as e:

        st.error(
            f"Unable to load dataset: {str(e)}"
        )

        return


    # =========================================================
    # DATA PREPARATION
    # =========================================================

    try:

        df["Order Date"] = pd.to_datetime(
            df["Order Date"]
        )

        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"]
        )

        df["Order Year"] = (
            df["Order Date"].dt.year
        )

        df["Order Month"] = (
            df["Order Date"].dt.month
        )

        df["Year-Month"] = (
            df["Order Date"]
            .dt.to_period("M")
            .astype(str)
        )

        df["Shipping Days"] = (
            df["Ship Date"] - df["Order Date"]
        ).dt.days

    except Exception as e:

        st.error(
            f"Unable to prepare dataset: {str(e)}"
        )

        return


    # =========================================================
    # PAGE TITLE
    # =========================================================

    st.title(
        "Business Insights"
    )

    st.write(
        "SalesIQ automatically analyzes the historical "
        "sales data and generates important business "
        "insights."
    )

    st.divider()


    # =========================================================
    # FILTERS
    # =========================================================

    st.sidebar.header(
        "Insight Filters"
    )


    available_years = sorted(
        df["Order Year"]
        .dropna()
        .unique()
    )

    selected_years = st.sidebar.multiselect(
        "Select Year",
        available_years,
        default=available_years
    )


    available_regions = sorted(
        df["Region"]
        .dropna()
        .unique()
    )

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        available_regions,
        default=available_regions
    )


    available_segments = sorted(
        df["Segment"]
        .dropna()
        .unique()
    )

    selected_segments = st.sidebar.multiselect(
        "Select Segment",
        available_segments,
        default=available_segments
    )


    # =========================================================
    # APPLY FILTERS
    # =========================================================

    filtered_df = df[
        df["Order Year"].isin(selected_years)
        & df["Region"].isin(selected_regions)
        & df["Segment"].isin(selected_segments)
    ].copy()


    # =========================================================
    # EMPTY DATA CHECK
    # =========================================================

    if filtered_df.empty:

        st.warning(
            "No data available for the selected filters."
        )

        return


    # =========================================================
    # BASIC SUMMARY
    # =========================================================

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["Profit"].sum()

    total_orders = len(filtered_df)

    total_quantity = (
        filtered_df["QtyOrdered"].sum()
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )


    # =========================================================
    # SUMMARY METRICS
    # =========================================================

    st.header(
        "Business Summary"
    )

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Total Sales",
            f"INR {total_sales:,.2f}"
        )


    with col2:

        st.metric(
            "Total Profit",
            f"INR {total_profit:,.2f}"
        )


    with col3:

        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )


    with col4:

        st.metric(
            "Total Quantity",
            f"{total_quantity:,}"
        )


    with col5:

        st.metric(
            "Average Order Value",
            f"INR {average_order_value:,.2f}"
        )


    st.divider()


    # =========================================================
    # AUTOMATED INSIGHTS
    # =========================================================

    st.header(
        "Automated Business Insights"
    )


    insights = generate_insights(
        filtered_df
    )


    if not insights:

        st.info(
            "No insights could be generated "
            "for the selected data."
        )

    else:

        for index, insight in enumerate(
            insights,
            start=1
        ):

            st.info(
                f"Insight {index}: {insight}"
            )


    st.divider()


    # =========================================================
    # TOP REGION
    # =========================================================

    st.header(
        "Regional Analysis"
    )


    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    if not region_sales.empty:

        top_region = region_sales.index[0]

        top_region_sales = (
            region_sales.iloc[0]
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Best Performing Region",
                top_region
            )


        with col2:

            st.metric(
                "Regional Sales",
                f"INR {top_region_sales:,.2f}"
            )


    st.divider()


    # =========================================================
    # TOP PRODUCT
    # =========================================================

    st.header(
        "Product Analysis"
    )


    product_sales = (
        filtered_df
        .groupby("Product Type")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    if not product_sales.empty:

        top_product = product_sales.index[0]

        top_product_sales = (
            product_sales.iloc[0]
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Best Selling Product Type",
                top_product
            )


        with col2:

            st.metric(
                "Product Sales",
                f"INR {top_product_sales:,.2f}"
            )


    st.divider()


    # =========================================================
    # PROFIT ANALYSIS
    # =========================================================

    st.header(
        "Profitability Analysis"
    )


    product_profit = (
        filtered_df
        .groupby("Product Type")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    if not product_profit.empty:

        best_profit_product = (
            product_profit.index[0]
        )

        best_profit_value = (
            product_profit.iloc[0]
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Most Profitable Product Type",
                best_profit_product
            )


        with col2:

            st.metric(
                "Generated Profit",
                f"INR {best_profit_value:,.2f}"
            )


    st.divider()


    # =========================================================
    # MONTHLY PERFORMANCE
    # =========================================================

    st.header(
        "Monthly Performance"
    )


    monthly_sales = (
        filtered_df
        .groupby("Year-Month")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    if not monthly_sales.empty:

        best_month = monthly_sales.index[0]

        best_month_sales = (
            monthly_sales.iloc[0]
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Best Sales Month",
                best_month
            )


        with col2:

            st.metric(
                "Monthly Sales",
                f"INR {best_month_sales:,.2f}"
            )


    st.divider()


    # =========================================================
    # SHIPPING ANALYSIS
    # =========================================================

    st.header(
        "Shipping Analysis"
    )


    if "Shipping Days" in filtered_df.columns:

        average_shipping_days = (
            filtered_df["Shipping Days"]
            .mean()
        )

        max_shipping_days = (
            filtered_df["Shipping Days"]
            .max()
        )

        min_shipping_days = (
            filtered_df["Shipping Days"]
            .min()
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Shipping Time",
                f"{average_shipping_days:.1f} days"
            )


        with col2:

            st.metric(
                "Maximum Shipping Time",
                f"{max_shipping_days:.0f} days"
            )


        with col3:

            st.metric(
                "Minimum Shipping Time",
                f"{min_shipping_days:.0f} days"
            )


    st.divider()


    # =========================================================
    # PROFITABILITY STATUS
    # =========================================================

    st.header(
        "Overall Profitability"
    )


    if total_profit > 0:

        st.success(
            f"The selected business data shows "
            f"positive overall profit of "
            f"INR {total_profit:,.2f}."
        )

    elif total_profit < 0:

        st.warning(
            f"The selected business data shows "
            f"a negative overall profit of "
            f"INR {total_profit:,.2f}."
        )

    else:

        st.info(
            "The selected business data has "
            "approximately zero overall profit."
        )


    # =========================================================
    # FILTERED DATA
    # =========================================================

    with st.expander(
        "View Analyzed Data"
    ):

        st.write(
            f"Number of records analyzed: "
            f"{len(filtered_df):,}"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True
        )


    # =========================================================
    # FOOTER
    # =========================================================

    st.divider()

    st.caption(
        "SalesIQ | AI-Powered Sales Analytics and "
        "Decision Support Platform"
    )