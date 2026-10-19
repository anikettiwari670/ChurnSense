import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


def get_feature_columns(df: pd.DataFrame):
    # Exclude "customerID" and target column ("Churn").
    X = df.drop(columns = ["customerID", "Churn"], errors = "ignore")

    num_cols = X.select_dtypes(include = "number").columns.tolist()

    cat_cols = X.select_dtypes(include = ["object", "category", "string", "bool"]).columns.tolist()

    return num_cols, cat_cols


def create_processor(df: pd.DataFrame):
    num_cols, cat_cols = get_feature_columns(df)

    num_pipeline = Pipeline(
        steps = [
            ("imputer", SimpleImputer(strategy = "median")),
            ("scaler", StandardScaler())
        ]
    )

    cat_pipeline = Pipeline(
        steps = [
            ("imputer", SimpleImputer(strategy = "most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown = "ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers = [
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols)
        ],
        remainder = "drop"
    )

    return preprocessor