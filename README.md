# SalesIQ — AI-Powered Sales Analytics & Decision Support Platform

SalesIQ is an AI-powered sales analytics and decision-support platform that helps businesses analyze historical sales data, predict sales revenue, and discover meaningful business insights.

The platform combines **Machine Learning, Flask, Streamlit, and data analytics** to transform raw sales data into useful predictions and visual insights for better decision-making.

---

## 🚀 Features

* 📊 Sales data analysis and visualization
* 🤖 Machine Learning-based sales prediction
* 📈 Revenue forecasting using historical sales data
* 🔍 Identification of important sales patterns and factors
* 📋 Interactive analytics dashboard
* 🔌 Flask REST API for backend communication
* 🖥️ Streamlit-based user interface
* 🧹 Automated data preprocessing
* 📅 Date-based feature engineering
* 🌳 Random Forest Regression model

---

## 🏗️ Project Architecture

```text
                   ┌──────────────────────┐
                   │      SalesIQ UI      │
                   │      Streamlit       │
                   └──────────┬───────────┘
                              │
                              │ HTTP Requests
                              ▼
                   ┌──────────────────────┐
                   │    Flask Backend     │
                   │      REST API        │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Machine Learning     │
                   │     Pipeline         │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Random Forest        │
                   │     Regressor        │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Sales Prediction &   │
                   │ Business Insights    │
                   └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* Flask
* REST API

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Random Forest Regression

### Data Processing

* Pandas
* One-Hot Encoding
* Median / Most-Frequent Imputation
* Feature Engineering

### Development Tools

* PyCharm
* Git
* GitHub

---

## 📂 Project Structure

```text
SalesIQ/
│
├── backend/
│   └── ...
│
├── ml/
│   └── train_model.py
│
├── data/
│   └── README.md
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

> The exact structure may vary as the project continues to evolve.

---

## 📊 Dataset

SalesIQ uses a retail sales dataset containing information related to orders, products, customers, locations, shipping, quantity, discounts, profit, and sales.

The dataset contains **2,534 records and 18 original features**.

Important attributes include:

* Order Priority
* Discount Offered
* Unit Price
* Freight Expenses
* Freight Mode
* Segment
* Product Type
* Product Sub-Category
* Product Container
* State
* City
* Region
* Country
* Order Date
* Ship Date
* Profit
* Qty Ordered
* Sales

---

## 🔄 Data Preprocessing

Before training the Machine Learning model, the raw dataset is processed to make it suitable for prediction.

### 1. Date Feature Engineering

The `Order Date` and `Ship Date` fields are processed to create additional useful features:

```text
Order Year
Order Month
Order Quarter
Order Day
Order DayOfWeek
Shipping Days
```

These features help the model identify seasonal and time-related sales patterns.

### 2. Feature Selection

The selected input features include numerical and categorical variables such as:

```text
Discount offered
Unit Price
Freight Expenses
Qty Ordered
Order Year
Order Month
Order Quarter
Order Day
Order DayOfWeek
Order Priority
Freight Mode
Segment
Product Type
Product Sub-Category
Product Container
State
City
Region
```

The target variable is:

```text
Sales
```

---

## ⚙️ Machine Learning Pipeline

SalesIQ uses a supervised Machine Learning approach.

The overall pipeline is:

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Feature Selection
     ↓
Train-Test Split
     ↓
Data Preprocessing
     ↓
Random Forest Regression
     ↓
Model Evaluation
     ↓
Sales Prediction
```

### Preprocessing

Numerical features are handled using:

```text
Median Imputation
```

Categorical features are handled using:

```text
Most-Frequent Imputation
One-Hot Encoding
```

A preprocessing pipeline is used so that the same transformations are consistently applied during training and prediction.

---

## 🌳 Machine Learning Model

SalesIQ uses a:

**Random Forest Regressor**

with:

```text
Number of Trees = 200
```

Random Forest was selected because it can handle both nonlinear relationships and a mixture of numerical and categorical-derived features effectively.

---

## 📈 Model Performance

The dataset was divided into:

```text
Training Data: 2027 records
Testing Data:   507 records
```

The model achieved approximately:

| Metric   | Result |
| -------- | -----: |
| MAE      | 209.61 |
| RMSE     | 937.02 |
| R² Score | 0.8221 |

The R² score indicates that the trained model explains a substantial portion of the variation in the test-set sales values.

---

## 🔌 Flask Backend

SalesIQ uses Flask to provide backend functionality through REST APIs.

The Flask backend acts as a bridge between the Streamlit interface and the Machine Learning prediction functionality.

Example flow:

```text
User Input
    ↓
Streamlit
    ↓
Flask REST API
    ↓
Preprocessing
    ↓
Trained ML Model
    ↓
Prediction
    ↓
Flask Response
    ↓
Streamlit Dashboard
```

---

## 🖥️ Streamlit Interface

The Streamlit application provides an interactive interface for users to work with the SalesIQ platform.

The application is designed around:

* Sales analytics
* Prediction
* Business insights
* Data visualization
* Decision support

The application can be accessed locally through:

```text
http://localhost:8501
```

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Siddhi2006/SalesIQ.git
```

### 2. Navigate to the Project

```bash
cd SalesIQ
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Train the Machine Learning Model

```bash
python ml/train_model.py
```

### 7. Start the Flask Backend

Run the Flask application according to the backend entry point configured in the project.

### 8. Start Streamlit

```bash
streamlit run app.py
```

The application will then be available at:

```text
http://localhost:8501
```

---

## 🎯 Objective

The primary objective of SalesIQ is to demonstrate how Machine Learning and web technologies can be combined to create a practical sales decision-support system.

Instead of relying only on raw sales reports, the platform processes historical data and provides predictive and analytical information that can assist users in understanding sales patterns and making data-driven decisions.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Real-time sales data integration
* Database integration for persistent storage
* Advanced sales forecasting models
* Customer segmentation
* Product-level demand prediction
* Automated business recommendations
* Role-based authentication
* Cloud deployment
* Interactive KPI dashboards
* Comparison of multiple Machine Learning models

---

## 👩‍💻 Author

**Siddhi Shendurkar**

B.Tech — Electronics and Telecommunication Engineering

Interested in:

* Java Backend Development
* Python
* Machine Learning
* Full-Stack Development
* Data Analytics

---

## 📌 Project Status

**Active Development**

SalesIQ is being developed as a practical Machine Learning and web-development project focused on sales analytics, prediction, and decision support.
