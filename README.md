# AI Security Projects

Eight hands-on projects for building a portfolio that proves — not just claims — the ability to
attack, defend, monitor and govern real AI systems.

> **Safety note.** Every project runs in an isolated environment, against systems you own, using
> fictional data and planted, fake secrets. Never point these tools or techniques at systems,
> models or accounts you do not control.

Sequenced for build order, not difficulty — each project below feeds telemetry, findings, or
architecture into the ones after it. Depth over breadth: projects done thoroughly and documented
well outperform a larger set done superficially. If time is short, Projects 1, 4 and 6 are the
minimum viable set; everything else adds depth.

## Projects

| # | Project                                                                    | Focus                                                            | Reference                                  | Status  |
| --- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------- | ------- |
| 1 | [Secure AI Agent](01-secure-ai-agent/README.md)                               | Break and re-architect a tool-using agent                            | LLM01, LLM06, LLM07 / OWASP Agentic            | Planned |
| 2 | [Secure MCP Application](02-secure-mcp-application/README.md)                 | Attack and harden an MCP server (tool poisoning, supply chain)      | OWASP MCP Top 10, LLM03                        | Planned |
| 3 | [AI Supply Chain Security](03-ai-supply-chain-security/README.md)             | Ingestion-gate a poisoned model/package before it reaches a build   | LLM03, MITRE ATLAS, NIST SP 800-218A           | Planned |
| 4 | [Automated AI Red-Teaming Lab](04-ai-red-teaming-lab/README.md)               | Attack a chatbot with Garak + PyRIT, automate in CI                  | LLM01, LLM02, LLM07                            | Planned |
| 5 | [AI Security Monitoring & Detection Lab](05-ai-security-monitoring/README.md) | Detect misuse across Projects 1, 2, 4 and 7                          | LLM01, LLM02, LLM06                            | Planned |
| 6 | [AI Security & Governance Assurance System](06-ai-governance-assurance/README.md) | Connect findings to risk, controls and evidence                 | All (via mapping)                              | Planned |
| 7 | [Secure RAG Application](07-secure-rag-application/README.md)                 | Threat-model and attack a retrieval pipeline                         | LLM01, LLM02, LLM08                            | Planned |
| 8 | [Model & Dataset Integrity](08-model-dataset-integrity/README.md)             | Poison and detect backdoors in a fine-tuned model                    | LLM04, MITRE ATLAS (Poison Training Data)      | Planned |

## Why this order

- **1 → Secure AI Agent** establishes the hardened tool/identity/authorization pattern (dedicated
  agent identity, allow-listed tools, HITL approval, tool-call logging) that Project 2 builds on
  at the protocol layer.
- **2 → Secure MCP Application** attacks and hardens the transport/tool layer underneath any
  agent — tool poisoning, credential exposure, missing tool-level RBAC.
- **3 → AI Supply Chain Security** moves one layer down again: the packages and model files that
  Projects 1 and 2 depend on before a single request is ever sent.
- **4 → Red-Teaming Lab** produces the automated, CI-wired probe suite (Garak, PyRIT, Promptfoo)
  used to generate the findings that Project 5 detects and Project 6 traces into governance.
- **5 → Monitoring & Detection** ingests runtime telemetry from Projects 1, 2, 4 and 7. Project 3's
  supply-chain findings are a build-time gate, not a telemetry stream, so they feed Project 6's
  risk register directly instead.
- **6 → Governance & Assurance** takes one real finding (from Project 4 by default, extendable to
  3 and 8) and traces it end to end: attack → risk register → control mapping → evidence →
  remediation → retest.
- **7 → Secure RAG Application** is the most self-contained project — its attack surface (indirect
  injection, cross-tenant leakage, embedding weaknesses) doesn't depend on the others, so it's the
  best candidate to drop if time is short.
- **8 → Model & Dataset Integrity** is placed last deliberately: it's pre-deployment rather than
  runtime, has the least overlap with SOC/agent-ops skills, and is the one project worth treating
  as optional depth rather than core sequence.

