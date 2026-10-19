import pandas as pd

from src.model import predict_single, predict_batch


def test_predict_single(model, single_customer_data):
    prediction = predict_single(model, single_customer_data)
    assert prediction in ["Yes", "No"]


def test_predict_batch(model, batch_customers_data):
    results = predict_batch(model, batch_customers_data)

    assert len(results) == len(batch_customers_data)
    assert "Predicted_Churn" in results.columns
    assert "Predicted_Churn_Status" in results.columns