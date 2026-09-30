import streamlit as st
import pandas as pd
import os
import sys


def show_decision_support():

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


    # =========================================================
    # IMPORT DECISION SUPPORT SERVICE
    # =========================================================

    from services.decision_support import (
        compare_scenarios
    )


    # =========================================================
    # LOAD DATASET
    # =========================================================

    data_path = os.path.join(
        base_dir,
        "data",
        "INDIA_RETAIL_DATA.xlsx"
    )

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
    # PAGE TITLE
    # =========================================================

    st.title(
        "Decision Support"
    )

    st.write(
        "Compare a current sales scenario with a "
        "proposed what-if scenario and evaluate "
        "the expected change in sales."
    )

    st.divider()


    # =========================================================
    # ORDER DETAILS
    # =========================================================

    st.header(
        "Order Details"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        order_priority = st.selectbox(
            "Order Priority",
            sorted(
                df["Order Priority"].dropna().unique()
            )
        )


    with col2:

        freight_mode = st.selectbox(
            "Freight Mode",
            sorted(
                df["Freight Mode"].dropna().unique()
            )
        )


    with col3:

        segment = st.selectbox(
            "Segment",
            sorted(
                df["Segment"].dropna().unique()
            )
        )


    # =========================================================
    # PRODUCT DETAILS
    # =========================================================

    st.divider()

    st.header(
        "Product Details"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        product_type = st.selectbox(
            "Product Type",
            sorted(
                df["Product Type"].dropna().unique()
            )
        )


    with col2:

        product_sub_category = st.selectbox(
            "Product Sub-Category",
            sorted(
                df["Product Sub-Category"]
                .dropna()
                .unique()
            )
        )


    with col3:

        product_container = st.selectbox(
            "Product Container",
            sorted(
                df["Product Container"]
                .dropna()
                .unique()
            )
        )


    # =========================================================
    # LOCATION DETAILS
    # =========================================================

    st.divider()

    st.header(
        "Location Details"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        state = st.selectbox(
            "State",
            sorted(
                df["State"].dropna().unique()
            )
        )


    with col2:

        city_list = sorted(
            df[
                df["State"] == state
            ]["City"]
            .dropna()
            .unique()
        )

        city = st.selectbox(
            "City",
            city_list
        )


    with col3:

        region = st.selectbox(
            "Region",
            sorted(
                df["Region"].dropna().unique()
            )
        )


    # =========================================================
    # BASELINE SCENARIO
    # =========================================================

    st.divider()

    st.header(
        "Baseline Scenario"
    )

    st.write(
        "Enter the current order conditions."
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        base_quantity = st.number_input(
            "Current Quantity",
            min_value=1,
            value=5,
            step=1
        )


    with col2:

        base_discount = st.number_input(
            "Current Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5
        )


    with col3:

        base_unit_price = st.number_input(
            "Current Unit Price",
            min_value=0.0,
            value=50.0,
            step=1.0
        )


    with col4:

        base_freight = st.number_input(
            "Current Freight Expenses",
            min_value=0.0,
            value=5.0,
            step=0.5
        )


    # =========================================================
    # WHAT-IF SCENARIO
    # =========================================================

    st.divider()

    st.header(
        "What-If Scenario"
    )

    st.write(
        "Change one or more values to simulate "
        "a different business scenario."
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        scenario_quantity = st.number_input(
            "Scenario Quantity",
            min_value=1,
            value=10,
            step=1
        )


    with col2:

        scenario_discount = st.number_input(
            "Scenario Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5
        )


    with col3:

        scenario_unit_price = st.number_input(
            "Scenario Unit Price",
            min_value=0.0,
            value=50.0,
            step=1.0
        )


    with col4:

        scenario_freight = st.number_input(
            "Scenario Freight Expenses",
            min_value=0.0,
            value=5.0,
            step=0.5
        )


    # =========================================================
    # BUILD BASELINE INPUT
    # =========================================================

    base_data = {

        "Discount offered":
            base_discount / 100,

        "Unit Price":
            base_unit_price,

        "Freight Expenses":
            base_freight,

        "QtyOrdered":
            base_quantity,

        "Order Year":
            2013,

        "Order Month":
            6,

        "Order Quarter":
            2,

        "Order Day":
            15,

        "Order DayOfWeek":
            5,

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


    # =========================================================
    # BUILD SCENARIO INPUT
    # =========================================================

    scenario_data = {

        "Discount offered":
            scenario_discount / 100,

        "Unit Price":
            scenario_unit_price,

        "Freight Expenses":
            scenario_freight,

        "QtyOrdered":
            scenario_quantity,

        "Order Year":
            2013,

        "Order Month":
            6,

        "Order Quarter":
            2,

        "Order Day":
            15,

        "Order DayOfWeek":
            5,

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


    # =========================================================
    # COMPARE SCENARIOS
    # =========================================================

    st.divider()

    if st.button(
        "Compare Scenarios",
        use_container_width=True
    ):

        with st.spinner(
            "Calculating sales predictions..."
        ):

            result = compare_scenarios(
                base_data,
                scenario_data
            )


        # -----------------------------------------------------
        # HANDLE ERROR
        # -----------------------------------------------------

        if result is None:

            st.error(
                "Unable to calculate scenario comparison."
            )

            st.info(
                "Please make sure the Flask backend "
                "is running on port 5000."
            )

            return


        # -----------------------------------------------------
        # EXTRACT RESULTS
        # -----------------------------------------------------

        base_prediction = result[
            "base_prediction"
        ]

        scenario_prediction = result[
            "scenario_prediction"
        ]

        difference = result[
            "difference"
        ]

        percentage_change = result[
            "percentage_change"
        ]


        # =====================================================
        # DISPLAY RESULTS
        # =====================================================

        st.success(
            "Scenario comparison completed successfully."
        )

        st.divider()

        st.header(
            "Scenario Comparison"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current Predicted Sales",
                f"INR {base_prediction:,.2f}"
            )


        with col2:

            st.metric(
                "Scenario Predicted Sales",
                f"INR {scenario_prediction:,.2f}"
            )


        with col3:

            st.metric(
                "Expected Change",
                f"INR {difference:,.2f}",
                delta=f"{percentage_change:.2f}%"
            )


        # =====================================================
        # DECISION MESSAGE
        # =====================================================

        st.divider()

        st.header(
            "Decision Recommendation"
        )


        if difference > 0:

            st.success(
                f"The proposed scenario is expected "
                f"to increase predicted sales by "
                f"INR {difference:,.2f}, representing "
                f"an estimated change of "
                f"{percentage_change:.2f}%."
            )

        elif difference < 0:

            st.warning(
                f"The proposed scenario is expected "
                f"to decrease predicted sales by "
                f"INR {abs(difference):,.2f}, representing "
                f"an estimated change of "
                f"{abs(percentage_change):.2f}%."
            )

        else:

            st.info(
                "The proposed scenario is not expected "
                "to change the predicted sales."
            )


        # =====================================================
        # INPUT DETAILS
        # =====================================================

        with st.expander(
            "View Scenario Inputs"
        ):

            input_col1, input_col2 = st.columns(2)


            with input_col1:

                st.subheader(
                    "Baseline Input"
                )

                st.json(
                    base_data
                )


            with input_col2:

                st.subheader(
                    "Scenario Input"
                )

                st.json(
                    scenario_data
                )


    # =========================================================
    # FOOTER
    # =========================================================

    st.divider()

    st.caption(
        "SalesIQ | AI-Powered Sales Analytics and "
        "Decision Support Platform"
    )