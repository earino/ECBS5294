#!/usr/bin/env python3
"""Lightweight documentation consistency checks.

1. Year-date policy: 4-digit years (20xx) may appear only in syllabus.md
   (repo policy: materials stay evergreen; the syllabus is refreshed each
   term). Dataset facts and code are exempt via the allowlist below.
2. Dead references: repo-relative file paths mentioned in markdown must
   exist on disk.

Usage:
    uv run python scripts/check_doc_consistency.py
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files/directories whose purpose involves dates: the syllabus (term
# dates by policy), data docs (describe actual dataset content), and
# reference material citing publications or examples.
YEAR_EXEMPT_PREFIXES = (
    "syllabus.md",
    "data/",                # dataset docs state real date ranges/fetch dates
    "assignments/hw1/README.md",   # dataset covers Dec 2009 - Dec 2010
    "assignments/hw2/README.md",   # dataset review-date span
    "solutions/PASSWORD_SAFETY_SYSTEM.md",
    "references/README_INSTRUCTOR_MATERIALS.md",
    "references/papers/",   # publication years
    "references/datasets/", # dataset update notes
    "interviews/",          # practice-question content
    "CLAUDE-EXTENDED.md",   # cites nbformat history and anti-example dates
)

# Substrings that make a year mention acceptable anywhere (dataset facts,
# library versions, URLs, teaching examples of untidy columns).
YEAR_CONTEXT_ALLOW = re.compile(
    r"(20\d\d-\d\d|\d\d/\d\d/20\d\d|copyright|©|https?://|ISO|dummyjson"
    r"|2009|2010|1989|2222|2024|2025-0|Jan(uary)? 2024|Jun(e)? 2025|H1 2024|H2 2024|H1 2025"
    r"|`20\d\d`)",  # years in backticks are column-name examples, not dates
    re.IGNORECASE,
)

PATH_RE = re.compile(r"`((?:data|scripts|notebooks|assignments|references|solutions)/[A-Za-z0-9_\-./{}*\[\]]+)`")

# Paths that are deliberately gitignored (instructor-local files): they
# exist on the instructor's machine but never in a fresh checkout, so
# docs may legitimately reference them.
LOCAL_ONLY_PREFIXES = (
    "solutions/PASSWORDS.md",
    "solutions/.password_backup.json",
    "solutions/.encryption_log.txt",
    "solutions/decrypted",
    "references/teaching",  # moved to the private instructor repo; the pointer README names it
    "assignments/final_exam",
)


def tracked_markdown() -> list[str]:
    out = subprocess.run(["git", "ls-files", "*.md"], capture_output=True,
                         text=True, cwd=REPO_ROOT).stdout.split()
    return out


def main() -> int:
    failures = []

    for rel in tracked_markdown():
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")

        if not rel.startswith(YEAR_EXEMPT_PREFIXES):
            for n, line in enumerate(text.splitlines(), 1):
                for m in re.finditer(r"\b20\d\d\b", line):
                    if YEAR_CONTEXT_ALLOW.search(line):
                        continue
                    failures.append(f"{rel}:{n}: year '{m.group()}' outside syllabus.md — {line.strip()[:80]}")

        for n, line in enumerate(text.splitlines(), 1):
            for m in PATH_RE.finditer(line):
                ref = m.group(1)
                # skip glob/template/placeholder patterns and ellipses
                if any(ch in ref for ch in "*{}[]") or "..." in ref \
                        or re.search(r"(hw|day)N\b|file\.csv|your_", ref):
                    continue
                if ref.rstrip("/").startswith(LOCAL_ONLY_PREFIXES):
                    continue
                # a path may be repo-root-relative OR relative to the doc
                if not (REPO_ROOT / ref).exists() \
                        and not ((REPO_ROOT / rel).parent / ref).exists():
                    failures.append(f"{rel}:{n}: references missing file `{ref}`")

    if failures:
        print("DOC CONSISTENCY FAILURES:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"Doc consistency OK across {len(tracked_markdown())} markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
