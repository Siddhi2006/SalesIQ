from flask import Flask
from backend.routes import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def home():
    return {
        "message": "Welcome to SalesIQ",
        "status": "running"
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)