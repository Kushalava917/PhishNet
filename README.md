# PhishNet

PhishNet is an **open-source, explainable, privacy-conscious phishing detection toolkit** for URLs and messages. It provides a local FastAPI service, command-line interface, web dashboard, and Chromium browser extension.

PhishNet is assistive software: it provides risk signals, not a guarantee of safety or a replacement for layered security controls.

## Why PhishNet
- **Local by default:** submitted URLs are analyzed as text and are not fetched.
- **Explainable:** results include classifications, confidence, indicators, severity, and evidence.
- **Usable anywhere:** use the API, CLI, web UI, or browser extension.
- **Offline baseline:** the heuristic detector works without model weights or external services.

## Threat model and scope
PhishNet analyzes untrusted user-provided text and URLs for common phishing indicators. The default service performs static local analysis only and does not fetch submitted URLs, helping avoid SSRF, tracking, and active-content execution.

## Limitations
- Heuristic baseline can produce false positives/false negatives
- It does not provide guaranteed phishing prevention or reputation verification
- Optional ML training requires your own licensed dataset and is not enabled by default
- The browser extension requires a running PhishNet API and currently targets Chromium Manifest V3

## Project structure
- `src/phishnet/` — package source (API, service, features, schemas, CLI)
- `src/phishnet/web/static/` — web dashboard assets
- `scripts/train.py` — baseline training + metrics + threshold support
- `scripts/evaluate.py` — evaluation script
- `tests/` — offline unit/API tests
- `extension/` — Chromium browser extension
- `Phishing UI.ipynb` and prior notebook code remain as research artifacts

## Quickstart (local demo, no external services)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ml]"
uvicorn phishnet.api:app --reload
```
Then open `http://127.0.0.1:8000`.

The API is also available at `http://127.0.0.1:8000/docs` through FastAPI's interactive documentation.

## API usage
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H 'content-type: application/json' \
  -d '{"url":"http://paypal-secure-login.example.top/verify"}'
```

Response includes:
- `classification`: `safe | suspicious | phishing`
- `confidence`
- `model_version`
- `analysis_mode`
- `indicators`

## CLI usage
```bash
phishnet analyze "http://example.com" --type url
phishnet analyze "Urgent verify your account now" --type message
python -m phishnet analyze "https://www.example.org" --type url
```

## Training & evaluation
PhishNet does not bundle datasets.
Use only datasets with clear licensing/permission for your use.

```bash
python scripts/train.py --dataset /path/to/dataset.csv --text-column text --label-column label --threshold 0.5
python scripts/evaluate.py --dataset /path/to/eval.csv --model artifacts/baseline_model.joblib
```

Training/evaluation reports precision, recall, F1, confusion matrix, and sample false positives/false negatives.
Threshold is configurable.

## Dataset provenance and licensing
- Do not commit proprietary/private datasets.
- Record dataset origin, license, and preprocessing choices in your experiment notes or PRs.
- Existing notebooks in this repo are retained for historical research context only.

## Privacy policy (project defaults)
- Inputs are treated as untrusted.
- No URL fetching or remote execution by default.
- No raw URL/message logging in normal request flow.
- CORS is deny-by-default unless `PHISHNET_CORS_ALLOW_ORIGINS` is explicitly set.
- The extension sends only the active tab URL to the configured API and stores results in memory per tab.

## Browser extension setup
The extension analyzes top-level HTTP(S) pages, displays safe/suspicious/phishing results with explainable indicators, supports manual re-checking, and can show browser notifications.

See [`extension/README.md`](extension/README.md) for installation, permissions, privacy behavior, and configuration.

## Development
```bash
pip install -e ".[dev,ml]"
ruff check .
ruff format --check .
pytest
```

## Responsible use warning
PhishNet provides risk signals only. Do not rely on it as the sole control for account, financial, or incident-response decisions.

## Architecture summary
1. Input validation (`schemas.py`)
2. Feature extraction (`features.py`)
3. Heuristic scoring/classification (`heuristics.py`)
4. Unified response (`service.py`)
5. API/UI/CLI/extension interfaces (`api.py`, static UI, `cli.py`, `extension/`)

## Roadmap
- Add pluggable offline ML model loading
- Improve multilingual phishing indicators
- Add calibration and benchmark suites
- Add optional isolated external reputation integrations

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security reporting
See [SECURITY.md](SECURITY.md).

## License
MIT (see [LICENSE](LICENSE)).
