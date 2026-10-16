# Contributing to PhishNet

## Setup
1. Fork and clone
2. Create virtual environment
3. `pip install -e ".[dev,ml]"`
4. Run `ruff check . && ruff format --check . && pytest`

## Pull requests
- Keep changes focused
- Add/update tests when behavior changes
- Document privacy/security implications
- Do not commit datasets, model binaries, or secrets

## Commit quality
- Use clear commit messages
- Include before/after behavior and limitations
