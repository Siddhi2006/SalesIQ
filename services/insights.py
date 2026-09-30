import pandas as pd


def generate_insights(df):
    """
    Generate automated business insights
    from sales data.
    """

    insights = []

    # =====================================================
    # CHECK DATA
    # =====================================================

    if df.empty:

        return [
            "No data available for generating insights."
        ]

    # =====================================================
    # 1. BEST REGION
    # =====================================================

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    if not region_sales.empty:

        best_region = region_sales.index[0]
        best_region_sales = region_sales.iloc[0]

        insights.append(
            f"{best_region} is the top-performing "
            f"region with total sales of "
            f"INR {best_region_sales:,.2f}."
        )

    # =====================================================
    # 2. LOWEST REGION
    # =====================================================

    if len(region_sales) > 1:

        lowest_region = region_sales.index[-1]
        lowest_region_sales = region_sales.iloc[-1]

        insights.append(
            f"{lowest_region} has the lowest regional "
            f"sales at INR {lowest_region_sales:,.2f}."
        )

    # =====================================================
    # 3. TOP PRODUCT
    # =====================================================

    product_sales = (
        df.groupby("Product Type")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    if not product_sales.empty:

        top_product = product_sales.index[0]
        top_product_sales = product_sales.iloc[0]

        insights.append(
            f"{top_product} is the highest-selling "
            f"product type with sales of "
            f"INR {top_product_sales:,.2f}."
        )

    # =====================================================
    # 4. MOST PROFITABLE PRODUCT
    # =====================================================

    product_profit = (
        df.groupby("Product Type")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    if not product_profit.empty:

        profitable_product = product_profit.index[0]
        profitable_value = product_profit.iloc[0]

        insights.append(
            f"{profitable_product} generated the highest "
            f"total profit of INR {profitable_value:,.2f}."
        )

    # =====================================================
    # 5. BEST MONTH
    # =====================================================

    if "Year-Month" in df.columns:

        monthly_sales = (
            df.groupby("Year-Month")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        if not monthly_sales.empty:

            best_month = monthly_sales.index[0]
            best_month_sales = monthly_sales.iloc[0]

            insights.append(
                f"{best_month} recorded the highest "
                f"monthly sales of "
                f"INR {best_month_sales:,.2f}."
            )

    # =====================================================
    # 6. AVERAGE ORDER VALUE
    # =====================================================

    total_sales = df["Sales"].sum()
    total_orders = len(df)

    if total_orders > 0:

        average_order_value = (
            total_sales / total_orders
        )

        insights.append(
            f"The average order value is "
            f"INR {average_order_value:,.2f}."
        )

    # =====================================================
    # 7. SHIPPING PERFORMANCE
    # =====================================================

    if "Shipping Days" in df.columns:

        average_shipping_days = (
            df["Shipping Days"].mean()
        )

        insights.append(
            f"Average shipping time is "
            f"{average_shipping_days:.1f} days."
        )

    # =====================================================
    # 8. PROFITABILITY CHECK
    # =====================================================

    total_profit = df["Profit"].sum()

    if total_profit > 0:

        insights.append(
            f"Overall business profitability is positive "
            f"with total profit of "
            f"INR {total_profit:,.2f}."
        )

    elif total_profit < 0:

        insights.append(
            f"Overall profit is negative at "
            f"INR {total_profit:,.2f}. "
            f"Further profitability analysis is recommended."
        )

    else:

        insights.append(
            "Overall profit is approximately zero."
        )

    return insights