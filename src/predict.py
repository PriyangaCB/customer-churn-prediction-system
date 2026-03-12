import pandas as pd
import joblib

# Load the best model and preprocessed data
model = joblib.load("models/best_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")

# Predict the data by the best model, add the predicted column and save it in a excel file 
def predict_file(file_path):

    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    X = preprocessor.transform(df)

    preds = model.predict(X)
    probs = model.predict_proba(X)[:,1]

    df["prediction"] = preds
    df["probability"] = probs

    output="predictions.xlsx"

    df.to_excel(output,index=False)

    return output