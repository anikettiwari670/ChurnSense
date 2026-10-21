import pandas as pd
import pytest

from src.model import load_model, predict_single, predict_batch


# --------------------------------------------------
# 1. Fixtures
# --------------------------------------------------

@pytest.fixture
def model():
    """Load the saved churn prediction pipeline."""
    return load_model()


@pytest.fixture
def single_customer_data():
    """Sample input for one customer."""
    return {
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


@pytest.fixture
def batch_customers_data(single_customer_data):
    """Sample input for two customers."""
    second_customer = single_customer_data.copy()

    second_customer.update({
        "gender": "Female",
        "tenure": 48,
        "Contract": "Two year",
        "MonthlyCharges": 85.0,
        "TotalCharges": 4080.0,
    })

    return pd.DataFrame([
        single_customer_data,
        second_customer,
    ])


# --------------------------------------------------
# 2. Test single-customer prediction
# --------------------------------------------------

def test_predict_single(model, single_customer_data):
    prediction = predict_single(model, single_customer_data)

    assert prediction in ["Yes", "No"]


# --------------------------------------------------
# 3. Test batch predictions
# --------------------------------------------------

def test_predict_batch(model, batch_customers_data):
    results = predict_batch(model, batch_customers_data)

    assert len(results) == len(batch_customers_data)

    assert "Predicted_Churn" in results.columns
    assert "Predicted_Churn_Status" in results.columns

    assert results["Predicted_Churn"].isin([0, 1]).all()

    assert results["Predicted_Churn_Status"].isin(
        ["Yes", "No"]
    ).all()