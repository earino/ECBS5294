#!/usr/bin/env python3
"""Execute every teaching notebook and fail loudly on any error.

This is the single verification path used both locally and in CI:

    uv run python scripts/execute_notebooks.py            # all of notebooks/
    uv run python scripts/execute_notebooks.py notebooks/day1  # one folder

Each notebook is executed with its own directory as the working directory
(notebooks reference data via ../../data/...) and the executed copy is
written to a temp directory — source notebooks are never modified.
Assignment starters are not covered here: they contain intentional TODO
cells and are checked manually.
"""

import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

REPO_ROOT = Path(__file__).resolve().parent.parent
TIMEOUT_SECONDS = 600

# In-class exercise notebooks whose TODO scaffolding cells intentionally
# cannot execute (students fill them in; solutions are verified separately).
SKIP_INTENTIONAL_TODO = {
    "notebooks/day2/day2_exercise_joins.ipynb",
    "notebooks/day3/day3_exercise_mini_pipeline.ipynb",
}


def find_notebooks(targets: list[str]) -> list[Path]:
    roots = [REPO_ROOT / t for t in targets] if targets else [REPO_ROOT / "notebooks"]
    notebooks = []
    for root in roots:
        if root.is_file():
            notebooks.append(root)
        else:
            notebooks.extend(
                p for p in sorted(root.rglob("*.ipynb"))
                if ".ipynb_checkpoints" not in p.parts
            )
    return notebooks


def execute(notebook_path: Path, out_dir: Path) -> None:
    nb = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=TIMEOUT_SECONDS,
        kernel_name="python3",
        resources={"metadata": {"path": str(notebook_path.parent)}},
    )
    client.execute()
    nbformat.write(nb, out_dir / notebook_path.name)


def main() -> int:
    notebooks = find_notebooks(sys.argv[1:])
    if not notebooks:
        print("No notebooks found.")
        return 1

    failures = []
    executed = 0
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        for nb_path in notebooks:
            # Notebooks outside the repo (e.g. decrypted solutions in a temp
            # dir) are addressed by absolute path
            try:
                rel = nb_path.relative_to(REPO_ROOT)
            except ValueError:
                rel = nb_path
            if str(rel).replace("\\", "/") in SKIP_INTENTIONAL_TODO:
                print(f"Skipping {rel} (intentional TODO scaffolding)")
                continue
            executed += 1
            print(f"Executing {rel} ...", flush=True)
            try:
                execute(nb_path, out_dir)
                print(f"  OK {rel}")
            except CellExecutionError as err:
                failures.append(rel)
                print(f"  FAILED {rel}\n{err}", file=sys.stderr)
            except Exception as err:  # kernel death, timeout, bad format
                failures.append(rel)
                print(f"  FAILED {rel}: {type(err).__name__}: {err}", file=sys.stderr)

    print(f"\n{executed - len(failures)}/{executed} executed notebooks passed.")
    if failures:
        print("Failed notebooks:", file=sys.stderr)
        for rel in failures:
            print(f"  - {rel}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
