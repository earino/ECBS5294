#!/usr/bin/env python3
"""Decrypt and execute every solution notebook (CI verify-solutions job).

Reads the SOLUTION_PASSWORDS environment variable: a JSON object mapping
zip basename -> password, e.g. {"solutions-hw1.zip": "..."}. In CI it
comes from a repository secret; locally you can build it from
solutions/PASSWORDS.md.

Each zip is decrypted into a temp directory laid out so the notebook's
relative data paths resolve (symlinks back into the repo), then executed
via scripts/execute_notebooks.py's machinery. Decrypted content never
leaves the temp dir; passwords are never printed.

Usage:
    SOLUTION_PASSWORDS='{"solutions-hw1.zip": "..."}' \
        uv run python scripts/ci_run_solutions.py
"""

import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# How each zip's notebook expects to find its data:
#   depth 0 + link assignments/hwN/data  -> notebook uses 'data/...'
#   depth 0 + link data                  -> notebook uses 'data/day3/...'
#   depth 1 + link data                  -> notebook uses '../data/...'
#   depth 2 + link data                  -> notebook uses '../../data/...'
LAYOUT = {
    "solutions-hw1.zip": (0, "assignments/hw1/data"),
    "solutions-hw2.zip": (0, "assignments/hw2/data"),
    "solutions-hw3.zip": (0, "data"),
    "solutions-day1-blockA.zip": (1, "data"),
    "solutions-day2-blockA.zip": (2, "data"),
    "solutions-day3-exercise.zip": (0, "data"),
}


def main() -> int:
    raw = os.environ.get("SOLUTION_PASSWORDS")
    if not raw:
        print("SOLUTION_PASSWORDS not set — nothing to verify.", file=sys.stderr)
        return 1
    passwords = json.loads(raw)

    failures = []
    for zip_name, (depth, data_target) in LAYOUT.items():
        zip_path = REPO_ROOT / "solutions" / zip_name
        if not zip_path.exists():
            failures.append(f"{zip_name}: zip missing")
            continue
        password = passwords.get(zip_name)
        if not password:
            failures.append(f"{zip_name}: no password provided")
            continue

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            nb_dir = base.joinpath(*["sub"] * depth)
            nb_dir.mkdir(parents=True, exist_ok=True)
            (base / "data").symlink_to(REPO_ROOT / data_target)

            with zipfile.ZipFile(zip_path) as zf:
                zf.setpassword(password.encode())
                for info in zf.infolist():
                    if info.filename.endswith(".ipynb"):
                        target = nb_dir / Path(info.filename).name
                        target.write_bytes(zf.read(info))

            notebooks = sorted(nb_dir.glob("*.ipynb"))
            if not notebooks:
                failures.append(f"{zip_name}: no notebook inside")
                continue
            for nb in notebooks:
                print(f"== executing {zip_name} :: {nb.name}", flush=True)
                proc = subprocess.run(
                    [sys.executable, str(REPO_ROOT / "scripts/execute_notebooks.py"), str(nb)],
                    cwd=REPO_ROOT,
                )
                if proc.returncode != 0:
                    failures.append(f"{zip_name} :: {nb.name}: execution failed")

    if failures:
        print("\nSOLUTION VERIFICATION FAILURES:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nAll solution notebooks decrypted and executed cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
