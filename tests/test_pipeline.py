
import joblib
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"

SAMPLE_CUSTOMER = pd.DataFrame([{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.0,
    "TotalCharges": 840.0
})


def test_model_file_exists():
    assert MODEL_PATH.exists(), f"Model not found: {MODEL_PATH}"


def test_model_loads():
    model = joblib.load(MODEL_PATH)
    assert model is not None


def test_model_predicts():
    model = joblib.load(MODEL_PATH)

    prediction = model.predict(SAMPLE_CUSTOMER)

    assert len(prediction) == 1
    assert prediction[0] in model.classes_


def test_prediction_probability():
    model = joblib.load(MODEL_PATH)

    if not hasattr(model, "predict_proba"):
        return

    probabilities = model.predict_proba(SAMPLE_CUSTOMER)

    assert probabilities.shape[0] == 1
    assert abs(probabilities.sum() - 1.0) < 1e-6