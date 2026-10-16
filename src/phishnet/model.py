"""Optional external/model inference interfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelPrediction:
    label: str
    confidence: float
    model_version: str
    available: bool = False


class LocalModelAdapter:
    """Placeholder for loading local ML models when available.

    This baseline intentionally returns unavailable to preserve full offline functionality.
    """

    def predict(self, text: str) -> ModelPrediction:  # noqa: ARG002
        return ModelPrediction(
            label="unknown", confidence=0.0, model_version="none", available=False
        )
