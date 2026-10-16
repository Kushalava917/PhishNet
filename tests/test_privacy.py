from phishnet.config import load_config


def test_external_analysis_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PHISHNET_ALLOW_EXTERNAL_ANALYSIS", raising=False)
    cfg = load_config()
    assert cfg.allow_external_analysis is False


def test_cors_is_deny_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PHISHNET_CORS_ALLOW_ORIGINS", raising=False)
    cfg = load_config()
    assert cfg.cors_allow_origins == []
