import time
from solutions.python.rate_limiter import RateLimiter

def test_burst_then_block():
    rl = RateLimiter(capacity=3, refill_rate=1)
    assert all(rl.allow("u1") for _ in range(3))
    assert rl.allow("u1") is False

def test_refill_over_time():
    rl = RateLimiter(capacity=2, refill_rate=2)
    assert rl.allow("ip") and rl.allow("ip")
    assert rl.allow("ip") is False
    time.sleep(0.6)  # ~1.2 tokens added
    assert rl.allow("ip") is True

def test_multiple_keys():
    rl = RateLimiter(capacity=1, refill_rate=0)
    assert rl.allow("k1") is True
    assert rl.allow("k1") is False
    assert rl.allow("k2") is True
