# Rate Limiter

**Slug:** `rate-limiter`  
**Difficulty:** Easy / Medium / Hard  
**Primary goals:** fairness, abuse-prevention, low latency, cost efficiency, consistency

## Problem
Protect backend services from abuse and bursty traffic by limiting how many requests a principal(user, API Key, IP, org) can make in 
given time window. The limiter must be fast, consistent enough to stop spikes, and cheap to run at scale.

## Requirements
- Functional:
allow(key) returns True if the request is permitted and consumes quota, else False.

Support multiple policies (e.g., user: 100 req/min, ip: 20 req/sec).

Support independent buckets per key.

Provide an admin/ops way to change limits and a kill-switch/bypass list.
  - ...
- Non-functional:
allow(key) returns True if the request is permitted and consumes quota, else False.

Support multiple policies (e.g., user: 100 req/min, ip: 20 req/sec).

Support independent buckets per key.

Provide an admin/ops way to change limits and a kill-switch/bypass list....

## Capacity & Constraints (back-of-the-envelope)
Assume 50k RPS peak to the limiter with a 90/10 read/write mix (reads = checks, writes = token updates).

Active keys at peak: ~5M/day, hot keys follow power-law.

Memory per key (Redis hash): ~60–120 bytes (tokens, last_refill, metadata).
→ 5M hot keys ≈ 0.5 GB to 1 GB; shard across nodes.

## High-Level Design
Algorithm choice

Use Token Bucket (burst-friendly) as default; optionally support Leaky Bucket (smoother) or Fixed Window / Sliding Window for specific rules.

Token Bucket parameters:

capacity – max tokens allowed to accumulate.

refill_rate – tokens added per second.

allow():

Refill tokens: tokens = min(capacity, tokens + rate * (now - last_refill))

If tokens >= 1, decrement and allow; else deny.

Deployment models

In-process (fastest, simple)

Per-instance memory; good for single node or when slight inconsistency across nodes is acceptable.

Add sticky routing or consistent hashing of keys to reduce cross-node skew.

Centralized store (Redis/Memcached) (recommended)

All app nodes call Redis using atomic ops (Lua or SET/GET with EVAL).

Pros: global view, consistent limits across nodes; simple to scale via sharding.

Cons: extra network hop; need HA Redis.

Sidecar/Service

Dedicated “rate-limit service” with gRPC/HTTP; apps call it.

Easier to evolve policies; cache results client-side for ultra-hot keys.

Data model (Redis example)

Key: rl:{policy}:{key} → Hash fields:

tokens (float), last_refill (timestamp), capacity, rate

TTL: optional (e.g., 24h) to auto-expire dormant keys.

Atomic script (Lua) to refill + consume in one round-trip.

API design

Library (in-process):
bool allow(key: str)
Policy(capacity: float, refill_rate: float)

Service:
POST /v1/allow { key, policy } → { allowed: bool, remaining_tokens, reset_in_ms }
POST /v1/policies (admin) to add/update/delete rules.

Scaling plan

Sharding keys across Redis cluster by hash(key).

Hot keys: enable local LRU cache with short TTL (e.g., 50–100 ms) to reduce thrash.

Multi-region: pick one:

Per-region limits (eventual consistency across regions).

Global limit via region-leader or CRDT counter (higher latency/complexity).

Consistency & fairness

Token bucket is eventually consistent in distributed setups; brief over-allow can happen during network partitions or clock skew.

To cap damage, include a hard ceiling per request path (e.g., N per second per instance).

Key Trade-offs

Token Bucket vs Fixed Window: TB supports bursts up to capacity; Fixed Window is simpler but has boundary effects.

In-proc vs Redis: In-proc is ultra-low latency but inconsistent across nodes; Redis adds a hop but keeps a global view.

Precision vs Cost: Floating-point tokens give smoothness but can add CPU; integer tokens are simpler.

Failure modes & mitigations

Redis down / slow → default-deny or fail-open based on product risk; add circuit-breaker & fallback to in-proc emergency bucket.

Clock skew → use server-side TIME (Redis) or monotonic clocks; never trust client timestamps.

Hot key DoS → per-IP + per-user layered policies; short local caches; backoff/ban list.

Config mistakes → versioned policies with dry-run + metrics before enforce.

Observability

Metrics:

rate_limiter_allowed_total{policy}, rate_limiter_blocked_total{policy}

decision_latency_ms, redis_roundtrip_ms, errors_total

Logs: sampled denies with key hash (not PII).

Traces: span around allow() with policy/key attributes (redacted).

Dashboards & alerts: spike in blocked_total, Redis latency > SLO.

Security & privacy

Avoid storing raw PII keys; hash keys (sha256) with a salt.

Don’t log full keys; log prefixes or hashes.

## Key Trade-offs
- ...

## Bottlenecks & Future Work
- ...

## Python Prototype
A minimal, single-process implementation lives at:

solutions/python/rate_limiter.py

Tests: tests/test_rate_limiter.py
```bash
pytest -q
```
