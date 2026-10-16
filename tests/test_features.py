from phishnet.features import (
    detect_urls_in_text,
    extract_message_indicators,
    extract_url_indicators,
)


def test_url_indicators_detect_multiple_risks() -> None:
    indicators = extract_url_indicators(
        "http://192.168.0.1/login?next=%2Fverify",
        long_url_length=20,
        many_subdomains=2,
    )
    names = {item["name"] for item in indicators}
    assert "ip_address_host" in names
    assert "url_obfuscation" in names
    assert "missing_https" in names


def test_message_detects_urls_and_keywords() -> None:
    text = "Urgent: verify account within 24 hours at http://secure-login-paypal.example.top"
    indicators = extract_message_indicators(text, long_url_length=75, many_subdomains=3)
    names = {item["name"] for item in indicators}
    assert "contains_url" in names
    assert "social_engineering_keyword" in names


def test_detect_urls_in_text() -> None:
    urls = detect_urls_in_text("Visit https://example.org and www.test.com")
    assert urls == ["https://example.org", "www.test.com"]
