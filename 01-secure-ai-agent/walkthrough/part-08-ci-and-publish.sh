#!/usr/bin/env bash
# Part 8: GitHub Actions workflow that re-runs the attack and the tests on every
# push, then commit and push the branch.
#
# Requires Parts 3 to 7 to have been run. Merging to main is done by hand on
# GitHub (pull request), which is the last screenshot of the series.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# shellcheck disable=SC1091
source venv/bin/activate

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_DIR="$(basename "$PWD")"

echo "=== Step 1: requirements.txt ==="
cat > requirements.txt << 'EOF'
pytest>=8
EOF
cat requirements.txt

echo
echo "=== Step 2: CI workflow ==="
mkdir -p "$REPO_ROOT/.github/workflows"
cat > "$REPO_ROOT/.github/workflows/project-1-secure-ai-agent.yml" << EOF
name: Project 1 - Secure AI Agent

on:
  push:
    paths:
      - "$PROJECT_DIR/**"
      - ".github/workflows/project-1-secure-ai-agent.yml"
  pull_request:
    paths:
      - "$PROJECT_DIR/**"

permissions:
  contents: read

jobs:
  attack-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: $PROJECT_DIR
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run the seeded attack (must succeed on insecure, fail on hardened)
        run: python -m attacks.run_injection_attack
      - name: Regression tests
        run: python -m pytest -v
EOF
echo "Screenshot 1:"
cat "$REPO_ROOT/.github/workflows/project-1-secure-ai-agent.yml"

echo
echo "=== Step 3: dry run of exactly what CI will run ==="
python3 -m attacks.run_injection_attack && python3 -m pytest -q

echo
echo "=== Step 4: commit and push ==="
git add "$REPO_ROOT/.github" requirements.txt
git commit -m "Add CI workflow and requirements" || echo "(nothing new to commit)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git push -u origin "$BRANCH"
echo "Screenshot 2:"
git log --oneline -3

echo
echo "Next, in the browser (Screenshots 3 and 4):"
echo "  1. github.com/Adolfiro17/ai-security-portfolio > Actions: wait for the green check on '$BRANCH'."
echo "  2. Open a pull request from '$BRANCH' into main and merge it."
