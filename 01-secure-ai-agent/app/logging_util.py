"""Structured tool-call logging. Every attempted call is recorded, whether it
was allowed, blocked, or held for human approval."""
from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field


@dataclass
class ToolCallLog:
    entries: list[dict] = field(default_factory=list)

    def record(self, *, agent_identity: str, tool_name: str, tool_args: dict,
               outcome: str, reason: str) -> None:
        self.entries.append({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "agent_identity": agent_identity,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "outcome": outcome,  # allowed, blocked, pending_approval, or denied
            "reason": reason,
        })

    def as_jsonl(self) -> str:
        return "\n".join(json.dumps(e) for e in self.entries)
