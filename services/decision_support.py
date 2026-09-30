import requests


API_URL = "http://127.0.0.1:5000/api/predict"


def predict_sales(data):
    """
    Send sales input data to Flask API
    and return predicted sales.
    """

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            return float(
                result["predicted_sales"]
            )

        return None

    except requests.exceptions.RequestException:

        return None


def compare_scenarios(
    base_data,
    scenario_data
):
    """
    Compare baseline and scenario
    sales predictions.
    """

    base_prediction = predict_sales(
        base_data
    )

    scenario_prediction = predict_sales(
        scenario_data
    )


    if (
        base_prediction is None
        or scenario_prediction is None
    ):

        return None


    difference = (
        scenario_prediction -
        base_prediction
    )


    if base_prediction != 0:

        percentage_change = (
            difference /
            base_prediction
        ) * 100

    else:

        percentage_change = 0


    return {

        "base_prediction":
            base_prediction,

        "scenario_prediction":
            scenario_prediction,

        "difference":
            difference,

        "percentage_change":
            percentage_change
    }