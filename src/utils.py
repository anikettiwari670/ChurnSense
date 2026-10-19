import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def churn_rate(df):
    return (df["Churn"].eq("Yes").mean() * 100).round(2)