import pandas as pd 

from src.model import predict_single, predict_batch 

def test_predict_single(model, single_customer_data):
    prediction = predict_single(model, single_customer_data)