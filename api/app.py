from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from pathlib import Path
from pydantic import create_model
from utils.column_mapper import auto_match_columns, align_missing_columns

app = FastAPI(title="Customer Churn Prediction API")


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"
FEATURES_PATH = BASE_DIR / "models" / "selected_features.pkl"

# Load model and preprocessor
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
features = joblib.load(FEATURES_PATH)

# Dynamic Manual Input Schema
ManualInput = create_model(
    "ManualInput",
    **{feature: (float, 0) for feature in features}
)

# Preprocessing Pipeline
def preprocess_input(df):

    # Step 1 auto match columns
    df = auto_match_columns(df, features)

    # Step 2 align missing columns
    df = align_missing_columns(df, features)

    return df

# Home Endpoint
@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}

# 1. Excel / CSV Upload Prediction
@app.post("/predict_excel")
async def predict_excel(file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    X_processed = preprocess_input(df)

    predictions = model.predict(X_processed)
    probabilities = model.predict_proba(X_processed)[:,1]

    df["prediction"] = predictions
    df["churn_probability"] = probabilities

    return df.to_dict(orient="records")


# 2. Manual Input Prediction
@app.post("/predict_manual")
def predict_manual(input_data: ManualInput):

    # Convert input to dataframe
    df = pd.DataFrame([input_data.dict()])

    # Preprocess
    X_processed = preprocess_input(df)

    # Predict
    prediction = model.predict(X_processed)[0]
    probability = model.predict_proba(X_processed)[0][1]

    return {
        "prediction": int(prediction),
        "churn_probability": float(probability),
        "result": "Customer will churn" if prediction == 1 else "Customer will stay"
    }