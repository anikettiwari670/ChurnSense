import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"

st.set_page_config(
    page_title="Batch Prediction",
    page_icon="📂",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.title("📂 Batch Churn Prediction")

st.write(
    "Upload a CSV file containing customer features. "
    "The application will predict churn for each customer."
)

uploaded_file = st.file_uploader(
    "Upload customer CSV",
    type=["csv"]
)

try:
    model = load_model()

    if uploaded_file is not None:
        customers = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(customers.head())

        if "Churn" in customers.columns:
            customers = customers.drop(columns=["Churn"])

        if "customerID" in customers.columns:
            customers = customers.drop(columns=["customerID"])

        if st.button("Predict All Customers"):

            predictions = model.predict(customers)

            results = customers.copy()
            results["Predicted_Churn"] = predictions
            results["Predicted_Churn_Status"] = (
                results["Predicted_Churn"]
                .map({1: "Yes", 0: "No"})
            )

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(customers)
                classes = list(model.classes_)
                churn_index = classes.index(1)

                results["Churn_Probability"] = (
                    probabilities[:, churn_index]
                )

            st.subheader("Prediction Results")
            st.dataframe(results, use_container_width=True)

            st.metric(
                "Customers Predicted to Churn",
                int((predictions == 1).sum())
            )

            csv = results.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Predictions",
                data=csv,
                file_name="churn_predictions.csv",
                mime="text/csv"
            )

except FileNotFoundError:
    st.error(
        "Model file not found. Train and save the model first."
    )
except Exception as e:
    st.error(f"Batch prediction failed: {e}")