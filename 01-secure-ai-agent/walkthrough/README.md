# Walkthrough scripts: Project 1, Secure AI Agent

One bash script per part of the build, so the whole walkthrough is reproducible from the repo.
Every file the build creates is written by one of these scripts, and each script prints the
output used for that part's screenshots.

## Layout

| Script | Part | What it does |
|---|---|---|
| `part-01-prerequisites.sh` | 1 | Read-only VM checks (OS, toolchain, venv, disk, NAT). `--install` adds missing packages. |
| `part-02-vm-identity.sh` | 2 | Git identity, SSH key, GitHub registration, clone, working branch. |
| `part-03-scaffold-and-seed-data.sh` | 3 | venv, folders, support documents including the poisoned one, `app/data.py`. |
| `part-04-tools-model-logger.sh` | 4 | `app/tools.py`, the mock model, the logger, plus smoke tests. |
| `part-05-insecure-agent-and-attack.sh` | 5 | `app/agent_insecure.py`, control case, the attack, the audit trail. |

Parts 6 to 8 (hardened agent, attack runner and tests, CI) will be added as they are built.

## Usage

Run in order, from anywhere inside the repo (Parts 3 to 5 move to `01-secure-ai-agent/` themselves):

```bash
cd ~/projects/ai-security-portfolio/01-secure-ai-agent
chmod +x walkthrough/*.sh
./walkthrough/part-03-scaffold-and-seed-data.sh
./walkthrough/part-04-tools-model-logger.sh
./walkthrough/part-05-insecure-agent-and-attack.sh
```

Part 2 is the exception: run it first, before the repo exists on the machine. Copy it out of
the repo, or paste it into a file, since it does the clone.

## Notes

- Parts 3 to 5 each end with a `git commit`. Re-running a part just reports nothing to commit.
- Re-running overwrites the generated files, so don't edit them in place and then re-run.
- The scripts activate the venv themselves. Your interactive shell still needs
  `source venv/bin/activate` for commands you type by hand.
- Everything here is fictional and meant for an isolated VM. The "restricted" record is a
  placeholder, not a real secret.
