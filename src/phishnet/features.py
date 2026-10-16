"""Feature extraction for URLs and messages."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import unquote, urlparse

SUSPICIOUS_TLDS = {
    "zip",
    "top",
    "xyz",
    "click",
    "gq",
    "work",
    "country",
    "stream",
}

BRAND_KEYWORDS = {"paypal", "microsoft", "google", "apple", "amazon", "bank", "netflix"}
CREDENTIAL_KEYWORDS = {
    "verify",
    "password",
    "login",
    "sign in",
    "credential",
    "urgent",
    "confirm",
    "payment",
    "invoice",
    "gift card",
    "otp",
}
SHORTENER_HOSTS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "rb.gy"}
URL_PATTERN = re.compile(r"https?://[^\s]+|www\.[^\s]+", re.IGNORECASE)


def _normalize_url(candidate: str) -> str:
    value = candidate.strip()
    if value.startswith("www."):
        return f"http://{value}"
    return value


def detect_urls_in_text(text: str) -> list[str]:
    return URL_PATTERN.findall(text)


def _host_parts(url: str) -> tuple[str, list[str], str]:
    parsed = urlparse(_normalize_url(url))
    host = parsed.hostname or ""
    parts = [p for p in host.split(".") if p]
    tld = parts[-1].lower() if parts else ""
    return host.lower(), parts, tld


def extract_url_indicators(
    url: str, long_url_length: int, many_subdomains: int
) -> list[dict[str, str | int]]:
    indicators: list[dict[str, str | int]] = []
    normalized = _normalize_url(url)
    host, host_parts, tld = _host_parts(normalized)

    if len(normalized) > long_url_length:
        indicators.append(
            {
                "name": "long_url",
                "severity": "medium",
                "score": 10,
                "evidence": f"URL length is {len(normalized)}.",
            }
        )

    try:
        ipaddress.ip_address(host)
        indicators.append(
            {
                "name": "ip_address_host",
                "severity": "high",
                "score": 25,
                "evidence": "Host is an IP address instead of a domain.",
            }
        )
    except ValueError:
        pass

    subdomain_count = max(len(host_parts) - 2, 0)
    if subdomain_count >= many_subdomains:
        indicators.append(
            {
                "name": "excessive_subdomains",
                "severity": "medium",
                "score": 15,
                "evidence": f"Host contains {subdomain_count} subdomains.",
            }
        )

    if tld in SUSPICIOUS_TLDS:
        indicators.append(
            {
                "name": "suspicious_tld",
                "severity": "medium",
                "score": 15,
                "evidence": f"Top-level domain '.{tld}' is frequently abused.",
            }
        )

    decoded = unquote(normalized)
    if decoded != normalized or "%" in normalized:
        indicators.append(
            {
                "name": "url_obfuscation",
                "severity": "high",
                "score": 15,
                "evidence": "URL appears encoded or obfuscated.",
            }
        )

    if re.search(r"[@<>\[\]{}|^~]", normalized):
        indicators.append(
            {
                "name": "suspicious_characters",
                "severity": "medium",
                "score": 10,
                "evidence": "URL contains suspicious special characters.",
            }
        )

    if host in SHORTENER_HOSTS:
        indicators.append(
            {
                "name": "url_shortener",
                "severity": "medium",
                "score": 10,
                "evidence": "URL uses a shortening service.",
            }
        )

    lowered_url = normalized.lower()
    for brand in BRAND_KEYWORDS:
        if brand in lowered_url and host and brand not in host:
            indicators.append(
                {
                    "name": "brand_impersonation_pattern",
                    "severity": "high",
                    "score": 20,
                    "evidence": f"Brand keyword '{brand}' appears outside the primary host.",
                }
            )
            break

    for keyword in CREDENTIAL_KEYWORDS:
        if keyword in lowered_url:
            indicators.append(
                {
                    "name": "credential_or_payment_keyword",
                    "severity": "medium",
                    "score": 10,
                    "evidence": f"Keyword '{keyword}' present in URL.",
                }
            )
            break

    if urlparse(normalized).scheme != "https":
        indicators.append(
            {
                "name": "missing_https",
                "severity": "low",
                "score": 5,
                "evidence": "URL does not use HTTPS.",
            }
        )

    return indicators


def extract_message_indicators(
    message: str, long_url_length: int, many_subdomains: int
) -> list[dict[str, str | int]]:
    indicators: list[dict[str, str | int]] = []
    lowered = message.lower()
    urls = detect_urls_in_text(message)

    if urls:
        indicators.append(
            {
                "name": "contains_url",
                "severity": "medium",
                "score": 10,
                "evidence": f"Message contains {len(urls)} URL(s).",
            }
        )
        for url in urls[:3]:
            indicators.extend(
                extract_url_indicators(
                    url, long_url_length=long_url_length, many_subdomains=many_subdomains
                )
            )

    for keyword in CREDENTIAL_KEYWORDS:
        if keyword in lowered:
            indicators.append(
                {
                    "name": "social_engineering_keyword",
                    "severity": "medium",
                    "score": 10,
                    "evidence": f"Message includes keyword '{keyword}'.",
                }
            )
            break

    if any(
        token in lowered for token in ["immediately", "within 24 hours", "final warning", "act now"]
    ):
        indicators.append(
            {
                "name": "urgency_language",
                "severity": "medium",
                "score": 10,
                "evidence": "Urgent language detected.",
            }
        )

    if re.search(r"\b(account|bank|wallet|payment)\b", lowered) and re.search(
        r"\b(verify|confirm|unlock)\b", lowered
    ):
        indicators.append(
            {
                "name": "account_verification_request",
                "severity": "high",
                "score": 20,
                "evidence": "Message asks for account verification actions.",
            }
        )

    return indicators
