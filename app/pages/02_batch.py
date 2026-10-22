import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] # Path(__file__).resolve() refers to the full path to app/pages/01_Predict.py, whereas .parents[0] refers to the "app/pages" folder, .parents[1] refers to the "app" folder, and .parents[2] refers to the "01_ChurnSense" project root.
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

from theme import apply_theme
apply_theme()


st.title("📂 Batch Churn Prediction")
st.write(
    "Upload a CSV Containing Customer Features to Predict Churn "
    "for Multiple Customers at Once."
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def is_churn_label(label):
    return str(label).strip().lower() in {"1", "yes", "true"}


try:
    model = load_model()

    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"],
        help=(
            "The CSV Should Contain the Same Feature Columns used to Train "
            "the Model. A customerID Column and an Existing Churn Column "
            "are Optional."
        ),
    )

    if uploaded_file is not None:
        try:
            customers = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Could Not Read the Uploaded CSV: {e}")
            st.stop()

        st.subheader("Uploaded Data")
        st.write(f"Rows: {len(customers):,} | Columns: {len(customers.columns)}")
        st.dataframe(customers.head(10), use_container_width=True)

        if customers.empty:
            st.warning("The Uploaded CSV Contains no Customer Records.")
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
                "The Uploaded CSV is Missing Required Feature Columns: "
                + ", ".join(missing_columns)
            )
            st.info(
                "Use a CSV with the Same Feature Names and Spelling as the "
                "Data used to Train the Model."
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
        "Model File not Found. Ensure "
        "'models/churn_model_v1.pkl' Exists in the Project Root."
    )
except Exception as e:
    st.error(f"Batch Prediction Failed: {e}")