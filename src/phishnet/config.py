"""Configuration for PhishNet."""

import os
from dataclasses import dataclass, field


@dataclass(slots=True)
class HeuristicThresholds:
    phishing_score: int = 75
    suspicious_score: int = 30
    long_url_length: int = 75
    many_subdomains: int = 3
    max_input_length: int = 4096


@dataclass(slots=True)
class AppConfig:
    model_version: str = "heuristic-baseline-v1"
    allow_external_analysis: bool = False
    cors_allow_origins: list[str] = field(default_factory=list)
    thresholds: HeuristicThresholds = field(default_factory=HeuristicThresholds)


def load_config() -> AppConfig:
    origins = os.getenv("PHISHNET_CORS_ALLOW_ORIGINS", "").strip()
    parsed_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    allow_external = os.getenv("PHISHNET_ALLOW_EXTERNAL_ANALYSIS", "false").lower() == "true"
    return AppConfig(cors_allow_origins=parsed_origins, allow_external_analysis=allow_external)
