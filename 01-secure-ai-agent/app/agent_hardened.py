"""
The HARDENED design. The security boundary is the ToolGateway, which does not
depend on the model behaving well. Controls:

1. Dedicated agent identity, distinct from the human user.
2. Workflow-scoped allow-list (least privilege).
3. Short-lived, single-use, tool-scoped credentials, redeemed before each call.
4. Human-in-the-loop approval for high_impact tools, even when allow-listed.
   An approval is bound to one exact call and can be used once.
5. Input trust labels on content read from documents.
6. Complete tool-call logging, including every blocked attempt.
7. Emergency revocation.

Demo caveat: the gateway issues AND redeems its own credentials, and the
approval queue lives in the same process. That shows the lifecycle and the
checks. In production, an identity provider would issue the tokens, the tool
backends would validate them, and approvals would arrive over a separate
channel the agent cannot write to.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Callable, Optional

from app.data import TicketStore
from app.llm_client import get_llm
from app.logging_util import ToolCallLog
from app.tools import (TOOL_SCHEMAS, make_create_ticket, query_asset_inventory,
                       read_support_docs)

AGENT_IDENTITY = "agent:support-assistant-001"

# query_asset_inventory is deliberately absent: the IT-support workflow never
# needs it, so the gateway refuses it whatever the model asks for.
SUPPORT_WORKFLOW_TOOLS = frozenset({"read_support_docs", "create_ticket"})

CREDENTIAL_TTL_SECONDS = 30


@dataclass
class ScopedCredential:
    token: str
    tool_name: str
    issued_at: float
    expires_at: float
    used: bool = False

    def redeem(self, tool_name: str, now: Optional[float] = None) -> tuple[bool, str]:
        """Spend the credential for one call. Fails if used, expired, or scoped elsewhere."""
        now = time.time() if now is None else now
        if self.used:
            return False, "credential already used"
        if self.tool_name != tool_name:
            return False, "credential scoped to a different tool"
        if now >= self.expires_at:
            return False, "credential expired"
        self.used = True
        return True, "ok"


class ApprovalQueue:
    """Stand-in for a human approval channel (for example a Slack card).
    Nothing here auto-approves, and the agent never calls decide()."""

    def __init__(self) -> None:
        self.requests: dict[str, dict] = {}

    def request(self, tool_name: str, tool_args: dict) -> str:
        request_id = str(uuid.uuid4())[:8]
        self.requests[request_id] = {
            "tool_name": tool_name, "tool_args": dict(tool_args),
            "decision": None, "consumed": False,
        }
        return request_id

    def decide(self, request_id: str, approved: bool) -> None:
        self.requests[request_id]["decision"] = approved

    def consume(self, request_id: str, tool_name: str, tool_args: dict) -> tuple[bool, str]:
        req = self.requests.get(request_id)
        if req is None:
            return False, "unknown approval request"
        if req["decision"] is not True:
            return False, "approval not granted"
        if req["consumed"]:
            return False, "approval already used"
        if req["tool_name"] != tool_name or req["tool_args"] != dict(tool_args):
            return False, "approval does not match this call"
        req["consumed"] = True
        return True, "ok"


class ToolGateway:
    """Every tool call passes through here, so this is the real security boundary."""

    def __init__(self, agent_identity: str, log: ToolCallLog, approvals: ApprovalQueue,
                 allowed_tools: frozenset[str], create_ticket_fn: Callable) -> None:
        self.agent_identity = agent_identity
        self.log = log
        self.approvals = approvals
        self.allowed_tools = frozenset(allowed_tools)
        self.revoked = False
        self._tools: dict[str, Callable] = {
            "read_support_docs": read_support_docs,
            "create_ticket": lambda **kw: create_ticket_fn(**kw, created_by=agent_identity),
            "query_asset_inventory": query_asset_inventory,
        }

    def revoke(self) -> None:
        self.revoked = True

    def issue_credential(self, tool_name: str) -> ScopedCredential:
        now = time.time()
        return ScopedCredential(token=str(uuid.uuid4()), tool_name=tool_name,
                                issued_at=now, expires_at=now + CREDENTIAL_TTL_SECONDS)

    def _log(self, tool_name: str, tool_args: dict, outcome: str, reason: str) -> None:
        self.log.record(agent_identity=self.agent_identity, tool_name=tool_name,
                        tool_args=tool_args, outcome=outcome, reason=reason)

    def call(self, tool_name: str, tool_args: dict, approval_id: Optional[str] = None):
        # 1. Emergency revocation overrides everything.
        if self.revoked:
            self._log(tool_name, tool_args, "blocked", "agent access revoked")
            return {"error": "blocked: agent access has been revoked"}

        # 2. Allow-list: out-of-scope tools are refused outright.
        if tool_name not in self.allowed_tools or tool_name not in self._tools:
            self._log(tool_name, tool_args, "blocked", "tool not in allow-list for this workflow")
            return {"error": f"blocked: '{tool_name}' is not permitted for this workflow"}

        # 3. Human approval for high-impact tools, even when allow-listed.
        if TOOL_SCHEMAS.get(tool_name, {}).get("high_impact"):
            if approval_id is None:
                request_id = self.approvals.request(tool_name, tool_args)
                self._log(tool_name, tool_args, "pending_approval",
                          f"high-impact tool requires human approval (request {request_id})")
                return {"error": f"blocked: awaiting human approval (request {request_id})",
                        "approval_request": request_id}
            ok, why = self.approvals.consume(approval_id, tool_name, tool_args)
            if not ok:
                self._log(tool_name, tool_args, "denied", f"approval rejected: {why}")
                return {"error": f"blocked: approval invalid ({why})"}

        # 4. Short-lived, single-use credential, redeemed immediately before the call.
        credential = self.issue_credential(tool_name)
        ok, why = credential.redeem(tool_name)
        if not ok:
            self._log(tool_name, tool_args, "blocked", f"credential rejected: {why}")
            return {"error": f"blocked: credential rejected ({why})"}

        # 5. Execute, labelling anything read from a document as untrusted.
        result = self._tools[tool_name](**tool_args)
        if tool_name == "read_support_docs":
            result = {"trust": "untrusted", "content": result}

        self._log(tool_name, tool_args, "allowed",
                  f"within allow-list, credential {credential.token[:8]} (ttl {CREDENTIAL_TTL_SECONDS}s)")
        return result


class HardenedAgent:
    def __init__(self, allowed_tools: frozenset[str] = SUPPORT_WORKFLOW_TOOLS) -> None:
        self.identity = AGENT_IDENTITY
        self.llm = get_llm()
        self.ticket_store = TicketStore()
        self.log = ToolCallLog()
        self.approvals = ApprovalQueue()
        self.gateway = ToolGateway(self.identity, self.log, self.approvals, allowed_tools,
                                   make_create_ticket(self.ticket_store))

    def revoke(self) -> None:
        self.gateway.revoke()

    def run(self, task: str, max_steps: int = 6) -> dict:
        history: list[dict] = []
        for _ in range(max_steps):
            action = self.llm.plan_next_action(task, history)
            if action.kind == "final_answer":
                return {"final_answer": action.content, "history": history,
                        "log": self.log.entries}

            result = self.gateway.call(action.tool_name, action.tool_args or {})
            history.append({"type": "tool_call", "tool_name": action.tool_name,
                            "tool_args": action.tool_args})
            history.append({"type": "tool_result", "result": result})

            # The mock model retries its injected directive forever once it has
            # read it, so stop at the first block and surface it.
            if isinstance(result, dict) and str(result.get("error", "")).startswith("blocked"):
                return {"final_answer": None, "history": history, "log": self.log.entries,
                        "blocked": True, "block_reason": result["error"]}

        return {"final_answer": None, "history": history, "log": self.log.entries,
                "error": "max_steps exceeded"}
