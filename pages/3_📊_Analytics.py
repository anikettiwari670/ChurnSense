from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Analytics | ChurnSense",
    page_icon="📊",
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


def add_predictions(data, model):
    missing = [col for col in FEATURES if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    model_input = data[FEATURES].copy()

    for col in NUMERIC_FEATURES:
        model_input[col] = pd.to_numeric(
            model_input[col], errors="coerce"
        )

    output = data.copy()
    predictions = model.predict(model_input)

    output["Predicted_Churn"] = predictions
    output["Predicted_Churn_Status"] = output[
        "Predicted_Churn"
    ].map({1: "Yes", 0: "No", "Yes": "Yes", "No": "No"})

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(model_input)
        classes = list(model.classes_)

        if 1 in classes:
            positive_index = classes.index(1)
        elif "Yes" in classes:
            positive_index = classes.index("Yes")
        else:
            positive_index = None

        if positive_index is not None:
            output["Churn_Probability"] = (
                probabilities[:, positive_index] * 100
            )

    return output


st.title("📊 ChurnSense Analytics Dashboard")
st.write(
    "Analyze customer churn predictions, explore customer segments, "
    "and identify groups that may need retention efforts."
)

if not MODEL_PATH.exists():
    st.error(f"Model file not found: {MODEL_PATH}")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload a customer CSV file",
    type=["csv"],
    key="analytics_csv",
)

st.caption(
    "Upload data containing the 19 required model features. "
    "An optional Churn column enables comparison with actual outcomes."
)

if uploaded_file is None:
    st.info(
        "Upload a CSV to view analytics. You can use your test dataset "
        "or the batch prediction output if it contains the original "
        "customer feature columns."
    )
    st.stop()

try:
    data = pd.read_csv(uploaded_file)

    if data.empty:
        st.warning("The uploaded CSV contains no rows.")
        st.stop()

    if len(data) > 100_000:
        st.error("Please upload a file with no more than 100,000 rows.")
        st.stop()

    model = load_model()
    results = add_predictions(data, model)

except Exception as exc:
    st.error(f"Could not analyze this file: {exc}")
    st.stop()

if results.empty:
    st.warning("No customer records are available to analyze.")
    st.stop()

total = len(results)
churners = results["Predicted_Churn_Status"].eq("Yes").sum()
non_churners = results["Predicted_Churn_Status"].eq("No").sum()
predicted_rate = churners / total * 100

st.divider()
st.subheader("1. Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers analyzed", f"{total:,}")
col2.metric("Predicted churners", f"{churners:,}")
col3.metric("Predicted non-churners", f"{non_churners:,}")
col4.metric("Predicted churn rate", f"{predicted_rate:.1f}%")

if "Churn_Probability" in results.columns:
    st.metric(
        "Average predicted churn probability",
        f"{results['Churn_Probability'].mean():.1f}%",
    )

st.divider()
st.subheader("2. Predicted churn distribution")

distribution = (
    results["Predicted_Churn_Status"]
    .value_counts()
    .reindex(["Yes", "No"], fill_value=0)
    .rename_axis("Prediction")
    .reset_index(name="Customers")
)

fig = px.bar(
    distribution,
    x="Prediction",
    y="Customers",
    color="Prediction",
    text="Customers",
    title="Customers by predicted churn status",
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("3. Churn by customer segment")

segment_options = {
    "Contract": "Contract",
    "Internet service": "InternetService",
    "Payment method": "PaymentMethod",
    "Paperless billing": "PaperlessBilling",
    "Partner status": "Partner",
    "Dependents": "Dependents",
}

selected_label = st.selectbox(
    "Select a customer segment",
    list(segment_options.keys()),
)

segment_column = segment_options[selected_label]

segment_data = results.copy()
segment_data[segment_column] = (
    segment_data[segment_column].fillna("Unknown").astype(str)
)

segment_summary = (
    segment_data.groupby(segment_column, dropna=False)
    .agg(
        Customers=("Predicted_Churn_Status", "size"),
        Predicted_Churners=(
            "Predicted_Churn_Status",
            lambda values: values.eq("Yes").sum(),
        ),
    )
    .reset_index()
)

segment_summary["Predicted_Churn_Rate"] = (
    segment_summary["Predicted_Churners"]
    / segment_summary["Customers"]
    * 100
).round(2)

fig_segment = px.bar(
    segment_summary,
    x=segment_column,
    y="Predicted_Churn_Rate",
    text="Predicted_Churn_Rate",
    title=f"Predicted churn rate by {selected_label.lower()}",
    labels={
        "Predicted_Churn_Rate": "Predicted churn rate (%)",
        segment_column: selected_label,
    },
)
fig_segment.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig_segment.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig_segment, use_container_width=True)

