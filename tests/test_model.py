"""Unit tests for training, persistence, and inference."""

from pathlib import Path

import numpy as np

from starter.ml.model import inference, load_model, save_model, train_model

ROOT = Path(__file__).resolve().parents[1]


def _tiny_training_set():
    features = np.array(
        [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.2, 0.1],
            [0.9, 0.8],
        ]
    )
    labels = np.array([0, 0, 1, 1, 0, 1])
    return features, labels


def test_train_model_returns_fitted_model():
    features, labels = _tiny_training_set()
    model = train_model(features, labels)

    assert hasattr(model, "predict")
    predictions = model.predict(features)
    assert len(predictions) == len(labels)


def test_save_and_load_model(tmp_path):
    features, labels = _tiny_training_set()
    model = train_model(features, labels)
    destination = tmp_path / "model.pkl"

    save_model(
        destination,
        model,
        encoder="encoder-placeholder",
        lb="lb-placeholder",
        categorical_features=["education"],
        feature_columns=["age", "education"],
        algorithm="RandomForestClassifier",
    )
    loaded = load_model(destination)

    assert loaded["algorithm"] == "RandomForestClassifier"
    assert loaded["categorical_features"] == ["education"]
    reloaded_predictions = inference(loaded["model"], features)
    assert len(reloaded_predictions) == len(labels)
    assert np.array_equal(reloaded_predictions, model.predict(features))


def test_inference_returns_valid_predictions():
    features, labels = _tiny_training_set()
    model = train_model(features, labels)

    predictions = inference(model, features)

    assert len(predictions) == len(labels)
    assert set(np.unique(predictions)).issubset({0, 1})


def test_saved_census_artifact_has_required_keys():
    artifact = load_model(ROOT / "model" / "model.pkl")

    for key in (
        "model",
        "encoder",
        "lb",
        "categorical_features",
        "feature_columns",
        "algorithm",
    ):
        assert key in artifact
    assert hasattr(artifact["model"], "predict")
    assert "education" in artifact["categorical_features"]
    assert "salary" not in artifact["feature_columns"]
