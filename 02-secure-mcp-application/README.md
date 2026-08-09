# 2. Secure MCP Application

MCP servers sit between an agent and the real world — tools, files, APIs, credentials. Unlike a
prompt, a tool's *description* is itself untrusted input the model reasons over, and unlike a
chatbot, a compromised MCP server has standing, reusable access. This is currently the fastest-
moving attack surface in AI security, with dozens of CVEs filed against MCP servers and tooling in
the first months of 2026 alone.

> **Safety note.** As with every project in this portfolio: isolated environment, fictional data,
> planted fake secrets, systems you own only.

## Business Scenario

A fictional internal MCP server for "Northwind Retail" exposing three tools to a client agent:
ticket lookup (read), file search (read), and one intentionally over-privileged tool (e.g. a
"send email" tool with no scope restriction) that stands in for the over-permissioned tools real
deployments accumulate.

## Architecture

```
flowchart LR
    Agent[Client Agent] -->|MCP requests| Server[MCP Server]
    Server -->|tool definitions,\nincl. untrusted\ndescriptions| Agent
    Server -->|read| Tickets[(Ticket System)]
    Server -->|read| Files[(File Store)]
    Server -->|unscoped write| Mail[(Email Tool)]

    Attacker([Attacker]) -.->|poisoned tool description,\nplaintext token interception,\ntyposquat package| Server

    style Attacker fill:#3a1414,stroke:#c0392b,color:#fff
    style Mail fill:#3a2a14,stroke:#e67e22,color:#fff
```

    Loading

## Attack Catalogue

- **Tool poisoning** — a manipulated tool description that hijacks agent behaviour without
  touching the prompt at all; the description field is untrusted input the model still reasons
  over.
- **Supply-chain compromise** — a malicious/typosquatted MCP package that behaves normally while
  silently exfiltrating data (e.g. BCC-ing every outbound email to an attacker address).
- **Credential and transport exposure** — plaintext HTTP MCP endpoints, tokens visible in transit,
  no TLS/mTLS between agent and server.
- **Command injection** — the most common real-world MCP vulnerability class; unsanitised input
  reaching a shell or subprocess call inside a tool handler.
- **Confused deputy / missing tool-level RBAC** — a role that should only read tickets is able to
  invoke the unscoped email tool because authorization is enforced at the server level, not the
  tool level.
- **Debug surface exposure** — MCP Inspector or other debug tooling left reachable on a network
  port instead of bound to localhost.

## Methodology

1. Stand up the server with plaintext HTTP and no tool-level scoping — demonstrate each attack
   above succeeding.
2. Run `mcp-scan` and Semgrep's MCP-specific ruleset against the server for a baseline static
   finding set.
3. Harden: OAuth 2.1 with audience validation, no token passthrough, tool-level RBAC with
   incremental scope consent, input validation on every tool handler, version pinning on all
   dependencies.
4. Retest every attack from the catalogue against the hardened server and record the result.

## Findings Mapping

| Attack                                  | Reference                                              |
| ---------------------------------------- | ------------------------------------------------------- |
| Tool poisoning, confused deputy          | OWASP MCP Top 10 / OWASP GenAI Security — Agentic Threats |
| Supply-chain compromise                  | OWASP LLM03 — Supply Chain Vulnerabilities              |
| Credential/transport exposure, injection | MITRE ATLAS                                              |

## Mitigation → Retest Loop

For every successful attack: implement the corresponding control, retest the identical attack
against the hardened server, and record the result. The retest evidence — not the fix — is the
deliverable, consistent with every other project in this portfolio.

## Portfolio Checklist

- [ ] MCP server code (insecure baseline + hardened version) in `server/`
- [ ] `mcp-scan` and Semgrep output in `results/`
- [ ] OAuth 2.1 + tool-level RBAC implementation
- [ ] Before/after evidence for each attack catalogue item
- [ ] Findings mapped to OWASP MCP Top 10 / LLM03 and MITRE ATLAS
- [ ] Written assessment + short recorded demo + one-page executive summary

## Tools & References

| Tool / Standard                       | Link                                                                 |
| -------------------------------------- | --------------------------------------------------------------------- |
| Model Context Protocol spec            | <https://modelcontextprotocol.io/>                                    |
| mcp-scan                               | <https://github.com/invariantlabs-ai/mcp-scan>                        |
| Semgrep MCP rules                      | <https://semgrep.dev/>                                                |
| OWASP Top 10 for LLM Applications      | <https://owasp.org/www-project-top-10-for-large-language-model-applications/> |
| OWASP GenAI Security — Agentic Threats | <https://genai.owasp.org/>                                            |
| MITRE ATLAS                            | <https://atlas.mitre.org/>                                            |
