# Rate Limiter

**Slug:** `rate-limiter`  
**Difficulty:** Easy / Medium / Hard  
**Primary goals:** scalability, availability, latency, cost, consistency

## Problem
Briefly describe the problem in 1–3 sentences.

## Requirements
- Functional:
  - ...
- Non-functional:
  - ...

## Capacity & Constraints (back-of-the-envelope)
- Daily active users / QPS / peak
- Storage estimates (hot vs cold)
- Latency SLOs / tail (p95/p99)

## High-Level Design
- Architecture diagram (describe components & data flow)
- API design (endpoints, payloads, status codes)
- Data model (schemas, keys, indexes)
- Scaling plan (sharding, caching, async, queues)
- Consistency model & failure handling
- Observability (metrics, logs, traces, alerts)

## Key Trade-offs
- ...

## Bottlenecks & Future Work
- ...

## Python Prototype
Explain what the prototype demonstrates, limitations, and how to run it.

```bash
pytest -q
```
