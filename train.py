import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from src.data_loader import load_dataset, detect_target
from src.preprocessing import build_preprocessor
from src.feature_selection import select_features
from src.model_training import train_models
from src.evaluate import evaluate_models

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Bank Customer Churn Prediction.csv"

OUTPUT_DIR = BASE_DIR / "outputs"
MODEL_DIR = BASE_DIR / "models"

OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)


def print_top_features(model, feature_names, top_n=15):

    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
    elif hasattr(model, "coef_"):
        importance = np.abs(model.coef_[0])
    else:
        print("Model does not support feature importance")
        return None

    feature_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importance
    })

    feature_df = feature_df.sort_values(
        by="Importance",
        ascending=False
    )
    
    # get top 5 feature names
    top_features = feature_df["Feature"].tolist()
    print("\nTop Important Features\n",top_features)

    feature_df.to_csv(OUTPUT_DIR / "feature_importance.csv", index=False)
    joblib.dump(top_features, MODEL_DIR / "selected_features.pkl")
    return top_features


def main():

    print("Loading dataset...")
    print("Dataset path:", DATA_PATH)
    df = load_dataset(DATA_PATH)

    print("Dataset shape:", df.shape)
    target_col = detect_target(df)

    print("Detected target column:", target_col)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    print("\nBuilding preprocessing pipeline...")
    preprocessor = build_preprocessor(X)

    print("Applying preprocessing...")
    X_processed = preprocessor.fit_transform(X)
    feature_names = preprocessor.get_feature_names_out()
    
    print("\nRunning feature selection...")
    X_selected,selector = select_features(X_processed, y)
    selected_indices = selector.get_support(indices=True)
    selected_features = feature_names[selected_indices]
    
    print("\nTraining models...")
    models, X_train, X_test, y_train, y_test = train_models(X_selected, y)

    print("\nEvaluating models...")
    results_df, best_model = evaluate_models(models, X_test,y_test)

    print("\nModel Performance:")
    print(results_df)

    results_df.to_csv(OUTPUT_DIR / "model_performance.csv", index=False)
    print("\nBest Model:",best_model)
    print("\nSaving best model...")
    joblib.dump(best_model, MODEL_DIR / "best_model.pkl")
    joblib.dump(preprocessor, MODEL_DIR / "preprocessor.pkl")

    print("\nGenerating predictions...")
    preds = best_model.predict(X_selected)
    pred_df = df.copy()
    pred_df["prediction"] = preds
    pred_df.to_excel(OUTPUT_DIR / "predictions.xlsx", index=False)
    print("\nExtracting feature importance...")
    print_top_features(best_model, selected_features)
    print("\nTraining pipeline completed successfully!")


if __name__ == "__main__":
    main()