"""
A minimal, in-memory URL shortener prototype.

- Generates base62 codes from an auto-incrementing id
- Stores mappings in memory (dicts)
- Not production-ready: no persistence, auth, or rate limits
"""

from __future__ import annotations

import string
from dataclasses import dataclass

ALPHABET = string.digits + string.ascii_letters  # 0-9a-zA-Z (62 chars)
BASE = len(ALPHABET)


def to_base62(n: int) -> str:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return ALPHABET[0]
    chars = []
    while n > 0:
        n, r = divmod(n, BASE)
        chars.append(ALPHABET[r])
    return "".join(reversed(chars))


def from_base62(s: str) -> int:
    n = 0
    for ch in s:
        n = n * BASE + ALPHABET.index(ch)
    return n


@dataclass
class Record:
    code: str
    url: str


class UrlShortener:
    def __init__(self) -> None:
        self._id = 0
        self._code_to_url = {}
        self._url_to_code = {}

    def shorten(self, url: str) -> str:
        # return existing code if url already shortened
        if url in self._url_to_code:
            return self._url_to_code[url]
        self._id += 1
        code = to_base62(self._id)
        # in real systems, ensure uniqueness & handle reserved words
        self._code_to_url[code] = url
        self._url_to_code[url] = code
        return code

    def resolve(self, code: str) -> str | None:
        return self._code_to_url.get(code)

    def stats(self) -> dict:
        return {
            "count": len(self._code_to_url),
            "last_id": self._id,
        }
