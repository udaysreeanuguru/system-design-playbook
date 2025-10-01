"""
Token-bucket rate limiter (per key).
"""

import time
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Bucket:
    capacity: float
    refill_rate: float  # tokens per second
    tokens: float
    last_refill: float = field(default_factory=time.monotonic)

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def allow(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class RateLimiter:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: Dict[str, Bucket] = {}

    def allow(self, key: str) -> bool:
        bucket = self._buckets.get(key)
        if bucket is None:
            bucket = self._buckets[key] = Bucket(self.capacity, self.refill_rate, self.capacity)
        return bucket.allow()
