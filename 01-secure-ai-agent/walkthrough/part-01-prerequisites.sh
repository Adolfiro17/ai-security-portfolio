#!/usr/bin/env bash
# Part 1: verify the VM meets the prerequisites for Project 1.
# Read-only checks, safe to run any time. Run `clear` between commands if you
# are taking one screenshot per check.
#
# Optional: pass --install to install missing packages (git, pip, venv).
set -uo pipefail

if [[ "${1:-}" == "--install" ]]; then
  echo ">> Installing prerequisites (needs sudo)"
  sudo apt update
  # python3-venv is required: on Debian/Ubuntu the venv module exists without
  # ensurepip, so `python3 -m venv --help` can pass while venv creation fails.
  sudo apt install -y git python3-pip python3-venv
  echo
fi

echo "=== Screenshot 1: VM identity ==="
hostnamectl | grep -E "Static hostname|Operating System|Kernel|Virtualization"
echo

echo "=== Screenshot 2: toolchain (Python needs 3.10+) ==="
python3 --version && git --version && pip3 --version
echo

echo "=== Screenshot 3: venv module and free disk space ==="
if python3 -m venv --help > /dev/null 2>&1; then echo "venv module: OK"; else echo "venv module: MISSING"; fi
# Real test: venv creation needs ensurepip, which --help does not exercise.
tmp="$(mktemp -d)"
if python3 -m venv "$tmp/probe" > /dev/null 2>&1; then
  echo "venv creation: OK"
else
  echo "venv creation: FAILED (run: ./part-01-prerequisites.sh --install)"
fi
rm -rf "$tmp"
df -h /
echo

echo "=== Screenshot 4: network isolation (gateway ending in .2 = VMware NAT) ==="
ip a | grep "inet "
ip route | grep default
