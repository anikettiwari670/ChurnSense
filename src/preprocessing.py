import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def get_feature_columns(df: pd.DataFrame):
    """Identify numerical and categorical input features."""

    X = df.drop(columns = ["customerID", "Churn"], errors = "ignore")

    num_cols = X.select_dtypes(include = "number").columns.tolist()

    cat_cols = X.select_dtypes(include = ["object", "category", "string", "bool"]).columns.tolist()

    return num_cols, cat_cols


def create_processor(df: pd.DataFrame):
    """Create preprocessing pipelines for customer features."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a Pandas DataFrame.")

    num_cols, cat_cols = get_feature_columns(df)

    if not num_cols and not cat_cols:
        raise ValueError("No Numerical or Categorical Features Found.")

    num_pipeline = Pipeline(
        steps = [
            ("imputer", SimpleImputer(strategy = "median")),
            ("scaler", StandardScaler()),
        ]
    )

    cat_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy = "most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown = "ignore"),
            ),
        ]
    )

    transformers = []

    if num_cols:
        transformers.append(("num", num_pipeline, num_cols))

    if cat_cols:
        transformers.append(("cat", cat_pipeline, cat_cols))

    preprocessor = ColumnTransformer(
        transformers = transformers,
        remainder = "drop", # remainder = "drop" 
    )

    return preprocessor