"""Evaluate a saved baseline model."""

from __future__ import annotations

import argparse

import joblib
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    return parser.parse_args()


def normalize_label(value: object) -> int:
    if isinstance(value, str):
        return 1 if value.strip().lower() in {"phishing", "1", "true"} else 0
    return int(value)


def main() -> None:
    args = parse_args()
    model_data = joblib.load(args.model)
    pipeline = model_data["pipeline"]
    threshold = float(model_data.get("threshold", 0.5))

    df = pd.read_csv(args.dataset)
    X = df[args.text_column].astype(str)
    y = df[args.label_column].apply(normalize_label)

    probabilities = pipeline.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    print("Precision:", round(precision_score(y, predictions, zero_division=0), 4))
    print("Recall:", round(recall_score(y, predictions, zero_division=0), 4))
    print("F1:", round(f1_score(y, predictions, zero_division=0), 4))
    print("Confusion Matrix:")
    print(confusion_matrix(y, predictions))
    print(classification_report(y, predictions, target_names=["safe", "phishing"], zero_division=0))


if __name__ == "__main__":
    main()
