# Script to train machine learning model.

import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from starter.ml.data import clean_data, process_data  # noqa: E402
from starter.ml.model import (  # noqa: E402
    compute_model_metrics,
    evaluate_slices,
    format_slice_report,
    inference,
    save_model,
    train_model,
)

CAT_FEATURES = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]
LABEL = "salary"
SLICE_FEATURE = "education"


def _score(model, features, labels):
    predictions = inference(model, features)
    precision, recall, fbeta = compute_model_metrics(labels, predictions)
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(fbeta),
    }


def main():
    """Clean the Census data, compare two models, and save the winner."""
    data_path = ROOT / "data" / "census.csv"
    raw = pd.read_csv(data_path, skipinitialspace=True)
    data = clean_data(raw)

    train, test = train_test_split(
        data,
        test_size=0.20,
        random_state=42,
        stratify=data[LABEL],
    )

    x_train, y_train, encoder, lb = process_data(
        train,
        categorical_features=CAT_FEATURES,
        label=LABEL,
        training=True,
    )
    x_test, y_test, _, _ = process_data(
        test,
        categorical_features=CAT_FEATURES,
        label=LABEL,
        training=False,
        encoder=encoder,
        lb=lb,
    )

    forest = train_model(x_train, y_train)
    # Scale inside the baseline only. train_model still returns the forest.
    logistic = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=1000, random_state=42),
            ),
        ]
    )
    logistic.fit(x_train, y_train)

    forest_metrics = _score(forest, x_test, y_test)
    logistic_metrics = _score(logistic, x_test, y_test)
    candidates = {
        "RandomForestClassifier": (forest, forest_metrics),
        "LogisticRegression": (logistic, logistic_metrics),
    }
    # Higher test F1 wins. An equal F1 keeps the random forest.
    chosen_name = max(
        candidates,
        key=lambda name: (
            candidates[name][1]["f1"],
            name == "RandomForestClassifier",
        ),
    )
    chosen_model, chosen_metrics = candidates[chosen_name]
    feature_columns = [column for column in train.columns if column != LABEL]

    model_path = ROOT / "model" / "model.pkl"
    save_model(
        model_path,
        chosen_model,
        encoder,
        lb,
        CAT_FEATURES,
        feature_columns,
        chosen_name,
    )

    slice_rows = evaluate_slices(
        test,
        SLICE_FEATURE,
        chosen_model,
        encoder,
        lb,
        CAT_FEATURES,
        label=LABEL,
    )
    slice_text = format_slice_report(SLICE_FEATURE, slice_rows)
    slice_path = ROOT / "slice_output.txt"
    slice_path.write_text(slice_text, encoding="utf-8")

    numeric_features = [
        column for column in feature_columns if column not in CAT_FEATURES
    ]
    metrics = {
        "rows_before_clean": int(len(raw)),
        "rows_after_clean": int(len(data)),
        "rows_dropped": int(len(raw) - len(data)),
        "training_samples": int(len(train)),
        "test_samples": int(len(test)),
        "algorithm": chosen_name,
        "label": LABEL,
        "classes": [str(value) for value in lb.classes_],
        "positive_class": str(lb.classes_[1]),
        "feature_columns": feature_columns,
        "categorical_features": CAT_FEATURES,
        "numerical_features": numeric_features,
        "random_forest": forest_metrics,
        "logistic_regression": logistic_metrics,
        "logistic_regression_note": (
            "StandardScaler is fit on the encoded training matrix "
            "inside the logistic regression pipeline only."
        ),
        "selected": chosen_metrics,
        "slice_feature": SLICE_FEATURE,
        "slices": slice_rows,
        "model_path": str(model_path),
    }
    metrics_path = ROOT / "model" / "metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Training samples: {len(train)}")
    print(f"Test samples: {len(test)}")
    print(f"Random forest: {forest_metrics}")
    print(f"Logistic regression: {logistic_metrics}")
    print(f"Selected: {chosen_name} {chosen_metrics}")
    print(f"Classes: {list(lb.classes_)}")
    print(slice_text)
    print(f"Saved model: {model_path}")
    print(f"Saved metrics: {metrics_path}")
    print(f"Saved slices: {slice_path}")


if __name__ == "__main__":
    main()
