from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    fbeta_score,
    precision_score,
    recall_score,
)

from starter.ml.data import process_data


def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.ndarray
        Training data.
    y_train : np.ndarray
        Labels.
    Returns
    -------
    model : RandomForestClassifier
        Trained machine learning model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model


def compute_model_metrics(y, preds):
    """
    Validates the trained machine learning model using precision, recall, and
    F1.

    Inputs
    ------
    y : np.ndarray
        Known labels, binarized.
    preds : np.ndarray
        Predicted labels, binarized.
    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def compute_accuracy(y, preds):
    """Return classification accuracy for binarized labels and predictions."""
    return float(accuracy_score(y, preds))


def inference(model, X):
    """ Run model inferences and return the predictions.

    Inputs
    ------
    model : RandomForestClassifier
        Trained machine learning model.
    X : np.ndarray
        Data used for prediction.
    Returns
    -------
    preds : np.ndarray
        Predictions from the model.
    """
    return model.predict(X)


def save_model(
    path,
    model,
    encoder,
    lb,
    categorical_features,
    feature_columns,
    algorithm,
):
    """Save the fitted model and preprocessing artifacts as one joblib file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": model,
        "encoder": encoder,
        "lb": lb,
        "categorical_features": list(categorical_features),
        "feature_columns": list(feature_columns),
        "algorithm": algorithm,
    }
    joblib.dump(artifact, destination)
    return destination


def load_model(path):
    """Load a model artifact saved by ``save_model``."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Model artifact not found: {source}")
    return joblib.load(source)


def evaluate_slices(
    df,
    feature,
    model,
    encoder,
    lb,
    categorical_features,
    label="salary",
):
    """Score the model on each category of one categorical feature.

    Small and single-class slices are scored with ``zero_division=1`` so
    undefined precision or recall does not raise. Empty slices are skipped.

    Returns
    -------
    list[dict]
        One metrics row per observed category.
    """
    rows = []
    categories = sorted(df[feature].unique(), key=str)
    for category in categories:
        subset = df[df[feature] == category]
        if subset.empty:
            continue
        features, y_slice, _, _ = process_data(
            subset,
            categorical_features=categorical_features,
            label=label,
            training=False,
            encoder=encoder,
            lb=lb,
        )
        preds = inference(model, features)
        precision, recall, fbeta = compute_model_metrics(y_slice, preds)
        rows.append(
            {
                "feature": feature,
                "category": str(category),
                "n": int(len(subset)),
                "accuracy": compute_accuracy(y_slice, preds),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(fbeta),
            }
        )
    return rows


def format_slice_report(feature, rows):
    """Format slice metrics as plain text for ``slice_output.txt``."""
    lines = [
        f"Slice performance for feature: {feature}",
        (
            "Metrics use the held-out test rows. Precision, recall, and F1 "
            "use the binarized positive class. zero_division=1 applies when "
            "a slice has no positive labels or no positive predictions. "
            "Slices with fewer than 30 rows are unstable."
        ),
        "category | n | accuracy | precision | recall | f1 | note",
    ]
    for row in rows:
        note = "small_sample" if row["n"] < 30 else ""
        lines.append(
            f"{row['category']} | {row['n']} | {row['accuracy']:.4f} | "
            f"{row['precision']:.4f} | {row['recall']:.4f} | "
            f"{row['f1']:.4f} | {note}"
        )
    return "\n".join(lines) + "\n"
