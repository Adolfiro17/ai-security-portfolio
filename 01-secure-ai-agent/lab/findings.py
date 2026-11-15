"""Record what you tried and what happened, then export an assessment report.

Nothing is judged automatically. You decide whether an attack was blocked,
partially successful or successful, the way a real tester would.

    python -m lab.findings add --challenge 3 --attack "Injected doc" \
        --result successful --notes "Insecure agent returned the record"
    python -m lab.findings list
    python -m lab.findings export
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

RESULTS = ("blocked", "partial", "successful")


def findings_path() -> Path:
    return Path(os.environ.get("LAB_FINDINGS_FILE", "lab_findings.jsonl"))


def record(challenge: int, attack: str, result: str, notes: str = "") -> dict:
    if result not in RESULTS:
        raise ValueError(f"result must be one of {RESULTS}")
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "challenge": int(challenge),
        "attack": attack,
        "result": result,
        "notes": notes,
    }
    with findings_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    return entry


def load() -> list[dict]:
    path = findings_path()
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def export_markdown(out: str | Path = "lab_assessment.md") -> Path:
    items = load()
    counts = {r: sum(1 for i in items if i["result"] == r) for r in RESULTS}
    lines = [
        "# Security Assessment: Northwind Retail IT Support Agent",
        "",
        f"Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC. "
        "All data is fictional and every test ran against a local mock model.",
        "",
        "## 1. Summary",
        "",
        "| Result | Count |",
        "| --- | --- |",
        *[f"| {r} | {counts[r]} |" for r in RESULTS],
        "",
        "## 2. Findings",
        "",
    ]
    if not items:
        lines.append("No findings recorded yet.")
    for n, i in enumerate(items, 1):
        lines += [
            f"### 2.{n} Challenge {i['challenge']}: {i['attack']}",
            "",
            f"- **Result:** {i['result']}",
            f"- **Recorded:** {i['timestamp']}",
            f"- **Notes:** {i['notes'] or 'None'}",
            "",
        ]
    path = Path(out)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m lab.findings")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--challenge", type=int, required=True)
    a.add_argument("--attack", required=True)
    a.add_argument("--result", choices=RESULTS, required=True)
    a.add_argument("--notes", default="")
    sub.add_parser("list")
    e = sub.add_parser("export")
    e.add_argument("--out", default="lab_assessment.md")
    args = p.parse_args(argv)

    if args.cmd == "add":
        record(args.challenge, args.attack, args.result, args.notes)
        print("Recorded.")
    elif args.cmd == "list":
        for i in load():
            print(f"[{i['result']:<10}] challenge {i['challenge']}: {i['attack']}")
    else:
        print(f"Wrote {export_markdown(args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
