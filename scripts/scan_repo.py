"""Fail if the repository contains keys, .env files, personal email addresses, or real domains in the example.

    python scripts/scan_repo.py [repo root]

Scans the files git tracks (or every file if git is not available).
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_site import SECRET  # noqa: E402

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAINS = ("example", "example.com", "example.org", "example.net", "anthropic.com")
DOMAIN = re.compile(r"\b(?:[a-z0-9-]+\.)+(?:com|org|net|io|co|ai|dev|app|uk|ca|de)\b", re.I)
# Real domains allowed in the example: the plugin's own repo link only.
EXAMPLE_ALLOWED = {"github.com"}
TEXT = {".md", ".csv", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".py", ".sh", ".cmd", ".toml", ""}


def tracked(root):
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        return [root / p for p in out.splitlines() if p]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


def scan(root):
    root = Path(root).resolve()
    problems = []
    for path in tracked(root):
        rel = path.relative_to(root).as_posix()
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            problems.append(f"{rel}: .env files must not be committed")
            continue
        if path.suffix not in TEXT or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if SECRET.search(text):
            problems.append(f"{rel}: looks like it contains a key or password")
        for m in EMAIL.finditer(text):
            domain = m.group(0).split("@", 1)[1].lower()
            if not (domain.endswith(ALLOWED_EMAIL_DOMAINS) or domain.startswith("users.noreply.")):
                problems.append(f"{rel}: email address {m.group(0)}")
        if rel.startswith("examples/"):
            for m in DOMAIN.finditer(text):
                if m.group(0).lower() not in EXAMPLE_ALLOWED:
                    problems.append(f"{rel}: real-looking domain {m.group(0)} (use .example)")
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    problems = scan(argv[0] if argv else Path(__file__).resolve().parents[1])
    for p in problems:
        print(p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
