"""FastAPI app for PhishNet."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import load_config
from .schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse
from .service import analyze_input

logger = logging.getLogger("phishnet")
logger.setLevel(logging.INFO)

config = load_config()
app = FastAPI(title="PhishNet API", version="0.1.0")

if config.cors_allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["POST", "GET"],
        allow_headers=["Content-Type"],
    )

static_dir = Path(__file__).parent / "web" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_version=config.model_version)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    try:
        return analyze_input(url=payload.url, message=payload.message, config=config)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid input.") from exc
    except Exception as exc:  # pragma: no cover
        logger.exception("analysis error: %s", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Analysis failed.") from exc
