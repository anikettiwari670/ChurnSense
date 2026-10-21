import pandas as pd


def load_data(file_path):
    """Load a CSV dataset into a DataFrame."""

    return pd.read_csv(file_path)


def churn_rate(df: pd.DataFrame) -> float:
    """Calculate the percentage of customers who churned."""

    if "Churn" not in df.columns:
        raise KeyError("Dataset must contain a 'Churn' column.")

    if df.empty:
        raise ValueError("Cannot calculate churn rate for empty data.")

    churn = df["Churn"]

    if churn.isna().any():
        raise ValueError(
            "The Churn column contains missing values."
        )

    if pd.api.types.is_numeric_dtype(churn):
        valid_values = set(churn.unique())

        if not valid_values.issubset({0, 1}):
            raise ValueError(
                "Numeric Churn values must be 0 or 1."
            )

        churned = churn.eq(1)

    else:
        normalized = churn.astype("string").str.strip().str.lower()

        valid_values = set(normalized.unique())

        if not valid_values.issubset({"yes", "no"}):
            raise ValueError(
                "Churn must contain only 'Yes' and 'No'."
            )

        churned = normalized.eq("yes")

    return round(float(churned.mean() * 100), 2)