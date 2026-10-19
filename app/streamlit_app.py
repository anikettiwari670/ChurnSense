import streamlit as st

st.set_page_config(
    page_title="ChurnSense",
    page_icon="🏢",
    layout="wide",
)

home_page = st.Page(
    "home.py",
    title="Home",
    icon="🏠",
    default=True,
)

predict_page = st.Page(
    "pages/01_predict.py",
    title="Customer Prediction",
    icon="🔍",
)

batch_page = st.Page(
    "pages/02_batch.py",
    title="Batch Prediction",
    icon="📁",
)

analytics_page = st.Page(
    "pages/03_analytics.py",
    title="Model Analytics",
    icon="📊",
)

pg = st.navigation(
    {
        "Dashboard": [home_page],
        "Churn Prediction": [predict_page, batch_page],
        "Analytics": [analytics_page],
    }
)

pg.run()