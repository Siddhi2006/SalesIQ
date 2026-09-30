import streamlit as st
import pandas as pd
import os
import plotly.express as px


def show_dashboard():

    # =========================================================
    # LOAD DATASET
    # =========================================================

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    data_path = os.path.join(
        base_dir,
        "data",
        "INDIA_RETAIL_DATA.xlsx"
    )

    try:
        df = pd.read_excel(data_path)

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

        df["Order Month Name"] = (
            df["Order Date"].dt.strftime("%b")
        )

        df["Order Quarter"] = (
            df["Order Date"].dt.quarter
        )

        df["Shipping Days"] = (
            df["Ship Date"] - df["Order Date"]
        ).dt.days

        df["Year-Month"] = (
            df["Order Date"].dt.to_period("M")
            .astype(str)
        )

    except Exception as e:

        st.error(
            f"Unable to prepare dataset: {str(e)}"
        )

        return


    # =========================================================
    # PAGE TITLE
    # =========================================================

    st.title(
        "SalesIQ Analytics Dashboard"
    )

    st.write(
        "Analyze sales performance, profitability, "
        "products, regions, cities and order trends."
    )

    st.divider()


    # =========================================================
    # SIDEBAR FILTERS
    # =========================================================

    st.sidebar.header(
        "Dashboard Filters"
    )


    # Year filter

    available_years = sorted(
        df["Order Year"].dropna().unique()
    )

    selected_years = st.sidebar.multiselect(
        "Select Year",
        available_years,
        default=available_years
    )


    # Region filter

    available_regions = sorted(
        df["Region"].dropna().unique()
    )

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        available_regions,
        default=available_regions
    )


    # Segment filter

    available_segments = sorted(
        df["Segment"].dropna().unique()
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
    # KEY PERFORMANCE INDICATORS
    # =========================================================

    st.header(
        "Key Performance Indicators"
    )

    total_sales = filtered_df["Sales"].sum()

    total_orders = len(filtered_df)

    total_quantity = filtered_df["QtyOrdered"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    total_profit = filtered_df["Profit"].sum()


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Total Sales",
            f"INR {total_sales:,.2f}"
        )


    with col2:

        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )


    with col3:

        st.metric(
            "Total Quantity",
            f"{total_quantity:,}"
        )


    with col4:

        st.metric(
            "Average Order Value",
            f"INR {average_order_value:,.2f}"
        )


    with col5:

        st.metric(
            "Total Profit",
            f"INR {total_profit:,.2f}"
        )


    st.divider()


    # =========================================================
    # MONTHLY SALES TREND
    # =========================================================

    st.header(
        "Monthly Sales Trend"
    )

    monthly_sales = (
        filtered_df
        .groupby("Year-Month", as_index=False)["Sales"]
        .sum()
    )

    monthly_sales = monthly_sales.sort_values(
        "Year-Month"
    )


    fig_monthly = px.line(
        monthly_sales,
        x="Year-Month",
        y="Sales",
        markers=True,
        title="Monthly Sales"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


    st.divider()


    # =========================================================
    # REGION ANALYSIS
    # =========================================================

    st.header(
        "Regional Performance"
    )

    region_sales = (
        filtered_df
        .groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    region_profit = (
        filtered_df
        .groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
    )


    col1, col2 = st.columns(2)


    with col1:

        fig_region_sales = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            title="Sales by Region"
        )

        fig_region_sales.update_layout(
            xaxis_title="Region",
            yaxis_title="Sales"
        )

        st.plotly_chart(
            fig_region_sales,
            use_container_width=True
        )


    with col2:

        fig_region_profit = px.bar(
            region_profit,
            x="Region",
            y="Profit",
            title="Profit by Region"
        )

        fig_region_profit.update_layout(
            xaxis_title="Region",
            yaxis_title="Profit"
        )

        st.plotly_chart(
            fig_region_profit,
            use_container_width=True
        )


    st.divider()


    # =========================================================
    # PRODUCT ANALYSIS
    # =========================================================

    st.header(
        "Product Performance"
    )


    # Top products by sales

    top_product_sales = (
        filtered_df
        .groupby("Product Type", as_index=False)["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )


    # Top products by quantity

    top_product_quantity = (
        filtered_df
        .groupby("Product Type", as_index=False)["QtyOrdered"]
        .sum()
        .sort_values(
            "QtyOrdered",
            ascending=False
        )
        .head(10)
    )


    col1, col2 = st.columns(2)


    with col1:

        fig_product_sales = px.bar(
            top_product_sales,
            x="Sales",
            y="Product Type",
            orientation="h",
            title="Top 10 Product Types by Sales"
        )

        fig_product_sales.update_layout(
            xaxis_title="Sales",
            yaxis_title="Product Type"
        )

        st.plotly_chart(
            fig_product_sales,
            use_container_width=True
        )


    with col2:

        fig_product_quantity = px.bar(
            top_product_quantity,
            x="QtyOrdered",
            y="Product Type",
            orientation="h",
            title="Top 10 Product Types by Quantity"
        )

        fig_product_quantity.update_layout(
            xaxis_title="Quantity",
            yaxis_title="Product Type"
        )

        st.plotly_chart(
            fig_product_quantity,
            use_container_width=True
        )


    st.divider()


    # =========================================================
    # SEGMENT ANALYSIS
    # =========================================================

    st.header(
        "Sales Distribution by Segment"
    )


    segment_sales = (
        filtered_df
        .groupby("Segment", as_index=False)["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        title="Sales by Segment"
    )


    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )


    st.divider()


    # =========================================================
    # CITY ANALYSIS
    # =========================================================

    st.header(
        "Top Cities by Sales"
    )


    top_cities = (
        filtered_df
        .groupby("City", as_index=False)["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )


    fig_cities = px.bar(
        top_cities,
        x="Sales",
        y="City",
        orientation="h",
        title="Top 10 Cities by Sales"
    )


    fig_cities.update_layout(
        xaxis_title="Sales",
        yaxis_title="City"
    )


    st.plotly_chart(
        fig_cities,
        use_container_width=True
    )


    st.divider()


    # =========================================================
    # PROFITABLE PRODUCTS
    # =========================================================

    st.header(
        "Top Product Types by Profit"
    )


    top_profit_products = (
        filtered_df
        .groupby("Product Type", as_index=False)["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
        .head(10)
    )


    fig_profit_products = px.bar(
        top_profit_products,
        x="Profit",
        y="Product Type",
        orientation="h",
        title="Top 10 Product Types by Profit"
    )


    fig_profit_products.update_layout(
        xaxis_title="Profit",
        yaxis_title="Product Type"
    )


    st.plotly_chart(
        fig_profit_products,
        use_container_width=True
    )


    st.divider()


    # =========================================================
    # SUMMARY INFORMATION
    # =========================================================

    st.header(
        "Business Summary"
    )


    best_region = (
        region_sales.iloc[0]["Region"]
        if not region_sales.empty
        else "N/A"
    )


    best_region_sales = (
        region_sales.iloc[0]["Sales"]
        if not region_sales.empty
        else 0
    )


    best_product = (
        top_product_sales.iloc[0]["Product Type"]
        if not top_product_sales.empty
        else "N/A"
    )


    best_product_sales = (
        top_product_sales.iloc[0]["Sales"]
        if not top_product_sales.empty
        else 0
    )


    best_city = (
        top_cities.iloc[0]["City"]
        if not top_cities.empty
        else "N/A"
    )


    best_city_sales = (
        top_cities.iloc[0]["Sales"]
        if not top_cities.empty
        else 0
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.info(
            f"Top region: {best_region}\n\n"
            f"Sales: INR {best_region_sales:,.2f}"
        )


    with col2:

        st.info(
            f"Top product type: {best_product}\n\n"
            f"Sales: INR {best_product_sales:,.2f}"
        )


    with col3:

        st.info(
            f"Top city: {best_city}\n\n"
            f"Sales: INR {best_city_sales:,.2f}"
        )


    st.divider()


    # =========================================================
    # FILTERED DATA
    # =========================================================

    with st.expander(
        "View Filtered Dataset"
    ):

        st.write(
            f"Showing {len(filtered_df):,} records."
        )

        st.dataframe(
            filtered_df,
            use_container_width=True
        )


    # =========================================================
    # FOOTER
    # =========================================================

    st.caption(
        "SalesIQ | AI-Powered Sales Analytics and "
        "Decision Support Platform"
    )