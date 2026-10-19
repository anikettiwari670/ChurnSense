import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"

st.set_page_config(
    page_title="Predict Churn",
    page_icon="🔮",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.title("🔮 Predict Customer Churn")

try:
    model = load_model()

    with st.form("predict_form"):

        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox(
                "Gender", ["Male", "Female"]
            )

            senior = st.selectbox(
                "Senior Citizen", [0, 1]
            )

            partner = st.selectbox(
                "Partner", ["Yes", "No"]
            )

            dependents = st.selectbox(
                "Dependents", ["Yes", "No"]
            )

            tenure = st.slider(
                "Tenure (months)", 0, 72, 12
            )

            phone = st.selectbox(
                "Phone Service", ["Yes", "No"]
            )

            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["Yes", "No", "No phone service"]
            )

            internet = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"]
            )

            contract = st.selectbox(
                "Contract",
                ["Month-to-month", "One year", "Two year"]
            )

        with col2:
            online_security = st.selectbox(
                "Online Security",
                ["Yes", "No", "No internet service"]
            )

            online_backup = st.selectbox(
                "Online Backup",
                ["Yes", "No", "No internet service"]
            )

            device_protection = st.selectbox(
                "Device Protection",
                ["Yes", "No", "No internet service"]
            )

            tech_support = st.selectbox(
                "Tech Support",
                ["Yes", "No", "No internet service"]
            )

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["Yes", "No", "No internet service"]
            )

            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["Yes", "No", "No internet service"]
            )

            paperless = st.selectbox(
                "Paperless Billing", ["Yes", "No"]
            )

            payment = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                value=70.0
            )

            total_charges = st.number_input(
                "Total Charges",
                min_value=0.0,
                value=840.0
            )

        submitted = st.form_submit_button(
            "Predict Churn",
            use_container_width=True
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
            "TotalCharges": total_charges
        }])

        prediction = model.predict(customer)[0]

        st.divider()
        st.subheader("Prediction Result")

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(customer)[0]
            classes = list(model.classes_)

            churn_index = classes.index(1)
            churn_probability = probabilities[churn_index] * 100

            col1, col2 = st.columns(2)

            col1.metric(
                "Predicted Churn",
                "Yes" if prediction == 1 else "No"
            )

            col2.metric(
                "Churn Probability",
                f"{churn_probability:.2f}%"
            )

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=churn_probability,
                title={"text": "Churn Risk"},
                gauge={"axis": {"range": [0, 100]}}
            ))

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if churn_probability >= 70:
                st.error("High predicted churn risk.")
            elif churn_probability >= 40:
                st.warning("Moderate predicted churn risk.")
            else:
                st.success("Low predicted churn risk.")

        else:
            st.metric(
                "Predicted Churn",
                "Yes" if prediction == 1 else "No"
            )

except FileNotFoundError:
    st.error(
        "Trained model not found. Train and save the model "
        "to models/churn_model_v1.pkl first."
    )
except Exception as e:
    st.error(f"Prediction failed: {e}")