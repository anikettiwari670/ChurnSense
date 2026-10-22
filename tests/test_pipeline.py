import joblib
import numpy as np
import pandas as pd
import pytest
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "churn_model_v1.pkl"


# --------------------------------------------------
# 2. Sample customer data
# --------------------------------------------------
SAMPLE_CUSTOMER = pd.DataFrame(
    [
        {
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
            "TotalCharges": 840.0,
        }
    ]
)


# --------------------------------------------------
# 3. Load model fixture
# --------------------------------------------------
@pytest.fixture(scope="module")
def model():
    assert MODEL_PATH.exists(), f"Model Not Found: {MODEL_PATH}"
    return joblib.load(MODEL_PATH)


# --------------------------------------------------
# 4. Test model file exists
# --------------------------------------------------
def test_model_file_exists():
    assert MODEL_PATH.is_file(), f"Model Not Found: {MODEL_PATH}"


# --------------------------------------------------
# 5. Test model loads successfully
# --------------------------------------------------
def test_model_loads(model):
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")


# --------------------------------------------------
# 6. Test model prediction
# --------------------------------------------------
def test_model_predicts(model):
    prediction = model.predict(SAMPLE_CUSTOMER)

    assert len(prediction) == 1
    assert prediction[0] in [0, 1]


# --------------------------------------------------
# 7. Test prediction probabilities
# --------------------------------------------------
def test_prediction_probability(model):
    probabilities = model.predict_proba(SAMPLE_CUSTOMER)

    assert probabilities.shape == (1, len(model.classes_))
    assert np.isfinite(probabilities).all()
    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)
    assert np.isclose(probabilities.sum(), 1.0)


# --------------------------------------------------
# 8. Test expected input features
# --------------------------------------------------
def test_input_features(model):
    expected_features = [
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

    assert list(model.feature_names_in_) == expected_features


# --------------------------------------------------
# 9. Test prediction output type
# --------------------------------------------------
def test_prediction_output_type(model):
    prediction = model.predict(SAMPLE_CUSTOMER)

    assert isinstance(prediction, np.ndarray) 