import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from io import BytesIO
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict_excel")

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("Customer Churn Prediction Dashboard")

st.write("Upload a CSV or Excel file to predict churn and visualize results.")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # Detect file type
    file_type = uploaded_file.name.split(".")[-1]

    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    st.info("Sending file to prediction API...")

    response = requests.post(API_URL, files=files)

    if response.status_code != 200:
        st.error("Prediction API error")
        st.stop()

    data = response.json()

    df = pd.DataFrame(data)

    st.success("Prediction completed")

    st.subheader("Predicted Dataset")

    st.dataframe(df)

    # KPI Metrics

    total_customers = len(df)

    churn_count = df["prediction"].sum()

    churn_rate = churn_count / total_customers

    avg_prob = df["churn_probability"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)

    col2.metric("Predicted Churn", churn_count)

    col3.metric("Churn Rate", f"{churn_rate:.2%}")

    col4.metric("Avg Churn Probability", f"{avg_prob:.2f}")

    # Charts

    st.subheader("Churn Distribution")

    fig1 = px.pie(
        df,
        names="prediction",
        title="Churn vs Retained Customers"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Churn Probability Distribution")

    fig2 = px.histogram(
        df,
        x="churn_probability",
        nbins=20,
        title="Probability Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # High Risk Customers

    st.subheader("Top 25 High Risk Customers")

    high_risk = (df.sort_values(by="churn_probability", ascending=False).head(25).reset_index(drop=True))

    # make index start from 1
    high_risk.index = high_risk.index + 1
    high_risk.index.name = "Rank"
    st.dataframe(high_risk[["customer_id", "churn_probability", "prediction"]])

    # Download Prediction File

    st.subheader("Download Predicted Dataset")

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="Download Excel File",
        data=output.getvalue(),
        file_name="churn_predictions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )