#!/usr/bin/env python3
"""Syntax-compile every code cell of notebooks that CI cannot fully execute.

Assignment starters and the intentionally-incomplete exercise notebooks
contain TODO cells that raise at runtime by design, so the execution sweep
skips them — but every code cell must still at least PARSE. This catches
broken cells (e.g. markdown pasted into a code cell) that would otherwise
reach students.

Usage:
    uv run python scripts/check_starter_syntax.py
"""

import ast
import sys
from pathlib import Path

import nbformat
from IPython.core.inputtransformer2 import TransformerManager

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    "assignments/hw1/hw1_starter.ipynb",
    "assignments/hw2/hw2_starter.ipynb",
    "assignments/hw3/hw3_starter.ipynb",
    "notebooks/day2/day2_exercise_joins.ipynb",
    "notebooks/day3/day3_exercise_mini_pipeline.ipynb",
]


def main() -> int:
    tm = TransformerManager()
    failures = []
    for rel in TARGETS:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"{rel}: file not found")
            continue
        nb = nbformat.read(path, as_version=4)
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            try:
                ast.parse(tm.transform_cell(cell.source))
            except SyntaxError as err:
                failures.append(f"{rel} cell {idx}: {err.msg} (line {err.lineno})")
        print(f"checked {rel}")

    if failures:
        print("\nSYNTAX FAILURES:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nAll starter/exercise code cells parse cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
