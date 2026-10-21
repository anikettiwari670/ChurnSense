import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] # Path(__file__).resolve() refers to the full path to app/pages/01_Predict.py, whereas .parents[0] refers to the "app/pages" folder, .parents[1] refers to the "app" folder, and .parents[2] refers to the "01_ChurnSense" project root.
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"

DATA_CANDIDATES = [
    ROOT / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv",
    ROOT / "data" / "WA_Fn-UseC_Telco.csv",
    ROOT / "data" / "WA_Fn-UseC_-Telco-Customer-Churn" / "WA_Fn-UseC_-Telco-Customer-Churn.csv",
]


st.set_page_config(
    page_title="Model Analytics | ChurnSense",
    page_icon="📈",
    layout="wide",
)

from theme import apply_theme
apply_theme()


st.title("📈 Model Analytics")
st.write("Explore Your Trained Model and Customer Churn Dataset.")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


def get_estimator(model):
    """Return the final estimator from a fitted sklearn Pipeline."""
    if hasattr(model, "steps"):
        return model.steps[-1][1]
    return model


def get_transformed_feature_names(model, estimator):
    """Get feature names after preprocessing, when available."""
    try:
        if hasattr(model, "steps") and len(model.steps) > 1:
            names = model[:-1].get_feature_names_out()
            if len(names) == len(estimator.coef_[0]):
                return [str(name) for name in names]

        names = getattr(model, "feature_names_in_", None)
        if names is not None:
            if len(names) == len(estimator.coef_[0]):
                return [str(name) for name in names]
    except (AttributeError, ValueError, TypeError):
        pass

    return [
        f"Feature {i + 1}"
        for i in range(len(estimator.coef_[0]))
    ]


# --------------------------------------------------
# Model information and feature analysis
# --------------------------------------------------
try:
    model = load_model()
    estimator = get_estimator(model)

    st.subheader("Model Information")

    col1, col2 = st.columns(2)
    col1.metric("Model Type", type(estimator).__name__)
    col2.metric(
        "Pipeline",
        "Yes" if hasattr(model, "steps") else "No",
    )

    # Logistic Regression coefficients.
    if hasattr(estimator, "coef_"):
        st.subheader("Logistic Regression Coefficients")

        coefficients = estimator.coef_

        if coefficients.ndim == 2 and coefficients.shape[0] > 1:
            coefficient_values = abs(coefficients).mean(axis=0)
            coefficient_description = (
                "Mean absolute coefficient across classes"
            )
        else:
            coefficient_values = coefficients.reshape(-1)
            coefficient_description = (
                "Positive Values Increase the Model's Log-Odds for its "
                "Positive Class; Negative Values Decrease them."
            )

        feature_names = get_transformed_feature_names(model, estimator)

        coefficient_df = pd.DataFrame({
            "Feature": feature_names,
            "Coefficient": coefficient_values,
        })

        coefficient_df["Absolute_Coefficient"] = (
            coefficient_df["Coefficient"].abs()
        )

        coefficient_df = coefficient_df.sort_values(
            "Absolute_Coefficient",
            ascending=False,
        ).head(15)

        fig = px.bar(
            coefficient_df.sort_values("Coefficient"),
            x="Coefficient",
            y="Feature",
            orientation="h",
            title="Top 15 Logistic Regression Coefficients",
            hover_data=["Absolute_Coefficient"],
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption(coefficient_description)

        st.write(
            "Note: Coefficient Direction Depends on the Class Coding and "
            "Preprocessing. With One-Hot Encoding, a Coefficient is Relative "
            "to the Relevant Reference Category. Coefficients are not "
            "Causal Effects."
        )

    # Tree-based model feature importances.
    elif hasattr(estimator, "feature_importances_"):
        st.subheader("Feature Importances")

        importances = estimator.feature_importances_

        try:
            feature_names = model[:-1].get_feature_names_out()
            if len(feature_names) != len(importances):
                raise ValueError("Feature-name count does not match.")
            feature_names = [str(name) for name in feature_names]
        except (AttributeError, ValueError, TypeError):
            feature_names = [
                f"Feature {i + 1}"
                for i in range(len(importances))
            ]

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances,
        }).sort_values(
            "Importance",
            ascending=False,
        ).head(15)

        fig = px.bar(
            importance_df.sort_values("Importance"),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Feature Importances",
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(
            "This Estimator does not Expose coef_ or feature_importances_. "
            "Check the Model Type and its Supported Interpretation Methods."
        )

except FileNotFoundError:
    st.error(
        "Model File not Found. Ensure "
        "'models/churn_model_v1.pkl' Exists in the Project Root."
    )
except Exception as e:
    st.error(f"Unable to Load Model Analytics: {e}")


# --------------------------------------------------
# Dataset overview
# --------------------------------------------------
st.divider()
st.subheader("Customer Dataset Overview")

DATA_PATH = next(
    (path for path in DATA_CANDIDATES if path.exists()),
    None,
)

if DATA_PATH is None:
    st.info(
        "Dataset CSV not found in the Expected Data Folder. "
        "Model Analytics can still work if the Trained Model is Present."
    )
else:
    try:
        df = load_data(str(DATA_PATH))

        st.caption(f"Dataset File: {DATA_PATH.name}")

        col1, col2 = st.columns(2)
        col1.metric("Total Records", f"{len(df):,}")
        col2.metric("Total Columns", len(df.columns))

        if "Churn" in df.columns:
            churn_counts = df["Churn"].astype(str).value_counts()

            fig = px.pie(
                values=churn_counts.values,
                names=churn_counts.index,
                title="Customer Churn Distribution",
                hole=0.4,
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Churn Summary")
            summary = churn_counts.rename_axis("Churn").reset_index(
                name="Customers"
            )
            summary["Percentage"] = (
                summary["Customers"] / len(df) * 100
            ).round(2)

            st.dataframe(summary, use_container_width=True)

        with st.expander("Preview Dataset"):
            st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"Could not Read the Dataset: {e}")