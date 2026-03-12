import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def evaluate_models(models, X, y):

    results = []

    best_f1 = 0
    best_model = None

    for name, model in models.items():
        preds = model.predict(X)

        acc = accuracy_score(y, preds)
        precision = precision_score(y, preds, zero_division=0)
        recall = recall_score(y, preds, zero_division=0)
        f1 = f1_score(y, preds, zero_division=0)

        results.append({
            "Model": name,
            "Accuracy": round(acc, 3),
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1 Score": round(f1, 3)
        })

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

    results_df = pd.DataFrame(results)

    return results_df, best_model