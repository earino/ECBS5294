#!/usr/bin/env python3
"""Verify solution archives leak nothing.

Two checks:
1. Every entry of every solutions/*.zip has the ZIP encryption flag set —
   a plaintext entry means the solution is readable with a bare unzip
   (this exact leak shipped once; see solutions-hw2.zip history).
2. No unencrypted solution file (*_solution.ipynb / *_solution.py) is
   tracked by git.

Usage:
    uv run python scripts/check_solution_zips.py
"""

import glob
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    failures = []

    for zip_path in sorted(glob.glob(str(REPO_ROOT / "solutions" / "*.zip"))):
        rel = Path(zip_path).relative_to(REPO_ROOT)
        entries = zipfile.ZipFile(zip_path).infolist()
        plaintext = [i.filename for i in entries if not (i.flag_bits & 0x1)]
        if plaintext:
            failures.append(f"{rel}: PLAINTEXT entries {plaintext}")
        else:
            print(f"OK {rel} ({len(entries)} encrypted entries)")

    tracked = subprocess.run(
        ["git", "ls-files", "*_solution.ipynb", "*_solution.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout.split()
    if tracked:
        failures.append(f"unencrypted solution files tracked by git: {tracked}")

    if failures:
        print("\nSOLUTION LEAKS DETECTED:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nAll solution archives fully encrypted; no solution files tracked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
