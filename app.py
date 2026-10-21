import streamlit as st

st.set_page_config(
    page_title="ChurnSense",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 ChurnSense")
st.subheader("Customer Churn Prediction & Analytics Platform")

st.markdown(
    """
    Welcome to **ChurnSense**, a machine learning application
    designed to predict customer churn and support data-driven
    customer retention decisions.
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔮 Predict Churn")
    st.write(
        "Predict churn for an individual customer using "
        "their account and service details."
    )

with col2:
    st.subheader("📂 Batch Prediction")
    st.write(
        "Upload a CSV file to predict churn for multiple "
        "customers and download the results."
    )

with col3:
    st.subheader("📊 Analytics")
    st.write(
        "Explore predicted churn distributions, customer "
        "segments, tenure, and monthly charges."
    )

st.divider()

st.info(
    "Use the navigation menu in the sidebar to open "
    "Predict Churn, Batch Prediction, or Analytics."
)

st.caption("ChurnSense | Machine Learning Portfolio Project")