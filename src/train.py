import joblib
import pandas as pd

from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

from src.preprocessing import create_processor


ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "churn_model_v2.pkl"


def train_model():
    """Train and save a new churn prediction pipeline."""

    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {"Churn"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Remove rows with missing target labels.
    df = df.dropna(subset=["Churn"]).copy()

    # Convert Yes/No target labels to 1/0.
    y = (
        df["Churn"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"yes": 1, "no": 0})
    )

    if y.isna().any():
        raise ValueError(
            "Churn must contain only 'Yes' and 'No'."
        )

    # Remove the target and identifier from model inputs.
    X = df.drop(
        columns=["Churn", "customerID"],
        errors="ignore",
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    preprocessor = create_processor(X_train)

    pipeline = Pipeline(
        steps=[
            ("prep", preprocessor),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    print("\n--- Classification Report ---")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["No Churn", "Churn"],
            zero_division=0,
        )
    )

    print(
        "ROC-AUC:",
        round(roc_auc_score(y_test, probabilities), 4),
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)

    print("\nNew model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_model()