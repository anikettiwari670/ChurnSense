from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Batch Prediction | ChurnSense",
    page_icon="📂",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "churn_model_v1.pkl"

FEATURES = [
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

NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
]


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


st.title("📂 Batch Customer Churn Prediction")
st.write(
    "Upload a CSV file to predict churn for multiple customers "
    "and download the results."
)

if not MODEL_PATH.exists():
    st.error(f"Model file not found: {MODEL_PATH}")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload customer data (CSV)",
    type=["csv"],
)

st.info(
    "Your CSV must contain all 19 model features. "
    "A customerID column is optional and will be retained in the results."
)

with st.expander("View required columns"):
    st.code(", ".join(FEATURES))

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()

    if data.empty:
        st.warning("The uploaded CSV contains no customer rows.")
        st.stop()

    st.subheader("1. Preview uploaded data")
    st.write(f"Rows: **{len(data):,}** | Columns: **{len(data.columns)}**")
    st.dataframe(data.head(10), use_container_width=True)

    missing = [column for column in FEATURES if column not in data.columns]

    if missing:
        st.error("The CSV is missing these required columns:")
        st.write(missing)
        st.stop()

    if len(data) > 100_000:
        st.error(
            "This file contains more than 100,000 rows. "
            "Please upload a smaller file."
        )
        st.stop()

    
    if st.button("🚀 Predict churn", type="primary"):
        try:
            model = load_model()

            # Select the required model features
            model_input = data[FEATURES].copy()

            # Convert numerical columns to numeric values
            for column in NUMERIC_FEATURES:
                model_input[column] = pd.to_numeric(
                    model_input[column], errors="coerce"
                )

            # Generate predictions
            predictions = model.predict(model_input)

            results = data.copy()
            results["Predicted_Churn"] = predictions

            results["Predicted_Churn_Status"] = (
                results["Predicted_Churn"]
                .map({1: "Yes", 0: "No", "Yes": "Yes", "No": "No"})
            )

            # Calculate churn probabilities
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(model_input)
                classes = list(model.classes_)

                if 1 in classes:
                    churn_index = classes.index(1)
                elif "Yes" in classes:
                    churn_index = classes.index("Yes")
                else:
                    churn_index = None

                if churn_index is not None:
                    results["Churn_Probability"] = (
                        probabilities[:, churn_index] * 100
                    ).round(2)

            # Save results across Streamlit reruns
            st.session_state["churnsense_batch_results"] = results

        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
            st.stop()


results = st.session_state.get("churnsense_batch_results")

if results is not None:
    st.divider()
    st.subheader("2. Prediction summary")

    total = len(results)
    predicted_yes = results["Predicted_Churn_Status"].eq("Yes").sum()
    predicted_no = results["Predicted_Churn_Status"].eq("No").sum()
    churn_rate = predicted_yes / total * 100 if total else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers analyzed", f"{total:,}")
    col2.metric("Predicted churners", f"{predicted_yes:,}")
    col3.metric("Predicted non-churners", f"{predicted_no:,}")
    col4.metric("Predicted churn rate", f"{churn_rate:.1f}%")

    st.subheader("3. Customer-level predictions")
    st.dataframe(results, use_container_width=True)

    csv_bytes = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download predictions as CSV",
        data=csv_bytes,
        file_name="churnsense_batch_predictions.csv",
        mime="text/csv",
    )

    st.caption(
        "Predictions are model estimates, not confirmed future outcomes. "
        "The predicted churn rate is not necessarily the actual churn rate."
    )