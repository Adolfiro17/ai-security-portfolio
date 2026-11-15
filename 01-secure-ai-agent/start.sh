#!/usr/bin/env bash
# One command to run Project 1. No API key, no network after install, no cloud account.
#
#   ./start.sh            run the tests, the seeded attack and the guided challenges
#   ./start.sh test       tests only
#   ./start.sh attack     seeded attack only
#   ./start.sh lab [N]    guided challenges (list, one, or "all")
#   ./start.sh site       serve the course site at http://localhost:8000
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  "$PY" -m venv .venv 2>/dev/null || {
    echo "Could not create a virtual environment."
    echo "On Debian/Ubuntu run: sudo apt update && sudo apt install -y python3-venv"
    exit 1
  }
fi
# shellcheck disable=SC1091
. .venv/bin/activate
pip install -q -r requirements.txt

cmd="${1:-demo}"
[ "$#" -gt 0 ] && shift
case "$cmd" in
  demo)   python -m pytest -q && python -m attacks.run_injection_attack && python -m lab.challenges all ;;
  test)   python -m pytest -q ;;
  attack) python -m attacks.run_injection_attack ;;
  lab)    python -m lab.challenges "$@" ;;
  site)   echo "Serving http://localhost:8000 (Ctrl+C to stop)"; python -m http.server 8000 --directory ../docs ;;
  *)      echo "Unknown command: $cmd"; exit 1 ;;
esac
