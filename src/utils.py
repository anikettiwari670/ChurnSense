import pandas as pd


def load_data(file_path):
    """Load a CSV dataset into a DataFrame."""

    return pd.read_csv(file_path)


def churn_rate(df: pd.DataFrame) -> float:
    """Calculate the percentage of customers who churned."""

    if "Churn" not in df.columns:
        raise KeyError("Dataset Must Contain a 'Churn' Column.")

    if df.empty:
        raise ValueError("Cannot Calculate Churn Rate for Empty Data.")

    churn = df["Churn"]

    if churn.isna().any():
        raise ValueError(
            "The Churn Column Contains Missing Values."
        )

    if pd.api.types.is_numeric_dtype(churn):
        valid_values = set(churn.unique())

        if not valid_values.issubset({0, 1}):
            raise ValueError(
                "Numeric Churn Values Must be 0 or 1."
            )

        churned = churn.eq(1)

    else:
        normalized = churn.astype("string").str.strip().str.lower()

        valid_values = set(normalized.unique())

        if not valid_values.issubset({"yes", "no"}):
            raise ValueError(
                "Churn Must Contain Only 'Yes' and 'No'."
            )

        churned = normalized.eq("yes")

    return round(float(churned.mean() * 100), 2)