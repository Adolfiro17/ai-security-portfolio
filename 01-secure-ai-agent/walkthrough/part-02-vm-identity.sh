#!/usr/bin/env bash
# Part 2: give the VM its own identity with GitHub, clone the repo, and
# prepare a clean working branch.
#
# Unlike Parts 3-5, run this one from anywhere, BEFORE you have the repo.
# (If you already cloned, the clone step is skipped.)
#
# Interactive steps: ssh-keygen asks for a passphrase, and GitHub needs the
# public key registered by hand in a browser (the script pauses for that).
set -euo pipefail

GIT_NAME="Adolf Sey"
GIT_EMAIL="adolfiro2030@gmail.com"
REPO_SSH="git@github.com:Adolfiro17/ai-security-portfolio.git"
BRANCH="build-project-1-by-hand"

echo "=== Step 1: git identity ==="
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
git config --global --list | grep user      # Screenshot 1
echo

echo "=== Step 2: SSH key pair ==="
KEY="$HOME/.ssh/id_ed25519"
if [[ -f "$KEY" ]]; then
  echo "Key already exists at $KEY, not overwriting."
else
  ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$KEY"   # Screenshot 2
fi
echo

echo "=== Step 3: public key (safe to share; NEVER print the file without .pub) ==="
cat "$KEY.pub"                                       # Screenshot 3 (crop it)
echo
echo "Add this at https://github.com/settings/keys"
echo "  Title: eden-vmware-lab   Type: Authentication Key"
read -r -p "Press Enter once the key is registered on GitHub... " _
echo

echo "=== Step 4: test authentication ==="
# ssh -T exits with status 1 even on success, so don't let set -e stop us.
ssh -o StrictHostKeyChecking=accept-new -T git@github.com || true   # Screenshot 5
echo

echo "=== Step 5: clone the repository ==="
mkdir -p "$HOME/projects"
cd "$HOME/projects"
if [[ -d ai-security-portfolio/.git ]]; then
  echo "Repo already cloned, skipping."
else
  git clone "$REPO_SSH"                              # Screenshot 6
fi
cd ai-security-portfolio
ls
git log --oneline | head -5
echo

echo "=== Step 6: clean slate on a working branch ==="
echo "This keeps a reference copy of the finished scaffold at"
echo "~/projects/reference-project-1, then DELETES these from 01-secure-ai-agent/:"
echo "  app attacks tests data requirements.txt .env.example"
read -r -p "Continue? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  if [[ ! -d "$HOME/projects/reference-project-1" ]]; then
    cp -r 01-secure-ai-agent "$HOME/projects/reference-project-1"
  fi
  git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
  cd 01-secure-ai-agent
  rm -rf app attacks tests data requirements.txt .env.example
  git branch                                         # Screenshot 7
  ls -a
else
  echo "Skipped. Nothing was deleted."
fi
