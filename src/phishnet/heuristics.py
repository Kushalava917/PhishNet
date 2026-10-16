"""Heuristic classification utilities."""

from __future__ import annotations

from .schemas import Classification, Indicator


def score_indicators(indicators: list[dict[str, str | int]]) -> tuple[int, list[Indicator]]:
    normalized = [Indicator(**item, source="heuristic") for item in indicators]
    score = min(100, sum(int(item.score) for item in normalized))
    return score, normalized


def classify_score(score: int, phishing_score: int, suspicious_score: int) -> Classification:
    if score >= phishing_score:
        return "phishing"
    if score >= suspicious_score:
        return "suspicious"
    return "safe"


def confidence_from_score(score: int, label: Classification) -> float:
    if label == "safe":
        return round(max(0.5, 1 - (score / 100)), 3)
    return round(min(0.99, 0.5 + (score / 100) * 0.5), 3)
