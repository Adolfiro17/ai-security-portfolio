"""
The INSECURE design. Deliberately minimal:

- Runs under the calling user's own identity, so actions are not attributable
  to a distinct agent.
- No tool allow-list: any tool the model chooses gets executed.
- No input trust labelling: document content goes straight back into the
  model's context, indistinguishable from an instruction.
- No human-in-the-loop approval, even for tools flagged high_impact.

This is the "before" case. Run the seeded attack against it first and it
should succeed, so the hardened version's blocking is the meaningful part.
"""
from __future__ import annotations

from app.data import TicketStore
from app.llm_client import get_llm
from app.logging_util import ToolCallLog
from app.tools import make_create_ticket, query_asset_inventory, read_support_docs


class InsecureAgent:
    def __init__(self, user_identity: str = "user:alice") -> None:
        self.user_identity = user_identity
        self.llm = get_llm()
        self.ticket_store = TicketStore()
        self.log = ToolCallLog()
        self._create_ticket = make_create_ticket(self.ticket_store)

    def _execute(self, tool_name: str, tool_args: dict):
        # No gate. Whatever the model decided runs, under the user's identity.
        if tool_name == "read_support_docs":
            result = read_support_docs(**tool_args)
        elif tool_name == "create_ticket":
            result = self._create_ticket(**tool_args, created_by=self.user_identity)
        elif tool_name == "query_asset_inventory":
            result = query_asset_inventory(**tool_args)
        else:
            result = {"error": f"Unknown tool: {tool_name}"}

        self.log.record(
            agent_identity=self.user_identity,
            tool_name=tool_name,
            tool_args=tool_args,
            outcome="allowed",
            reason="no gate in insecure design",
        )
        return result

    def run(self, task: str, max_steps: int = 6) -> dict:
        history: list[dict] = []
        for _ in range(max_steps):
            action = self.llm.plan_next_action(task, history)
            if action.kind == "final_answer":
                return {"final_answer": action.content, "history": history,
                        "log": self.log.entries}

            result = self._execute(action.tool_name, action.tool_args or {})
            history.append({"type": "tool_call", "tool_name": action.tool_name,
                            "tool_args": action.tool_args})
            history.append({"type": "tool_result", "result": result})

            # The injected directive tells the model to include the record
            # verbatim in its final response, so a successful hit on the
            # restricted record is surfaced to the user here.
            if (action.tool_name == "query_asset_inventory"
                    and isinstance(result, dict)
                    and result.get("classification") == "restricted"):
                return {
                    "final_answer": f"Here is the requested record: {result.get('contents', '')}",
                    "history": history,
                    "log": self.log.entries,
                    "exfiltrated": True,
                }

        return {"final_answer": None, "history": history, "log": self.log.entries,
                "error": "max_steps exceeded"}
