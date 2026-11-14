# Frameworks map

## OWASP Top 10 for LLM Applications (2025) to this guide

| ID | Risk | Primary questions | Typical controls |
| --- | --- | --- | --- |
| LLM01 | Prompt Injection | [Q2](../questions/02-prompt-injection.md), [Q4](../questions/04-agent-tool-access.md), [Q19](../questions/19-guardrails.md) | Privilege separation, policy gateway, taint tracking, approvals |
| LLM02 | Sensitive Information Disclosure | [Q14](../questions/14-privacy-data-protection.md), [Q3](../questions/03-rag-security.md), [Q18](../questions/18-model-theft-and-inference-attacks.md) | Minimisation, ACL-filtered retrieval, redaction |
| LLM03 | Supply Chain | [Q12](../questions/12-ai-supply-chain.md), [Q5](../questions/05-mcp-security.md) | Safe formats, pinning, signing, AIBOM |
| LLM04 | Data and Model Poisoning | [Q13](../questions/13-data-and-model-poisoning.md), [Q3](../questions/03-rag-security.md) | Provenance, ingestion checks, canaries |
| LLM05 | Improper Output Handling | [Q11](../questions/11-improper-output-handling.md) | Schema validation, parameterisation, encoding |
| LLM06 | Excessive Agency | [Q4](../questions/04-agent-tool-access.md), [Q15](../questions/15-multi-agent-security.md), [Q16](../questions/16-human-in-the-loop.md) | Least privilege, tiers, kill switch |
| LLM07 | System Prompt Leakage | [Q2](../questions/02-prompt-injection.md) | No secrets in prompts; assume disclosure |
| LLM08 | Vector and Embedding Weaknesses | [Q3](../questions/03-rag-security.md), [Q14](../questions/14-privacy-data-protection.md) | Tenant isolation, access filters |
| LLM09 | Misinformation | [Q19](../questions/19-guardrails.md), [Q16](../questions/16-human-in-the-loop.md) | Grounding checks, human review for impact |
| LLM10 | Unbounded Consumption | [Q17](../questions/17-unbounded-consumption.md), [Q18](../questions/18-model-theft-and-inference-attacks.md) | Quotas, step caps, spend alarms |

Confirm the numbering against the current OWASP publication.

## Which framework answers which need

| Need | Use |
| --- | --- |
| Threat modelling vocabulary | STRIDE, MITRE ATLAS, OWASP LLM and agentic lists |
| Risk management process | NIST AI RMF (Govern, Map, Measure, Manage) |
| Certifiable management system | ISO/IEC 42001 |
| Legal obligations | EU AI Act, Privacy Act 1988 (Australia), GDPR where relevant |
| Local voluntary guidance | Australian Voluntary AI Safety Standard |
| Testing | garak, PyRIT, promptfoo, Inspect ([Q6](../questions/06-ai-red-teaming.md)) |
