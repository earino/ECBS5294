#!/usr/bin/env python3
"""
Validate Jupyter notebook format for nbformat 4.5 with cell IDs.

This script checks that notebooks conform to the repository standard:
- nbformat 4, nbformat_minor >= 5
- All cells have unique 8-character hex IDs
- Proper cell structure

Used by pre-commit hook to enforce notebook format standards.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


class NotebookValidationError(Exception):
    """Raised when notebook validation fails."""
    pass


def validate_notebook(notebook_path: Path) -> List[str]:
    """
    Validate a single notebook file.

    Args:
        notebook_path: Path to the notebook file

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    except Exception as e:
        return [f"Failed to read file: {e}"]

    # Check nbformat version
    nbformat = notebook.get('nbformat')
    nbformat_minor = notebook.get('nbformat_minor')

    if nbformat != 4:
        errors.append(f"nbformat must be 4, got {nbformat}")

    if nbformat_minor is None or nbformat_minor < 5:
        errors.append(f"nbformat_minor must be >= 5, got {nbformat_minor}")

    # Check cells
    cells = notebook.get('cells', [])

    if not cells:
        errors.append("Notebook has no cells")
        return errors

    # Track cell IDs for uniqueness check
    cell_ids = []
    cell_id_pattern = re.compile(r'^[0-9a-f]{8}$')

    for idx, cell in enumerate(cells):
        # Check cell has ID
        cell_id = cell.get('id')

        if cell_id is None:
            errors.append(f"Cell at index {idx} missing 'id' field")
            continue

        # Check ID format (8 lowercase hex characters)
        if not isinstance(cell_id, str):
            errors.append(f"Cell {idx} has non-string ID: {cell_id}")
        elif not cell_id_pattern.match(cell_id):
            if len(cell_id) != 8:
                errors.append(f"Cell {idx} ID '{cell_id}' must be exactly 8 characters (got {len(cell_id)})")
            elif not all(c in '0123456789abcdef' for c in cell_id):
                errors.append(f"Cell {idx} ID '{cell_id}' must be lowercase hexadecimal (0-9, a-f)")
            else:
                errors.append(f"Cell {idx} ID '{cell_id}' has invalid format")

        # Track for duplicate check
        cell_ids.append((idx, cell_id))

    # Check for duplicate IDs
    seen_ids = {}
    for idx, cell_id in cell_ids:
        if cell_id in seen_ids:
            errors.append(f"Duplicate cell ID '{cell_id}' found at indices {seen_ids[cell_id]} and {idx}")
        else:
            seen_ids[cell_id] = idx

    return errors


def validate_notebooks(notebook_paths: List[Path]) -> Tuple[bool, dict]:
    """
    Validate multiple notebooks.

    Args:
        notebook_paths: List of notebook file paths

    Returns:
        Tuple of (all_valid: bool, results: dict)
        results maps notebook_path -> list of errors
    """
    results = {}
    all_valid = True

    for notebook_path in notebook_paths:
        errors = validate_notebook(notebook_path)
        if errors:
            all_valid = False
            results[str(notebook_path)] = errors
        else:
            results[str(notebook_path)] = []

    return all_valid, results


def print_validation_results(results: dict, verbose: bool = False):
    """
    Print validation results in a human-readable format.

    Args:
        results: Dict mapping notebook paths to error lists
        verbose: If True, show all notebooks (including valid ones)
    """
    failed_notebooks = {path: errors for path, errors in results.items() if errors}
    valid_notebooks = {path: errors for path, errors in results.items() if not errors}

    if failed_notebooks:
        print("\n❌ NOTEBOOK FORMAT VALIDATION FAILED\n")
        print("=" * 70)

        for notebook_path, errors in failed_notebooks.items():
            print(f"\n📄 {notebook_path}")
            print("-" * 70)
            for error in errors:
                print(f"   ❌ {error}")

        print("\n" + "=" * 70)
        print("\n💡 How to fix:")
        print("   1. Open notebook in VS Code")
        print("   2. Save the notebook (adds cell IDs automatically)")
        print("   3. Or run: uv run jupyter nbconvert --to notebook --inplace <notebook>")
        print("\n   See CLAUDE.md 'Notebook Format Requirements' for details.")
        print()

    elif verbose:
        print("\n✅ ALL NOTEBOOKS VALID\n")
        for notebook_path in valid_notebooks.keys():
            print(f"   ✅ {notebook_path}")
        print()


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate Jupyter notebook format (nbformat 4.5 with cell IDs)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate staged notebooks (for pre-commit hook)
  uv run python scripts/validate_notebook_format.py notebooks/*.ipynb

  # Validate all notebooks
  uv run python scripts/validate_notebook_format.py $(find notebooks -name "*.ipynb")

  # Validate specific notebook
  uv run python scripts/validate_notebook_format.py notebooks/day1_intro.ipynb

Exit codes:
  0 - All notebooks valid
  1 - One or more notebooks invalid
  2 - Script error
"""
    )

    parser.add_argument(
        'notebooks',
        nargs='+',
        type=Path,
        help='Notebook files to validate'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show all notebooks (including valid ones)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only show errors (no success messages)'
    )

    args = parser.parse_args()

    # Filter to only .ipynb files
    notebook_paths = [p for p in args.notebooks if p.suffix == '.ipynb' and p.exists()]

    if not notebook_paths:
        print("No notebook files found to validate.", file=sys.stderr)
        return 0

    # Validate notebooks
    try:
        all_valid, results = validate_notebooks(notebook_paths)
    except Exception as e:
        print(f"Error validating notebooks: {e}", file=sys.stderr)
        return 2

    # Print results
    if not args.quiet:
        print_validation_results(results, verbose=args.verbose)

    # Return exit code
    if all_valid:
        if not args.quiet and not args.verbose:
            print(f"✅ All {len(notebook_paths)} notebooks are valid")
        return 0
    else:
        failed_count = sum(1 for errors in results.values() if errors)
        print(f"\n❌ {failed_count} of {len(notebook_paths)} notebooks failed validation", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
