"""Pydantic schemas for API contracts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Classification = Literal["safe", "suspicious", "phishing"]
InputType = Literal["url", "message"]


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str | None = Field(default=None, max_length=2048)
    message: str | None = Field(default=None, max_length=4096)

    @model_validator(mode="after")
    def exactly_one_input(self) -> "AnalyzeRequest":
        provided = [
            bool(self.url and self.url.strip()),
            bool(self.message and self.message.strip()),
        ]
        if sum(provided) != 1:
            raise ValueError("Provide exactly one of 'url' or 'message'.")
        return self

    @field_validator("url", "message")
    @classmethod
    def strip_values(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        return cleaned


class Indicator(BaseModel):
    name: str
    severity: Literal["low", "medium", "high"]
    score: int = Field(ge=0, le=100)
    evidence: str
    source: Literal["heuristic", "model"] = "heuristic"


class AnalyzeResponse(BaseModel):
    classification: Classification
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str
    analysis_mode: Literal["local", "external"]
    input_type: InputType
    indicators: list[Indicator]
    summary: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    model_version: str
