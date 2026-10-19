
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"

FEATURE_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]


st.set_page_config(
    page_title="Batch Prediction | ChurnSense",
    page_icon="📂",
    layout="wide",
)

st.title("📂 Batch Churn Prediction")
st.write(
    "Upload a CSV containing customer features to predict churn "
    "for multiple customers at once."
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def is_churn_label(label):
    return str(label).strip().lower() in {"1", "yes", "true"}


try:
    model = load_model()

    uploaded_file = st.file_uploader(
        "Upload customer CSV",
        type=["csv"],
        help=(
            "The CSV should contain the same feature columns used to train "
            "the model. A customerID column and an existing Churn column "
            "are optional."
        ),
    )

    if uploaded_file is not None:
        try:
            customers = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Could not read the uploaded CSV: {e}")
            st.stop()

        st.subheader("Uploaded Data")
        st.write(f"Rows: {len(customers):,} | Columns: {len(customers.columns)}")
        st.dataframe(customers.head(10), use_container_width=True)

        if customers.empty:
            st.warning("The uploaded CSV contains no customer records.")
            st.stop()

        # Remove identifiers and an existing target column, if present.
        drop_columns = [
            col for col in customers.columns
            if col.strip().lower() in {"customerid", "churn"}
        ]
        customers = customers.drop(columns=drop_columns, errors="ignore")

        # Use model feature names when the fitted model exposes them.
        expected = getattr(model, "feature_names_in_", None)
        expected_columns = (
            list(expected) if expected is not None else FEATURE_COLUMNS
        )

        missing_columns = [
            col for col in expected_columns
            if col not in customers.columns
        ]

        if missing_columns:
            st.error(
                "The uploaded CSV is missing required feature columns: "
                + ", ".join(missing_columns)
            )
            st.info(
                "Use a CSV with the same feature names and spelling as the "
                "data used to train the model."
            )
            st.stop()

        # Extra columns are excluded; keep the training feature order.
        X = customers[expected_columns].copy()

        if st.button("Predict All Customers", type="primary"):
            predictions = model.predict(X)

            results = X.copy()
            results["Predicted_Churn"] = predictions
            results["Predicted_Churn_Status"] = [
                "Yes" if is_churn_label(value) else "No"
                for value in predictions
            ]

            if hasattr(model, "predict_proba"):
                classes = list(model.classes_)
                churn_indices = [
                    i for i, label in enumerate(classes)
                    if is_churn_label(label)
                ]

                if churn_indices:
                    probabilities = model.predict_proba(X)
                    results["Churn_Probability"] = (
                        probabilities[:, churn_indices[0]]
                    )
                    results["Churn_Probability_Percent"] = (
                        results["Churn_Probability"] * 100
                    ).round(2)

            st.subheader("Prediction Results")
            st.dataframe(results, use_container_width=True)

            predicted_churn = sum(
                is_churn_label(value) for value in predictions
            )
            total_customers = len(predictions)
            churn_rate = (
                predicted_churn / total_customers * 100
                if total_customers else 0
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Customers Processed", total_customers)
            col2.metric("Predicted to Churn", predicted_churn)
            col3.metric("Predicted Churn Rate", f"{churn_rate:.2f}%")

            csv_data = results.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Predictions as CSV",
                data=csv_data,
                file_name="churn_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )

except FileNotFoundError:
    st.error(
        "Model file not found. Ensure "
        "'models/churn_model_v1.pkl' exists in the project root."
    )
except Exception as e:
    st.error(f"Batch prediction failed: {e}")
