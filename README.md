# System Design Playbook

A clean, repeatable structure to capture **system design problems** with a brief problem statement, high‑level design, and a small **Python prototype** + tests.

## Structure
```
.
├── problems/
│   └── url-shortener/
│       └── README.md
├── solutions/
│   └── python/
│       └── url_shortener.py
├── tests/
│   └── test_url_shortener.py
├── templates/
│   └── problem.md
├── tools/
│   └── new_problem.py
├── requirements.txt
├── .gitignore
└── .github/workflows/ci.yml
```
- Write the full system-design thinking in `problems/<slug>/README.md` (use `templates/problem.md`).
- Put Python prototype(s) in `solutions/python/<slug>.py`.
- Add tests in `tests/test_<slug>.py`.

## Quickstart
```bash
# (optional) create a venv
python -m venv .venv
# activate:
#   Windows: .venv\Scripts\activate
#   macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt

# run tests
pytest -q
```

## Add a new problem
Use the helper (it scaffolds problem docs, a Python file, and a test):
```bash
python tools/new_problem.py
# then follow the prompts (e.g., "rate-limiter", "Rate Limiter")
pytest -q
```

---

Happy building! 🚀
