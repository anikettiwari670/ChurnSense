import joblib
import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"


def load_model():
    """Load the saved, fitted churn prediction pipeline."""

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_single(model, single_customer_data):
    """Predict churn for one customer."""

    if not isinstance(single_customer_data, dict):
        raise TypeError(
            "single_customer_data must be a dictionary."
        )

    customer_df = pd.DataFrame([single_customer_data])

    prediction = model.predict(customer_df)[0]

    return "Yes" if prediction == 1 else "No"


def predict_batch(model, batch_customers_data):
    """Predict churn for multiple customers."""

    if not isinstance(batch_customers_data, pd.DataFrame):
        raise TypeError(
            "batch_customers_data must be a pandas DataFrame."
        )

    if batch_customers_data.empty:
        raise ValueError("Customer DataFrame cannot be empty.")

    predictions = model.predict(batch_customers_data)

    results = batch_customers_data.copy()

    results["Predicted_Churn"] = predictions

    results["Predicted_Churn_Status"] = (
        results["Predicted_Churn"].map({
            1: "Yes",
            0: "No",
        })
    )

    return results