from fastapi.testclient import TestClient

from phishnet.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_analyze_url() -> None:
    response = client.post("/analyze", json={"url": "http://paypal-verify.example.top/login"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["classification"] in {"safe", "suspicious", "phishing"}
    assert payload["analysis_mode"] == "local"


def test_validation_error_for_both_fields() -> None:
    response = client.post("/analyze", json={"url": "https://example.com", "message": "x"})
    assert response.status_code == 422


def test_validation_error_for_empty_payload() -> None:
    response = client.post("/analyze", json={})
    assert response.status_code == 422
