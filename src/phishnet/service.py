"""Core analysis service."""

from __future__ import annotations

from .config import AppConfig, load_config
from .features import extract_message_indicators, extract_url_indicators
from .heuristics import classify_score, confidence_from_score, score_indicators
from .model import LocalModelAdapter
from .schemas import AnalyzeResponse

MODEL = LocalModelAdapter()


def analyze_input(
    url: str | None = None, message: str | None = None, config: AppConfig | None = None
) -> AnalyzeResponse:
    cfg = config or load_config()

    if bool(url) == bool(message):
        raise ValueError("Exactly one of url or message must be provided.")

    if url:
        raw_indicators = extract_url_indicators(
            url,
            long_url_length=cfg.thresholds.long_url_length,
            many_subdomains=cfg.thresholds.many_subdomains,
        )
        input_type = "url"
    else:
        raw_indicators = extract_message_indicators(
            message or "",
            long_url_length=cfg.thresholds.long_url_length,
            many_subdomains=cfg.thresholds.many_subdomains,
        )
        input_type = "message"

    score, indicators = score_indicators(raw_indicators)
    classification = classify_score(
        score,
        phishing_score=cfg.thresholds.phishing_score,
        suspicious_score=cfg.thresholds.suspicious_score,
    )
    confidence = confidence_from_score(score, classification)

    model_prediction = MODEL.predict(url or message or "")
    model_version = cfg.model_version
    if model_prediction.available:
        model_version = model_prediction.model_version

    return AnalyzeResponse(
        classification=classification,
        confidence=confidence,
        model_version=model_version,
        analysis_mode="local",
        input_type=input_type,
        indicators=indicators,
        summary=(
            "Heuristic baseline analysis completed locally. "
            "Indicators are assistive signals and not a guarantee."
        ),
    )
