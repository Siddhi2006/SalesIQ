import streamlit as st
import pandas as pd
import os
import requests


def show_prediction():

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

    df = pd.read_excel(data_path)


    # =========================================================
    # PAGE TITLE
    # =========================================================

    st.title("Sales Prediction")

    st.write(
        "Enter the order details below to estimate "
        "the expected sales value using Machine Learning."
    )

    st.divider()


    # =========================================================
    # ORDER INFORMATION
    # =========================================================

    st.header("Order Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        order_date = st.date_input(
            "Order Date"
        )

        order_priority = st.selectbox(
            "Order Priority",
            sorted(
                df["Order Priority"].unique()
            )
        )


    with col2:

        freight_mode = st.selectbox(
            "Freight Mode",
            sorted(
                df["Freight Mode"].unique()
            )
        )

        segment = st.selectbox(
            "Segment",
            sorted(
                df["Segment"].unique()
            )
        )


    with col3:

        qty_ordered = st.number_input(
            "Quantity Ordered",
            min_value=1,
            value=5,
            step=1
        )

        discount_percentage = st.number_input(
            "Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            help=(
                "Enter discount as a percentage. "
                "Example: 6 means 6%."
            )
        )


    # =========================================================
    # PRODUCT INFORMATION
    # =========================================================

    st.divider()

    st.header("Product Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        product_type = st.selectbox(
            "Product Type",
            sorted(
                df["Product Type"].unique()
            )
        )


    with col2:

        product_sub_category = st.selectbox(
            "Product Sub-Category",
            sorted(
                df["Product Sub-Category"].unique()
            )
        )


    with col3:

        product_container = st.selectbox(
            "Product Container",
            sorted(
                df["Product Container"].unique()
            )
        )


    # =========================================================
    # LOCATION INFORMATION
    # =========================================================

    st.divider()

    st.header("Location Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        state = st.selectbox(
            "State",
            sorted(
                df["State"].unique()
            )
        )


    with col2:

        cities_for_state = sorted(
            df[
                df["State"] == state
            ]["City"].unique()
        )

        city = st.selectbox(
            "City",
            cities_for_state
        )


    with col3:

        region = st.selectbox(
            "Region",
            sorted(
                df["Region"].unique()
            )
        )


    # =========================================================
    # PRICING AND FREIGHT
    # =========================================================

    st.divider()

    st.header("Pricing and Freight")

    col1, col2, col3 = st.columns(3)

    with col1:

        unit_price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=50.0,
            step=1.0
        )


    with col2:

        freight_expenses = st.number_input(
            "Freight Expenses",
            min_value=0.0,
            value=5.0,
            step=0.5
        )


    with col3:

        st.info(
            f"Discount entered: "
            f"{discount_percentage:.1f}%"
        )


    # =========================================================
    # CALCULATE DATE FEATURES
    # =========================================================

    date_value = pd.Timestamp(
        order_date
    )

    order_year = date_value.year
    order_month = date_value.month
    order_quarter = date_value.quarter
    order_day = date_value.day
    order_day_of_week = date_value.dayofweek


    # =========================================================
    # SHOW CALCULATED DATE FEATURES
    # =========================================================

    st.divider()

    st.header("Calculated Date Features")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Year",
            order_year
        )


    with col2:

        st.metric(
            "Month",
            order_month
        )


    with col3:

        st.metric(
            "Quarter",
            order_quarter
        )


    with col4:

        st.metric(
            "Day",
            order_day
        )


    with col5:

        st.metric(
            "Day of Week",
            order_day_of_week
        )


    # =========================================================
    # MACHINE LEARNING PREDICTION
    # =========================================================

    st.divider()

    st.header("Machine Learning Prediction")

    if st.button(
        "Predict Sales",
        use_container_width=True
    ):

        # -----------------------------------------------------
        # PREPARE INPUT DATA
        # -----------------------------------------------------

        prediction_data = {

            "Discount offered":
                discount_percentage / 100,

            "Unit Price":
                unit_price,

            "Freight Expenses":
                freight_expenses,

            "QtyOrdered":
                qty_ordered,

            "Order Year":
                order_year,

            "Order Month":
                order_month,

            "Order Quarter":
                order_quarter,

            "Order Day":
                order_day,

            "Order DayOfWeek":
                order_day_of_week,

            "Order Priority":
                order_priority,

            "Freight Mode":
                freight_mode,

            "Segment":
                segment,

            "Product Type":
                product_type,

            "Product Sub-Category":
                product_sub_category,

            "Product Container":
                product_container,

            "State":
                state,

            "City":
                city,

            "Region":
                region
        }


        # -----------------------------------------------------
        # SEND DATA TO FLASK API
        # -----------------------------------------------------

        api_url = (
            "http://127.0.0.1:5000/api/predict"
        )


        try:

            response = requests.post(
                api_url,
                json=prediction_data,
                timeout=10
            )


            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            if response.status_code == 200:

                result = response.json()

                predicted_sales = result.get(
                    "predicted_sales"
                )


                if predicted_sales is not None:

                    st.divider()

                    st.success(
                        "Sales prediction generated successfully!"
                    )


                    # -----------------------------------------
                    # DISPLAY RESULT
                    # -----------------------------------------

                    st.subheader(
                        "Predicted Sales"
                    )

                    result_col1, result_col2, result_col3 = (
                        st.columns(3)
                    )

                    with result_col2:

                        st.metric(
                            label="Expected Sales",
                            value=(
                                f"₹ {predicted_sales:,.2f}"
                            )
                        )


                    # -----------------------------------------
                    # SHOW INPUT SUMMARY
                    # -----------------------------------------

                    with st.expander(
                        "View Prediction Input"
                    ):

                        st.json(
                            prediction_data
                        )


                else:

                    st.error(
                        "Prediction value was not returned "
                        "by the Flask API."
                    )


            # -------------------------------------------------
            # API ERROR
            # -------------------------------------------------

            else:

                try:

                    error_data = response.json()

                    error_message = error_data.get(
                        "message",
                        "Unknown API error"
                    )

                except ValueError:

                    error_message = response.text


                st.error(
                    f"Prediction failed: "
                    f"{error_message}"
                )


        # -----------------------------------------------------
        # FLASK CONNECTION ERROR
        # -----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to Flask backend."
            )

            st.info(
                "Please make sure app.py is running "
                "on port 5000."
            )


        # -----------------------------------------------------
        # REQUEST TIMEOUT
        # -----------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "Flask API request timed out. "
                "Please try again."
            )


        # -----------------------------------------------------
        # OTHER REQUEST ERROR
        # -----------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"API request failed: {str(e)}"
            )


    # =========================================================
    # FOOTER
    # =========================================================

    st.divider()

    st.caption(
        "SalesIQ | AI-Powered Sales Analytics & "
        "Decision Support Platform"
    )