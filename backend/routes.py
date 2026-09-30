from flask import Blueprint, jsonify, request
import joblib
import pandas as pd
import os


api = Blueprint("api", __name__)


# -----------------------------------------
# LOAD TRAINED MODEL
# -----------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml",
    "sales_model.pkl"
)

model = joblib.load(MODEL_PATH)


# -----------------------------------------
# HEALTH CHECK
# -----------------------------------------

@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "SalesIQ Flask API is running!"
    })


# -----------------------------------------
# SALES PREDICTION API
# -----------------------------------------

@api.route("/predict", methods=["POST"])
def predict_sales():

    try:
        data = request.get_json()

        # Create DataFrame from received data
        input_data = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(input_data)

        predicted_sales = float(prediction[0])

        return jsonify({
            "status": "success",
            "predicted_sales": round(predicted_sales, 2)
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400