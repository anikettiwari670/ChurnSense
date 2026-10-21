from pathlib import Path

import streamlit as st
from theme import apply_theme

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------
APP_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="ChurnSense | Customer Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply the custom dark theme globally
apply_theme()

# --------------------------------------------------
# PAGE DEFINITIONS
# --------------------------------------------------
home_page = st.Page(
    str(APP_DIR / "home.py"),
    title="Overview",
    icon="🏠",
    default=True,
)

predict_page = st.Page(
    str(APP_DIR / "pages" / "01_Predict.py"),
    title="Predict Churn",
    icon="🔮",
)

batch_page = st.Page(
    str(APP_DIR / "pages" / "02_Batch.py"),
    title="Batch Predictions",
    icon="📂",
)

analytics_page = st.Page(
    str(APP_DIR / "pages" / "03_Analytics.py"),
    title="Model Analytics",
    icon="📊",
)

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------
pg = st.navigation(
    {
        "WORKSPACE": [home_page],
        "CHURN INTELLIGENCE": [
            predict_page,
            batch_page,
        ],
        "MODEL PERFORMANCE": [
            analytics_page,
        ],
    },
    position="sidebar",
)

pg.run()