
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
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
    page_title="Predict Churn | ChurnSense",
    page_icon="🔮",
    layout="wide",
)

st.title("🔮 Predict Customer Churn")
st.write("Enter customer details to estimate churn risk.")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def is_churn_label(label):
    """Recognize positive churn labels such as 1 or 'Yes'."""
    return str(label).strip().lower() in {"1", "yes", "true"}


def get_churn_probability(model, customer):
    """Return churn probability, or None if unavailable."""
    if not hasattr(model, "predict_proba"):
        return None

    classes = list(model.classes_)
    churn_indices = [
        i for i, label in enumerate(classes)
        if is_churn_label(label)
    ]

    if not churn_indices:
        raise ValueError(
            f"Could not identify the churn class in model classes: {classes}"
        )

    probabilities = model.predict_proba(customer)[0]
    return float(probabilities[churn_indices[0]])


try:
    model = load_model()

    with st.form("predict_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior = st.selectbox("Senior Citizen", [0, 1])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.slider("Tenure (months)", 0, 72, 12)
            phone = st.selectbox("Phone Service", ["Yes", "No"])

            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["No", "Yes", "No phone service"],
            )

            internet = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"],
            )

            contract = st.selectbox(
                "Contract",
                ["Month-to-month", "One year", "Two year"],
            )

        with col2:
            online_security = st.selectbox(
                "Online Security",
                ["No", "Yes", "No internet service"],
            )

            online_backup = st.selectbox(
                "Online Backup",
                ["No", "Yes", "No internet service"],
            )

            device_protection = st.selectbox(
                "Device Protection",
                ["No", "Yes", "No internet service"],
            )

            tech_support = st.selectbox(
                "Tech Support",
                ["No", "Yes", "No internet service"],
            )

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["No", "Yes", "No internet service"],
            )

            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["No", "Yes", "No internet service"],
            )

            paperless = st.selectbox(
                "Paperless Billing",
                ["Yes", "No"],
            )

            payment = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
            )

            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                value=70.0,
                step=1.0,
            )

            total_charges = st.number_input(
                "Total Charges",
                min_value=0.0,
                value=840.0,
                step=10.0,
            )

        submitted = st.form_submit_button(
            "Predict Churn",
            use_container_width=True,
        )

    if submitted:
        customer = pd.DataFrame([{
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone,
            "MultipleLines": multiple_lines,
            "InternetService": internet,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }])

        # Match the order used when the model was trained, if available.
        expected = getattr(model, "feature_names_in_", None)
        if expected is not None:
            missing = [c for c in expected if c not in customer.columns]
            if missing:
                raise ValueError(f"Missing required model features: {missing}")
            customer = customer[list(expected)]

        prediction = model.predict(customer)[0]
        churn_predicted = is_churn_label(prediction)

        st.divider()
        st.subheader("Prediction Result")

        result_col, probability_col = st.columns(2)

        result_col.metric(
            "Predicted Churn",
            "Yes" if churn_predicted else "No",
        )

        probability = get_churn_probability(model, customer)

        if probability is not None:
            probability_col.metric(
                "Churn Probability",
                f"{probability * 100:.2f}%",
            )

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    number={"suffix": "%"},
                    title={"text": "Estimated Churn Probability"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "steps": [
                            {"range": [0, 40]},
                            {"range": [40, 70]},
                            {"range": [70, 100]},
                        ],
                    },
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            if probability >= 0.70:
                st.error("High estimated churn probability.")
            elif probability >= 0.40:
                st.warning("Moderate estimated churn probability.")
            else:
                st.success("Low estimated churn probability.")
        else:
            st.info(
                "This model does not support predict_proba, "
                "so a churn probability cannot be displayed."
            )

        st.caption(
            "This is a model estimate, not a guarantee that the customer will churn."
        )

except FileNotFoundError:
    st.error(
        "Model file not found. Ensure "
        "'models/churn_model_v1.pkl' exists in the project root."
    )
except Exception as e:
    st.error(f"Prediction failed: {e}")
