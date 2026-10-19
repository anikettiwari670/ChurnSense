
import pandas as pd
import joblib


def load_model():
    return joblib.load("models/churn_model_v1.pkl")


def predict_single(model, single_customer_data): # Within predict_single(), we provide a single customer's dictionary. 
    customer_df = pd.DataFrame([single_customer_data])
    prediction = model.predict(customer_df)[0]

    return "Yes" if prediction == 1 else "No"


def predict_batch(model, batch_customers_data): # Within predict_batch(), we provide a DataFrame of all customers.
    predictions = model.predict(batch_customers_data) 

    results = batch_customers_data.copy()
    results["Predicted_Churn"] = predictions
    results["Predicted_Churn_Status"] = (results["Predicted_Churn"].map({1: "Yes", 0: "No"}))

    return results