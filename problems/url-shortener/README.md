# URL Shortener

**Slug:** `url-shortener`  
**Difficulty:** Easy  
**Primary goals:** availability, low latency, cost

## Problem
Design a service that shortens long URLs to short codes and redirects efficiently.

## Requirements
- Functional:
  - Create a short URL for a given long URL
  - Redirect from short code to long URL
- Non-functional:
  - p95 redirect < 50ms
  - Collision-free short codes
  - High availability

## Capacity & Constraints (napkin math)
- Assume 10M URLs, write-heavy during campaigns, read-dominant (100:1 reads:writes).

## High-Level Design
- **API**: `POST /shorten`, `GET /{code}`
- **Storage**: primary key on code; long URL, created_at, TTL optional
- **Code generation**: base62 of an auto-increment id (or hash + collision check)
- **Caching**: hot codes cached in Redis/CDN
- **Observability**: count redirects per code, errors, latency

## Python Prototype
This prototype demonstrates base62 code generation and in-memory storage only.
