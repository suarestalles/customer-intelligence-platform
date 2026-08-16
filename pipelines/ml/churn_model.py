from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class ChurnModel:
    FEATURES = [
        "frequency",
        "monetary",
        "average_order_value",
        "total_items",
        "customer_lifetime_days",
        "recency",
    ]

    def __init__(self, model_path: Path) -> None:
        self.model_path = model_path

    def train(self, data: pd.DataFrame) -> dict[str, float]:
        X = data[self.FEATURES]
        y = data["churn"]

        test_size = max(
            0.2,
            y.nunique() / len(y),
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
            stratify=y,
        )

        model = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1000,
                        random_state=42,
                    ),
                ),
            ]
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        metrics = {
            "precision": precision_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "f1": f1_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "roc_auc": roc_auc_score(
                y_test,
                probabilities,
            ),
        }

        self.model_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(model, self.model_path)

        return metrics

    def load(self) -> Any:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        return joblib.load(self.model_path)

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        model = self.load()

        X = data[self.FEATURES]

        predictions = model.predict(X)
        probabilities = model.predict_proba(X)[:, 1]

        result = data[["customer_unique_id"]].copy()

        result["churn_probability"] = probabilities
        result["churn_prediction"] = predictions

        return result
