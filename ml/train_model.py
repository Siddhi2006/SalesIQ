import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# -----------------------------------------
# STEP 1: LOAD DATASET
# -----------------------------------------

file_path = "../data/INDIA_RETAIL_DATA.xlsx"

df = pd.read_excel(file_path)

print("\n========== DATASET LOADED ==========")
print("Rows and Columns:", df.shape)


# -----------------------------------------
# STEP 2: FEATURE ENGINEERING
# -----------------------------------------

print("\n========== FEATURE ENGINEERING ==========")

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Order Quarter"] = df["Order Date"].dt.quarter
df["Order Day"] = df["Order Date"].dt.day
df["Order DayOfWeek"] = df["Order Date"].dt.dayofweek

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\nNew features created:")
print("- Order Year")
print("- Order Month")
print("- Order Quarter")
print("- Order Day")
print("- Order DayOfWeek")
print("- Shipping Days")


print("\n========== FEATURE EXAMPLES ==========")

print(
    df[
        [
            "Order Date",
            "Order Year",
            "Order Month",
            "Order Quarter",
            "Order Day",
            "Order DayOfWeek",
            "Ship Date",
            "Shipping Days"
        ]
    ].head()
)


print("\n========== UPDATED DATASET ==========")
print("Rows and Columns:", df.shape)

print("\nAll columns:")
print(df.columns.tolist())


# -----------------------------------------
# STEP 3: SELECT FEATURES AND TARGET
# -----------------------------------------

print("\n========== FEATURE SELECTION ==========")

features = [
    # Numerical features
    "Discount offered",
    "Unit Price",
    "Freight Expenses",
    "QtyOrdered",
    "Order Year",
    "Order Month",
    "Order Quarter",
    "Order Day",
    "Order DayOfWeek",

    # Categorical features
    "Order Priority",
    "Freight Mode",
    "Segment",
    "Product Type",
    "Product Sub-Category",
    "Product Container",
    "State",
    "City",
    "Region"
]

# Input features
X = df[features]

# Target variable
y = df["Sales"]

print("\nInput features (X):")
print(X.columns.tolist())

print("\nTarget variable (y):")
print("Sales")

print("\nShape of X:", X.shape)
print("Shape of y:", y.shape)


# -----------------------------------------
# STEP 4: TRAIN-TEST SPLIT
# -----------------------------------------

print("\n========== TRAIN-TEST SPLIT ==========")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Total records:", len(X))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining feature shape:", X_train.shape)
print("Testing feature shape:", X_test.shape)

print("\nTraining target shape:", y_train.shape)
print("Testing target shape:", y_test.shape)


# -----------------------------------------
# STEP 5: DATA PREPROCESSING
# -----------------------------------------

print("\n========== DATA PREPROCESSING ==========")

# Numerical features
numerical_features = [
    "Discount offered",
    "Unit Price",
    "Freight Expenses",
    "QtyOrdered",
    "Order Year",
    "Order Month",
    "Order Quarter",
    "Order Day",
    "Order DayOfWeek"
]

# Categorical features
categorical_features = [
    "Order Priority",
    "Freight Mode",
    "Segment",
    "Product Type",
    "Product Sub-Category",
    "Product Container",
    "State",
    "City",
    "Region"
]


# -----------------------------------------
# NUMERICAL PREPROCESSING
# -----------------------------------------

numerical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)


# -----------------------------------------
# CATEGORICAL PREPROCESSING
# -----------------------------------------

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# -----------------------------------------
# COMBINE PREPROCESSING
# -----------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            numerical_pipeline,
            numerical_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


print("Numerical features:", len(numerical_features))
print("Categorical features:", len(categorical_features))

print("\nNumerical preprocessing:")
print("- Missing values → Median")

print("\nCategorical preprocessing:")
print("- Missing values → Most Frequent")
print("- Categories → One-Hot Encoding")

print("\nPreprocessing pipeline created successfully.")
# -----------------------------------------
# STEP 6: BUILD AND TRAIN ML MODEL
# -----------------------------------------

print("\n========== MODEL TRAINING ==========")

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

print("Model: Random Forest Regressor")
print("Number of trees:", 200)


# -----------------------------------------
# COMPLETE ML PIPELINE
# -----------------------------------------

model_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

print("\nComplete ML pipeline created:")
print("- Data preprocessing")
print("- One-Hot Encoding")
print("- Random Forest Regressor")


# -----------------------------------------
# TRAIN MODEL
# -----------------------------------------

print("\nTraining model...")

model_pipeline.fit(X_train, y_train)

print("Model training completed successfully!")

# -----------------------------------------
# STEP 7: MODEL EVALUATION
# -----------------------------------------

print("\n========== MODEL EVALUATION ==========")

# Make predictions on test data
y_pred = model_pipeline.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)

print("\nEvaluation Metrics:")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 4))


# -----------------------------------------
# SAMPLE PREDICTIONS
# -----------------------------------------

print("\n========== SAMPLE PREDICTIONS ==========")

results = pd.DataFrame({
    "Actual Sales": y_test.values,
    "Predicted Sales": y_pred
})

results["Difference"] = (
    results["Actual Sales"] -
    results["Predicted Sales"]
)

print(results.head(10))
# -----------------------------------------
# STEP 8: SAVE TRAINED MODEL
# -----------------------------------------

print("\n========== SAVING MODEL ==========")

model_path = "sales_model.pkl"

joblib.dump(
    model_pipeline,
    model_path
)

print("Model saved successfully!")
print("Model file:", model_path)