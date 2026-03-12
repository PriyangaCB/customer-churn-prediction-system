import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score,roc_auc_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

# Train different models and compare the models to find the best model
def train_models(X,y):

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    models = {

        "LogisticRegression":LogisticRegression(max_iter=1000),

        "RandomForest":RandomForestClassifier(n_estimators=200),

        "GradientBoosting":GradientBoostingClassifier(),

        "XGBoost":XGBClassifier(eval_metric="logloss"),

        "LightGBM":LGBMClassifier()

    }

    trained_models = {}

    for name, model in models.items():
        print("Training:", name)
        model.fit(X, y)
        trained_models[name] = model

    return trained_models,X_train, X_test, y_train, y_test