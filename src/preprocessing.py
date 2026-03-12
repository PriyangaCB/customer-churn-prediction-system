from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

# Identify the numerical and categorical data columns
def build_preprocessor(df):

    numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
    categorical_cols = df.select_dtypes(include=["object","category"]).columns
# Create pipeline for each 
    numeric_pipeline = Pipeline([
        ("imputer",SimpleImputer(strategy="median"))
    ])

    categorical_pipeline = Pipeline([
        ("imputer",SimpleImputer(strategy="most_frequent")),
        ("encoder",OneHotEncoder(handle_unknown="ignore"))
    ])
# ColumnTransformer for heterogeneous data 
    preprocessor = ColumnTransformer([
        ("num",numeric_pipeline,numeric_cols),
        ("cat",categorical_pipeline,categorical_cols)
    ])

    return preprocessor