## Standards and Frameworks Referenced

| Framework                                         | Use                                                                 | Link                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| OWASP Top 10 for LLM Applications                 | Vulnerability classification for prompts, RAG and outputs           | <https://owasp.org/www-project-top-10-for-large-language-model-applications/> |
| OWASP GenAI Security Project — Agentic AI Threats | Agent-specific risks: goal hijacking, tool misuse, memory poisoning | <https://genai.owasp.org/>                                                    |
| MITRE ATLAS                                       | Adversary tactics/techniques for AI systems                         | <https://atlas.mitre.org/>                                                    |
| NIST AI Risk Management Framework (AI RMF 1.0)    | Govern / Map / Measure / Manage structure for AI risk               | <https://www.nist.gov/itl/ai-risk-management-framework>                       |
| NIST Generative AI Profile (NIST AI 600-1)        | GenAI-specific risk profile on top of the AI RMF                    | <https://www.nist.gov/itl/ai-risk-management-framework>                       |
| NIST SP 800-218A                                  | Secure software development practices for AI/ML components          | <https://csrc.nist.gov/pubs/sp/800/218/a/final>                               |

## Tools Referenced Across Projects

| Tool                 | Purpose                                                                                  | Link                                                  |
| -------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Ollama               | Run open-weight LLMs locally for a free, isolated target                                 | <https://ollama.com/>                                 |
| Garak                | Open-source LLM vulnerability scanner (probes, generators, hit-logs)                     | <https://github.com/NVIDIA/garak>                     |
| PyRIT                | Adversarial-prompt orchestration framework (targets, orchestrators, scorers, converters) | <https://github.com/Azure/PyRIT>                      |
| Promptfoo            | Fast red-team/eval suite for LLM apps                                                    | <https://www.promptfoo.dev/>                          |
| mcp-scan              | Static/config scanning for MCP servers                                                   | <https://github.com/invariantlabs-ai/mcp-scan>         |
| picklescan / modelscan | Scan model files/checkpoints for malicious payloads                                    | <https://github.com/mmaitre314/picklescan> · <https://github.com/protectai/modelscan> |
| Adversarial Robustness Toolbox (ART) | Data poisoning, backdoor detection and evaluation                          | <https://github.com/Trusted-AI/adversarial-robustness-toolbox> |
| LangChain            | RAG pipeline components (loaders, retrievers, chains)                                    | <https://python.langchain.com/>                       |
| LlamaIndex           | Alternative RAG/indexing framework                                                       | <https://www.llamaindex.ai/>                          |
| Chroma               | Lightweight local vector database                                                        | <https://www.trychroma.com/>                          |
| Elastic / OpenSearch | Ship and search telemetry for the monitoring lab                                         | <https://www.elastic.co/> · <https://opensearch.org/> |
| GitHub Actions       | CI automation for rerunning red-team probes on change                                    | <https://docs.github.com/actions>                     |

## How Each Project Is Documented

- Business scenario — who the fictional org is and what the system does
- Architecture — a Mermaid diagram of components and trust boundaries
- Threat model / attack catalogue — what is tested and why
- Methodology — tools, steps, how success/failure is scored
- Findings format — how results map to OWASP LLM Top 10 / OWASP MCP Top 10 / MITRE ATLAS / NIST
- Mitigations and retest — the control implemented and proof it worked
- Portfolio checklist — what to actually ship (code, report, demo, README)

## Presenting the Work

For each completed project: a concise README, a short recorded demo, and a one-page executive
summary in plain business language. State what was built directly, where AI assisted, and what
still needs human validation.

## Attribution

The original five-project structure, format, and portfolio philosophy behind this repository come
from [taimurijlal/AI-Security-Projects](https://github.com/taimurijlal/AI-Security-Projects). This
version reorders the original projects and adds three new ones — Secure MCP Application, AI Supply
Chain Security, and Model & Dataset Integrity — following the same documentation format.
