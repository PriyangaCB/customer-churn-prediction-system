# Customer Churn Prediction System

A complete end-to-end Machine Learning system that predicts customer churn using automated data preprocessing, model comparison, and feature selection.

The system accepts **CSV or Excel datasets with flexible column names**, automatically preprocesses the data, compares multiple machine learning models, selects the best performing model, and uses the most important features for churn prediction.

---

## Project Overview

Customer churn prediction helps businesses identify customers who are likely to leave their service. By predicting churn in advance, companies can take proactive actions to retain customers.

This project builds a robust churn prediction pipeline that:

* Accepts datasets in CSV or Excel format
* Automatically matches column names
* Handles missing values
* Performs data preprocessing
* Trains multiple ML models
* Selects the best performing model
* Extracts top important features
* Provides prediction APIs
* Supports containerized deployment with Docker

---

## Key Features

* Automatic dataset ingestion (CSV / Excel)
* Intelligent column matching for flexible datasets
* Automatic missing column handling
* Data preprocessing pipeline
* Multi-model training and evaluation
* Automatic best model selection
* Feature importance extraction
* REST API for predictions      
* Dockerized deployment

---

## Machine Learning Models Compared

The system trains and evaluates multiple models and selects the best one based on performance.

Models used include:

* Logistic Regression
* Random Forest Classifier
* Gradient Boosting Classifier
* XBoost
* LightGBM

The best model is automatically selected based on evaluation metrics.

The project uses the Python ML library:

* scikit-learn

---

## Project Workflow

```
Dataset (CSV / Excel)
        │
        ▼
Column Matching
        │
        ▼
Data Preprocessing
        │
        ▼
Train / Test Split
        │
        ▼
Model Training (5 Models)
        │
        ▼
Model Evaluation
        │
        ▼
Best Model Selection
        │
        ▼
Feature Importance Extraction
        │
        ▼
Top Feature Selection
        │
        ▼
Prediction API
```

---

## Project Structure

```
churn_prediction_system
│
├── api
│   └── app.py
|   └── __int__.py
├── data
│   ├── Excel data
│
├── outputs
│   ├── feature_importance.csv
│   └── model_performane.csv
|   └── predictions.xlsx
|
├── models
│   ├── best_model.pkl
│   └── selected_features.pkl
|   └── preprocessor.pkl
|
├── src
│   ├── data_loader.py
│   └── evaluate.py
|   └── feature_selection.py
|   └── model_training.py
|   └── predict.py
|   └── preprocessing.py
│
├── utils
│   ├── column_mapper.py
│
├── Dockerfile
├── train.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```
git clone https://github.com/PriyangaCB/churn-prediction-system.git
```

Navigate to the project directory

```
cd churn-prediction-system
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

## Training the Model

Run the training pipeline:

```
python train.py
```

This will:

* preprocess the dataset
* train five machine learning models
* evaluate their performance
* select the best model
* extract top features
* save the model and features

Saved files:

```
models/best_model.pkl
models/preprocessor.pkl
models/seleted_features.pkl
```

---

## Running the API

Start the API server

```
uvicorn api.app:app --reload
```

API will run at

```
http://127.0.0.1:8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

## Prediction Method
The system supports two prediction approaches.

### 1. File Upload Prediction

Upload a CSV or Excel file containing customer data.

The system will:

* automatically match column names
* preprocess the dataset
* align required features
* generate churn predictions

----
### 2. Manual Input Prediction

Users can send feature values directly to the API.

Example request:

{
  "credit_score": 650,
  "age": 45,
  "balance": 120000,
  "products_number": 2,
  "active_member": 1
}

The API returns the churn prediction.
---

### Docker Deployment

The application is containerized using Docker.

### Build Docker Image
docker build -t churn-prediction-api .
### Run Docker Container
docker run -p 8000:8000 churn-prediction-api

Access API documentation:
http://localhost:8000/docs

---
## Technologies Used

Python
pandas
numpy
scikit-learn
FastAPI
Uvicorn
Docker

---

## Future Improvements

* Add model explainability using SHAP
* Add dashboard for churn visualization
* Deploy API to cloud platforms
* Build a web interface for predictions

---

## Author

Priyanga

---
