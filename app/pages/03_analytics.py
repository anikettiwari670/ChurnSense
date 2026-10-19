import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "WA_Fn-UseC_Telco.csv"
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"
ROC_PATH = ROOT / "reports" / "roc_curves.png"

st.set_page_config(
    page_title="Model Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Model Analytics")

if ROC_PATH.exists():
    st.subheader("ROC Curve")
    st.image(str(ROC_PATH), use_container_width=True)
else:
    st.info(
        "ROC curve image not found. Add your saved ROC curve "
        "to the reports folder."
    )

try:
    model = joblib.load(MODEL_PATH)

    st.subheader("Model Information")
    st.write("Loaded model:", type(model).__name__)

    classifier = (
        model.steps[-1][1]
        if hasattr(model, "steps")
        else model
    )

    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_

        if hasattr(model, "feature_names_in_"):
            feature_names = model.feature_names_in_
        else:
            feature_names = [
                f"Feature {i + 1}"
                for i in range(len(importances))
            ]

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances
        }).sort_values("Importance", ascending=False).head(15)

        fig = px.bar(
            importance_df.sort_values("Importance"),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Feature Importances"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(
            "This model does not expose feature_importances_. "
            "For Logistic Regression, coefficients can be examined "
            "after accounting for preprocessing."
        )

except FileNotFoundError:
    st.warning("Train and save your model to view model analytics.")

except Exception as e:
    st.error(f"Unable to load analytics: {e}")