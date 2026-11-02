# Contributing to PhishNet

Thanks for helping improve an open-source, privacy-first phishing analysis toolkit.

## Setup
1. Fork and clone
2. Create virtual environment
3. `pip install -e ".[dev,ml]"`
4. Run `ruff check . && ruff format --check . && pytest`

## Areas to contribute
- Improve explainable URL and message indicators
- Add tests for API, CLI, web UI, or extension behavior
- Improve the Chromium extension UX without adding unnecessary permissions
- Add reproducible evaluation datasets with clear licensing
- Improve documentation and accessibility

## Pull requests
- Keep changes focused
- Add/update tests when behavior changes
- Document privacy/security implications
- Do not commit datasets, model binaries, or secrets
- Update user-facing documentation when commands, API behavior, or extension behavior changes

For browser extension changes, validate JavaScript syntax and load `extension/` as an unpacked Chromium extension.

## Commit quality
- Use clear commit messages
- Include before/after behavior and limitations
