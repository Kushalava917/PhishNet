"""Reproducible baseline training script.

Expected CSV columns:
- text or url
- label (0/1 or safe/phishing)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, help="Path to CSV dataset")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output", default="artifacts/baseline_model.joblib")
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


def normalize_label(value: object) -> int:
    if isinstance(value, str):
        return 1 if value.strip().lower() in {"phishing", "1", "true"} else 0
    return int(value)


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.dataset)
    if args.text_column not in df.columns:
        raise ValueError(f"Missing text column: {args.text_column}")
    if args.label_column not in df.columns:
        raise ValueError(f"Missing label column: {args.label_column}")

    X = df[args.text_column].astype(str)
    y = df[args.label_column].apply(normalize_label)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=30000)),
            ("clf", LogisticRegression(max_iter=500, class_weight="balanced")),
        ]
    )
    pipeline.fit(x_train, y_train)

    probabilities = pipeline.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= args.threshold).astype(int)

    print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 4))
    print("Recall:", round(recall_score(y_test, predictions, zero_division=0), 4))
    print("F1:", round(f1_score(y_test, predictions, zero_division=0), 4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print("Detailed Report:")
    print(
        classification_report(
            y_test, predictions, target_names=["safe", "phishing"], zero_division=0
        )
    )

    false_positive = x_test[(predictions == 1) & (y_test.to_numpy() == 0)].head(5).tolist()
    false_negative = x_test[(predictions == 0) & (y_test.to_numpy() == 1)].head(5).tolist()
    print("Sample False Positives:", false_positive)
    print("Sample False Negatives:", false_negative)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "threshold": args.threshold}, output_path)
    print(f"Saved model artifact to {output_path}")


if __name__ == "__main__":
    main()
