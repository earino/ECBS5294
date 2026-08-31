#!/bin/bash
#
# Setup Git Hooks for ECBS5294
#
# This script installs the pre-commit hook that:
# 1. Clears outputs from Jupyter notebooks
# 2. Validates notebook format (nbformat 4.5 with cell IDs)
# 3. Prevents accidental commits of unencrypted solution files
#
# Usage: ./scripts/setup_hooks.sh
#

set -e

echo "Setting up git hooks for ECBS5294..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "   Run this script from the repository root"
    exit 1
fi

# Install the tracked hook from scripts/pre-commit
if [ ! -f "scripts/pre-commit" ]; then
    echo "❌ Error: Hook source not found at scripts/pre-commit"
    exit 1
fi

cp scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed and activated"
echo ""
echo "What this hook does:"
echo "  1️⃣  Clears outputs from Jupyter notebooks automatically"
echo "  2️⃣  Validates notebook format (nbformat 4.5 with unique cell IDs)"
echo "  3️⃣  Blocks commits of unencrypted solution files (*_solution.ipynb, *_solution.py)"
echo "  3️⃣  Allows commits of encrypted solutions-*.zip files"
echo "  3️⃣  Verifies ZIP files are password-protected"
echo ""
echo "To test the hook:"
echo "  1. Try to commit a solution file (will be blocked):"
echo "     touch test_solution.ipynb"
echo "     git add test_solution.ipynb"
echo "     git commit -m \"test\" "
echo "     # Should be blocked!"
echo ""
echo "  2. Check solution status:"
echo "     uv run python scripts/list_solutions.py"
echo ""
echo "✅ Setup complete!"
