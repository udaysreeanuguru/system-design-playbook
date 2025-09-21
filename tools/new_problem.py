import os, sys, textwrap, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TPL = (ROOT / "templates" / "problem.md").read_text(encoding="utf-8")

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    s = s.replace(" ", "-")
    return s

def main():
    print("Create a new system-design problem scaffold\n")
    title = input("Title (e.g., Rate Limiter): ").strip()
    if not title:
        print("Title is required")
        sys.exit(1)
    proposed = slugify(title)
    slug = input(f"Slug [{proposed}]: ").strip() or proposed

    # Paths
    prob_dir = ROOT / "problems" / slug
    prob_dir.mkdir(parents=True, exist_ok=True)
    prob_md = prob_dir / "README.md"
    sol_py = ROOT / "solutions" / "python" / f"{slug.replace('-', '_')}.py"
    test_py = ROOT / "tests" / f"test_{slug.replace('-', '_')}.py"

    # Write problem doc
    content = TPL.replace("<TITLE>", title).replace("<slug>", slug)
    prob_md.write_text(content, encoding="utf-8")

    # Write python skeleton
    sol_py.parent.mkdir(parents=True, exist_ok=True)
    sol_py.write_text(textwrap.dedent(f\"\"\"
        \"\"\"Prototype for {title} ({slug}). Replace with a minimal, testable demo.\"\"\"

        def todo():
            return True
    \"\"\").lstrip(), encoding="utf-8")

    # Write test skeleton
    test_py.parent.mkdir(parents=True, exist_ok=True)
    test_py.write_text(textwrap.dedent(f\"\"\"
        def test_placeholder():
            from solutions.python.{slug.replace('-', '_')} import todo
            assert todo() is True
    \"\"\"), encoding="utf-8")

    print(f"\nCreated:\n- {prob_md}\n- {sol_py}\n- {test_py}\n")
    print("Next:\n  pip install -r requirements.txt\n  pytest -q")

if __name__ == "__main__":
    main()
