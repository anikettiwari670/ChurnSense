from pathlib import Path
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path

# Repository root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Project paths
DATA_PATH = ROOT_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
MODEL_PATH = ROOT_DIR / "models" / "churn_model_v1.pkl"


# Page configuration
st.set_page_config(
    page_title="ChurnSense",
    page_icon="🏢",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

# Load model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.title("📊 ChurnSense Dashboard")
st.caption("Telecom Customer Churn Prediction and Analytics")

try:
    df = load_data()

    total_customers = len(df)
    churned = (df["Churn"] == "Yes").sum()
    churn_rate = churned / total_customers * 100
    retained = total_customers - churned
    retention_rate = retained / total_customers * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churned Customers", f"{churned:,}")
    col3.metric("Churn Rate", f"{churn_rate:.2f}%")
    col4.metric("Retention Rate", f"{retention_rate:.2f}%")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Customer Churn Distribution")

        churn_counts = (
            df["Churn"]
            .value_counts()
            .rename_axis("Churn Status")
            .reset_index(name="Customers")
        )

        fig = px.pie(
            churn_counts,
            names="Churn Status",
            values="Customers",
            hole=0.45,
            title="Churn vs Retained Customers"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Contract Distribution")

        if "Contract" in df.columns:
            contract_counts = (
                df.groupby(["Contract", "Churn"])
                .size()
                .reset_index(name="Customers")
            )

            fig = px.bar(
                contract_counts,
                x="Contract",
                y="Customers",
                color="Churn",
                barmode="group",
                title="Churn by Contract Type"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Use the pages in the sidebar to predict individual customer churn, "
        "process customer CSV files, and review model analytics."
    )

except FileNotFoundError:
    st.error(
        "Required data file not found. Check the CSV filename "
        "and ensure it exists in the data folder."
    )
except Exception as e:
    st.error(f"Unable to load the dashboard: {e}")