st.dataframe(segment_summary, use_container_width=True)

st.divider()
st.subheader("4. Tenure and monthly charges")

left, right = st.columns(2)

with left:
    tenure_data = results.copy()
    tenure_data["tenure"] = pd.to_numeric(
        tenure_data["tenure"], errors="coerce"
    )
    tenure_data = tenure_data.dropna(subset=["tenure"])

    if not tenure_data.empty:
        tenure_data["Tenure_Group"] = pd.cut(
            tenure_data["tenure"],
            bins=[-1, 12, 24, 48, float("inf")],
            labels=["0–12 months", "13–24 months",
                    "25–48 months", "49+ months"],
        )

        tenure_summary = (
            tenure_data.groupby("Tenure_Group", observed=False)
            .agg(
                Customers=("Predicted_Churn_Status", "size"),
                Predicted_Churners=(
                    "Predicted_Churn_Status",
                    lambda values: values.eq("Yes").sum(),
                ),
            )
            .reset_index()
        )

        tenure_summary["Predicted_Churn_Rate"] = (
            tenure_summary["Predicted_Churners"]
            / tenure_summary["Customers"].replace(0, float("nan"))
            * 100
        )

        fig_tenure = px.bar(
            tenure_summary,
            x="Tenure_Group",
            y="Predicted_Churn_Rate",
            title="Predicted churn by tenure",
            labels={
                "Tenure_Group": "Tenure",
                "Predicted_Churn_Rate": "Predicted churn rate (%)",
            },
        )
        fig_tenure.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig_tenure, use_container_width=True)
    else:
        st.info("No usable numeric tenure values were found.")

with right:
    charges_data = results.copy()
    charges_data["MonthlyCharges"] = pd.to_numeric(
        charges_data["MonthlyCharges"], errors="coerce"
    )
    charges_data = charges_data.dropna(subset=["MonthlyCharges"])

    if not charges_data.empty:
        fig_charges = px.box(
            charges_data,
            x="Predicted_Churn_Status",
            y="MonthlyCharges",
            color="Predicted_Churn_Status",
            title="Monthly charges by predicted churn status",
            labels={
                "Predicted_Churn_Status": "Predicted churn",
                "MonthlyCharges": "Monthly charges",
            },
        )
        st.plotly_chart(fig_charges, use_container_width=True)
    else:
        st.info("No usable monthly charge values were found.")

st.divider()
st.subheader("5. Actual churn comparison (optional)")

if "Churn" in results.columns:
    actual = (
        results["Churn"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"yes": 1, "no": 0, "1": 1, "0": 0})
    )

    valid = actual.notna()

    if valid.any():
        actual_rate = actual[valid].mean() * 100
        st.metric(
            "Actual churn rate in labeled records",
            f"{actual_rate:.1f}%",
        )

        comparison = pd.DataFrame({
            "Actual": actual[valid].map({1.0: "Yes", 0.0: "No"}),
            "Predicted": results.loc[
                valid, "Predicted_Churn_Status"
            ].values,
        })

        comparison_table = pd.crosstab(
            comparison["Actual"],
            comparison["Predicted"],
        ).reindex(
            index=["Yes", "No"],
            columns=["Yes", "No"],
            fill_value=0,
        )

        st.write("Actual vs predicted churn counts")
        st.dataframe(comparison_table, use_container_width=True)

        st.caption(
            "This table compares predicted labels with the actual labels "
            "provided in the uploaded data. It is not a substitute for "
            "evaluating on a separate held-out test set."
        )
    else:
        st.info(
            "A Churn column was found, but it did not contain recognizable "
            "Yes/No or 1/0 labels."
        )
else:
    st.info(
        "No Churn column was supplied. This dashboard therefore reports "
        "predictions, not actual churn or model accuracy."
    )

st.divider()
st.subheader("6. Download analyzed data")

st.dataframe(results.head(20), use_container_width=True)

st.download_button(
    label="⬇️ Download analytics data as CSV",
    data=results.to_csv(index=False).encode("utf-8"),
    file_name="churnsense_analytics.csv",
    mime="text/csv",
)

st.caption(
    "ChurnSense | Predictions are estimates and should not be treated "
    "as confirmed customer outcomes."
)