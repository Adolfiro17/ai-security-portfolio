# Instructor Solutions: Lab 1

Attempt the lab first. These are model answers, not the only valid ones.

## Challenge answers

1. **Normal behaviour.** Both agents complete the password-reset task using one document read. A
   control that breaks the legitimate workflow will be switched off, so test it first.
2. **The injection.** It is an HTML comment in `data/support_docs/asset_faq.md`, invisible in a
   rendered page, but the model receives raw text. Any retrieved or tool-returned content is an
   input channel.
3. **Insecure exploit.** The call ran as `user:alice`, nobody approved it, and the log recorded
   "allowed" because no check existed. The record was returned to the user.
4. **Hardened replay.** The mock model is exactly as manipulated, and still `query_asset_inventory`
   is refused: "not in allow-list for this workflow". The blocked attempt is logged under
   `agent:support-assistant-001`.
5. **Approval lifecycle.** Step 3 fails because the approval is bound to the exact tool and
   arguments it was requested for. Step 5 fails because an approval is consumed on use.
6. **Credentials.** A stolen credential works for one named tool, once, for thirty seconds.
7. **Revocation.** It overrides everything, including the legitimate task. That is the point of a
   kill switch; accept the lost availability to stop an active incident.
8. **Mutations.** Removing the allow-list alone is survivable because approval still blocks the
   call. Removing both lets the manipulated model reach the record. This is defence in depth, and
   it shows why the allow-list and approval should not rely on each other.

## Task notes

**A.** Order: revocation, allow-list, approval for high-impact tools, credential issue and redeem,
execute with a trust label, log. Revocation is first so that nothing else can be reached once the
kill switch is thrown.

**B.** Approval still protects it. The approval request must be rendered from the structured call
by trusted code (tool name and arguments), never from model-written text.

**C.** Sketch:

```python
# app/tools.py
def reset_password(user: str) -> dict:
    return {"status": "reset_requested", "user": user}

TOOL_SCHEMAS["reset_password"] = {"description": "Reset a user's password.", "high_impact": True}
# app/agent_hardened.py: add to ToolGateway._tools, and leave it OUT of SUPPORT_WORKFLOW_TOOLS
```

```python
def test_injected_password_reset_is_blocked():
    result = HardenedAgent().gateway.call("reset_password", {"user": "ceo"})
    assert "blocked" in result["error"]
```

**D.** The existing test keeps passing because it uses the default allow-list. That reveals a gap:
the suite does not test the gateway under a widened allow-list. The test to add is the one in
`lab/mutations.py`: with the allow-list widened and approval on, the call must still be blocked.

**E.** Track the last document read in the gateway and add it to each log record:

```python
# in ToolGateway.call, after a read_support_docs success:
self.last_document = tool_args.get("filename")
# in _log: pass last_document=self.last_document
```

## Reflection answers

1. A prompt is a request, not enforcement. The model can be convinced to ignore it.
2. Trustworthy: separate channel the agent cannot write to, rendering from the raw call, bound and
   single use. Theatre: approvals inside the agent's own chat, model-written summaries, and so many
   prompts that people click through.
3. Revocation and logging, because they let you respond when everything else has failed.
4. Cross-agent escalation and synthetic-identity attacks, real approval channels and real
   identity-provider tokens.
