The repository is the "System Design Playbook": focused, minimal Python prototypes and writeups for system design problems.

Goal for AI agents:
- Help implement small, self-contained Python prototypes under `solutions/python/` that match the design described in `problems/<slug>/README.md`.
- Keep changes limited to the problem's files (README, solution, tests) unless the user asks for cross-cutting edits.

Quick orientation (files to read first):
- `README.md` — repo layout, quickstart, testing commands.
- `problems/<slug>/README.md` — problem statement and high-level design (use as spec).
- `solutions/python/<slug>.py` — canonical prototype (in-memory, minimal dependencies).
- `tests/test_<slug>.py` — tests express expected behavior and edge-cases to satisfy.
- `templates/problem.md` and `tools/new_problem.py` — show repo conventions for new problems.

Project-specific conventions and patterns:
- Prototypes are intentionally minimal and in-memory. Do not introduce databases or external infra unless the user asks to expand beyond the prototype.
- Use base62 helpers and id-based code generation pattern shown in `solutions/python/url_shortener.py` when implementing similar features (see `to_base62`/`from_base62`).
- Preserve the repo layout: new problems get a `problems/<slug>/README.md`, `solutions/python/<slug>.py`, and `tests/test_<slug>.py`.
- Tests are run via `pytest -q`. The CI runs Python 3.11 and installs from `requirements.txt`.

Developer workflows & commands (exact):
- Create and activate virtualenv (optional):
  - Windows: `.venv\Scripts\activate`
  - macOS/Linux: `source .venv/bin/activate`
- Install deps and run tests: `pip install -r requirements.txt; pytest -q` (CI uses the same steps).
- Scaffolding helper: `python tools/new_problem.py` prompts and creates the three canonical files for a new problem.

When editing code:
- Run and satisfy tests in `tests/` before proposing broad changes.
- Keep prototypes synchronous and dependency-free where possible (the repo prefers clarity over production wiring).
- Follow naming: module `solutions/python/<slug>.py` and tests `tests/test_<slug>.py`.

Examples to reference in edits:
- Url shortener: `solutions/python/url_shortener.py` (base62 conversion, in-memory dicts) and `tests/test_url_shortener.py` (behavioral tests).
- Template: `templates/problem.md` shows expected README sections and how to document trade-offs and capacity assumptions.

Edge cases the repo cares about (discoverable from tests and README):
- Deterministic id/code generation and idempotent shorten() behavior (same URL should return same code).
- Base62 roundtrip correctness (see `to_base62`/`from_base62` tests).

If you modify tests or add dependencies:
- Update `requirements.txt` and ensure CI still passes (CI installs requirements and runs `pytest -q` on Python 3.11).

If unsure, prefer small, test-driven changes and ask the user which problem/slug they want to work on. When creating a new problem, follow `tools/new_problem.py` conventions.

Ask the user which problem (slug) to work on or whether they want edits across multiple problems.
