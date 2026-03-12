import pandas as pd
from pathlib import Path

# load dataset - Excel or CSV file
def load_dataset(path):
    path = Path(path)
    if path.suffix == ".xlsx":
        df = pd.read_excel(path)
    elif path.suffix == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")
    return df

# Auto-detects the target column
def detect_target(df):

    candidates = [
        "churn","target","label","y",
        "Exited","Attrition","default",
        "fraud","is_fraud"
    ]

    for col in candidates:
        if col in df.columns:
            return col

    return df.columns[-1]