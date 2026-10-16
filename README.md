# PhishNet

PhishNet is an **explainable, privacy-conscious phishing detection toolkit** for URLs and messages.
It is assistive software, not a guarantee of safety and not a substitute for professional security controls.

## Threat model and scope
PhishNet analyzes untrusted user-provided text and URLs to detect common phishing indicators.
By default it does **static local analysis only** and does **not fetch submitted URLs**, which helps avoid SSRF and active-content execution.

## Key capabilities
- FastAPI API with `POST /analyze` and `/health`
- Local heuristic baseline that works without model weights
- Explainable indicators with confidence and reasons
- Minimal web UI (served by FastAPI)
- CLI (`phishnet analyze ...`)
- Browser extension skeleton with warning + "Report incorrect result"
- Reproducible baseline training/evaluation scripts

## Limitations
- Heuristic baseline can produce false positives/false negatives
- No guaranteed phishing prevention
- Optional ML training requires your own licensed dataset

## Project structure
- `src/phishnet/` — package source (API, service, features, schemas, CLI)
- `src/phishnet/web/static/` — frontend
- `scripts/train.py` — baseline training + metrics + threshold support
- `scripts/evaluate.py` — evaluation script
- `tests/` — offline unit/API tests
- `extension/` — browser extension skeleton
- `Phishing UI.ipynb` and prior notebook code remain as research artifacts

## Quickstart (local demo, no external services)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ml]"
uvicorn phishnet.api:app --reload
```
Then open `http://127.0.0.1:8000`.

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

## Browser extension setup
See `extension/README.md`.

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
5. API/UI/CLI interfaces (`api.py`, static UI, `cli.py`)

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
