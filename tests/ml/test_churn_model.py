from pathlib import Path

import pandas as pd

from pipelines.ml.churn_model import ChurnModel


def create_training_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "customer_unique_id": "unique-1",
                "total_orders": 10,
                "total_items": 20,
                "total_spent": 1000.0,
                "average_order_value": 100.0,
                "customer_lifetime_days": 300,
                "recency": 10,
                "frequency": 10,
                "monetary": 1000.0,
                "churn": 0,
            },
            {
                "customer_unique_id": "unique-2",
                "total_orders": 2,
                "total_items": 3,
                "total_spent": 100.0,
                "average_order_value": 50.0,
                "customer_lifetime_days": 30,
                "recency": 120,
                "frequency": 2,
                "monetary": 100.0,
                "churn": 1,
            },
            {
                "customer_unique_id": "unique-3",
                "total_orders": 8,
                "total_items": 15,
                "total_spent": 800.0,
                "average_order_value": 100.0,
                "customer_lifetime_days": 250,
                "recency": 20,
                "frequency": 8,
                "monetary": 800.0,
                "churn": 0,
            },
            {
                "customer_unique_id": "unique-4",
                "total_orders": 1,
                "total_items": 1,
                "total_spent": 50.0,
                "average_order_value": 50.0,
                "customer_lifetime_days": 10,
                "recency": 150,
                "frequency": 1,
                "monetary": 50.0,
                "churn": 1,
            },
            {
                "customer_unique_id": "unique-5",
                "total_orders": 7,
                "total_items": 12,
                "total_spent": 700.0,
                "average_order_value": 100.0,
                "customer_lifetime_days": 200,
                "recency": 15,
                "frequency": 7,
                "monetary": 700.0,
                "churn": 0,
            },
            {
                "customer_unique_id": "unique-6",
                "total_orders": 3,
                "total_items": 4,
                "total_spent": 150.0,
                "average_order_value": 50.0,
                "customer_lifetime_days": 40,
                "recency": 100,
                "frequency": 3,
                "monetary": 150.0,
                "churn": 1,
            },
            {
                "customer_unique_id": "unique-7",
                "total_orders": 9,
                "total_items": 18,
                "total_spent": 900.0,
                "average_order_value": 100.0,
                "customer_lifetime_days": 280,
                "recency": 12,
                "frequency": 9,
                "monetary": 900.0,
                "churn": 0,
            },
            {
                "customer_unique_id": "unique-8",
                "total_orders": 2,
                "total_items": 2,
                "total_spent": 80.0,
                "average_order_value": 40.0,
                "customer_lifetime_days": 20,
                "recency": 130,
                "frequency": 2,
                "monetary": 80.0,
                "churn": 1,
            },
            {
                "customer_unique_id": "unique-9",
                "total_orders": 6,
                "total_items": 10,
                "total_spent": 600.0,
                "average_order_value": 100.0,
                "customer_lifetime_days": 180,
                "recency": 25,
                "frequency": 6,
                "monetary": 600.0,
                "churn": 0,
            },
            {
                "customer_unique_id": "unique-10",
                "total_orders": 1,
                "total_items": 1,
                "total_spent": 40.0,
                "average_order_value": 40.0,
                "customer_lifetime_days": 15,
                "recency": 140,
                "frequency": 1,
                "monetary": 40.0,
                "churn": 1,
            },
        ]
    )


def test_churn_model_should_be_trained(tmp_path: Path) -> None:
    data = create_training_data()

    model_path = tmp_path / "models" / "churn.joblib"

    model = ChurnModel(model_path)

    metrics = model.train(data)

    assert model_path.exists()

    assert set(metrics) == {
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }

    assert all(0.0 <= value <= 1.0 for value in metrics.values())


def test_churn_model_should_predict(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "models" / "churn_model.joblib"

    model = ChurnModel(model_path)

    training_data = create_training_data()

    model.train(training_data)

    prediction_data = training_data.drop(columns=["churn"])

    predictions = model.predict(prediction_data)

    assert len(predictions) == len(training_data)

    assert list(predictions.columns) == [
        "customer_unique_id",
        "churn_probability",
        "churn_prediction",
    ]


def test_churn_model_should_return_valid_predictions(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "models" / "churn_model.joblib"

    model = ChurnModel(model_path)

    training_data = create_training_data()

    model.train(training_data)

    prediction_data = training_data.drop(columns=["churn"])

    predictions = model.predict(prediction_data)

    assert predictions["churn_prediction"].isin([0, 1]).all()

    assert (
        predictions["churn_probability"]
        .between(
            0,
            1,
        )
        .all()
    )


def test_churn_model_should_load_trained_model(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "models" / "churn_model.joblib"

    model = ChurnModel(model_path)

    training_data = create_training_data()

    model.train(training_data)

    loaded_model = model.load()

    assert loaded_model is not None
