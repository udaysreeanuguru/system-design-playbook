import pytest
from solutions.python.url_shortener import UrlShortener, to_base62, from_base62

def test_base62_roundtrip():
    nums = [0, 1, 10, 61, 62, 12345, 10**6]
    for n in nums:
        code = to_base62(n)
        assert from_base62(code) == n

def test_shorten_and_resolve_idempotent():
    svc = UrlShortener()
    code1 = svc.shorten("https://example.com/alpha")
    code2 = svc.shorten("https://example.com/alpha")
    assert code1 == code2
    assert svc.resolve(code1) == "https://example.com/alpha"

def test_multiple_urls_get_unique_codes():
    svc = UrlShortener()
    codes = {svc.shorten(f"https://example.com/{i}") for i in range(5)}
    assert len(codes) == 5
