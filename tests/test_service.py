from phishnet.config import AppConfig
from phishnet.service import analyze_input


def test_safe_url_classification() -> None:
    response = analyze_input(url="https://example.com")
    assert response.classification in {"safe", "suspicious"}


def test_phishing_like_message_classification() -> None:
    cfg = AppConfig()
    response = analyze_input(
        message="Urgent! Verify your bank account password now at http://verify-payments.example.top",
        config=cfg,
    )
    assert response.classification in {"suspicious", "phishing"}
    assert response.analysis_mode == "local"
    assert response.model_version


def test_requires_single_input() -> None:
    try:
        analyze_input(url="https://example.com", message="both")
    except ValueError:
        return
    else:
        raise AssertionError("Expected ValueError for providing both url and message")
