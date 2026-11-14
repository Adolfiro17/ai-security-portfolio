# 15. What changes when several agents work together?

> **Added question.** It extends the ten source questions (see Q4) to multi-agent systems and agent-to-agent protocols. See [ATTRIBUTION.md](../ATTRIBUTION.md).

**Portfolio link:** the optional two-agent escalation extension described in [Project 1](../../01-secure-ai-agent/).

## 1. The answer in one minute

When agents delegate to each other, every message between them becomes a new injection channel, authority can grow at every hop, and accountability gets harder to trace. The weak agent in the chain, perhaps one that reads untrusted email, can become the way into a powerful agent that can pay invoices. So I give each agent its own verifiable identity, make delegated authority only ever shrink (attenuation), mediate messages through a policy layer that carries provenance, isolate memory and context, put approval at privilege boundaries, limit chain depth and fan-out, and trace actions end to end across agents.

## 2. The escalation problem

```mermaid
sequenceDiagram
    participant X as Attacker
    participant R as Reader agent (low privilege, reads email)
    participant O as Orchestrator
    participant P as Payments agent (high privilege)
    participant B as Bank API

    X->>R: Email with hidden instruction
    R->>O: "Summary: urgent, pay invoice 77 to account 123"
    O->>P: Delegate: pay invoice 77
    Note over R,P: Without provenance, the request looks like an internal, trusted message
    P->>B: Transfer funds (the payments agent has the authority)
    Note over P,B: With controls: provenance marks the request as derived from untrusted email, policy requires approval, bank details verified
```

The attack never touched the payments agent directly. It borrowed that agent's authority through a chain of trust. This is the *confused deputy* problem, repeated at every hop.

## 3. Threats

| Threat | Description | Example |
| --- | --- | --- |
| Message injection | Instructions arrive via another agent's output | The reader agent's summary carries a hidden command |
| Agent impersonation | A rogue process pretends to be a trusted agent | A look-alike agent registers on the message bus |
| Privilege escalation by delegation | A weak agent obtains the effect of a strong agent's permissions | Section 2 |
| Authority accumulation | Delegated tokens are broader than needed or never expire | A "temporary" admin token still valid next week |
| Shared-memory poisoning | One agent writes to a shared store that others trust | A poisoned note changes every agent's plan |
| Cascading failure and runaway loops | Agents trigger each other repeatedly | Cost spike, repeated side effects |
| Accountability gap | Logs show the final action but not the chain behind it | Nobody can say which input started it |
| Collusion by contamination | Several agents share a compromised context | One injected context spreads |

## 4. Controls

| Control | How it works |
| --- | --- |
| Distinct identity per agent | Each agent has a workload identity with credentials of its own; calls are authenticated, for example with mutual TLS or signed messages |
| Attenuated delegation | A delegated credential can only grant a subset of the delegator's rights, with a short life, a narrow scope and a named audience; use capability-style tokens |
| Provenance and taint on messages | Messages carry the origin and trust level of the content they derive from; policy rules refer to it ("payments over a limit cannot be triggered by untrusted-derived requests without approval") |
| A mediating broker | Agents do not talk to each other directly; a broker applies policy, logs and enforces schemas |
| Structured messages | Agents exchange validated, typed messages, not free text that the next agent will read as instructions |
| Context and memory isolation | Separate memory per agent and per task; writes to shared memory are privileged and audited |
| Approval at privilege boundaries | A human or an independent control approves when a request moves from a low-trust to a high-trust agent, with raw parameters shown ([Q16](16-human-in-the-loop.md)) |
| Limits | Maximum chain depth, fan-out, steps, spend and wall-clock per task, plus loop detection |
| End-to-end tracing | One trace ID spans every hop, recording the identity, delegated scope and decision at each step |
| Kill switches | Disable one agent, one capability or one tenant independently |

Protocols such as Model Context Protocol (agent to tool) and Agent2Agent (agent to agent) standardise connectivity. Review the authentication and authorisation options each offers, and do not assume that a protocol's use implies safe defaults.

## 5. Worked example: delegation that can only shrink

```python
from dataclasses import dataclass
import time

@dataclass(frozen=True)
class Capability:
    holder: str
    scopes: frozenset          # e.g. {"invoices:read", "payments:create<=1000"}
    expires_at: float
    audience: str

def delegate(parent: Capability, to_agent: str, requested: set, ttl_s: int, audience: str) -> Capability:
    if time.time() >= parent.expires_at:
        raise PermissionError("parent capability expired")
    if not requested <= parent.scopes:                        # attenuation: subset only
        raise PermissionError("cannot delegate rights you do not hold")
    expires = min(parent.expires_at, time.time() + ttl_s)    # never outlive the parent
    return Capability(to_agent, frozenset(requested), expires, audience)
```

The reader agent never receives `payments:*` at all, so nothing it says can cause a payment unless a request passes through the broker and policy for the payments agent, which can then require approval because the request is marked as derived from untrusted input.

## 6. Follow-up questions, with answers

**How should identity work between agents?**
Give each agent its own workload identity and authenticate every call, for example with mutual TLS or signed tokens. Authorisation is per agent and per action. The log records both the calling agent and the user on whose behalf it acts, so the chain can be reconstructed.

**How do you prevent privilege escalation through delegation?**
Make delegation attenuating (a delegate can never hold more than the delegator), short-lived and audience-bound. Evaluate policy at the receiving agent using the original provenance, not just the immediate sender, so a trusted-looking message that derives from untrusted content is still treated with suspicion.

**Is the orchestrator a single point of trust?**
It can be, and that is a risk. Keep it simple and deterministic where possible, treat the model inside it as untrusted for authorisation decisions, run the policy in separate code, and avoid giving the orchestrator broad credentials of its own.

**Do more agents mean more safety through cross-checking?**
Only if they are independent. Agents that share context, a model and a prompt tend to fail together, so a reviewing agent can be talked into the same mistake. Independent checks should be deterministic where possible or involve different information and a human where stakes are high.

**How does this relate to MCP?** *(added)*
MCP connects a host to tools and data; multi-agent protocols connect agents to agents. Both create trust relationships, so the same ideas apply: authenticate, scope, validate, label untrusted content and log ([Q5](05-mcp-security.md)).

**How would you test a multi-agent system?** *(added)*
Write escalation scenarios in which a low-privilege agent is compromised and tries to obtain a high-privilege outcome, assert on the final actions and on the policy decisions, test chain-depth and loop limits, test revocation of a single agent and check that the trace reconstructs the whole chain. Add the scenarios to CI ([Q9](09-ai-security-cicd.md)).

## 7. Common mistakes

1. Treating messages from other agents as trusted by default.
2. Sharing one broad credential among all agents.
3. Letting agents write to a common memory without controls.
4. Logging each agent separately, with no way to follow a request across them.

## 8. What to demonstrate

A two-agent workflow where a compromised low-privilege agent tries to trigger a high-privilege action, with attenuated delegation, provenance-aware policy and a trace showing the blocked escalation.
