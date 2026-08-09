# 6. AI Security and Governance Assurance System

Connects technical security work to business decisions — the skill that separates senior candidates
from junior ones, and the one most technically-minded applicants neglect entirely.

## Business Scenario

A fictional organisation, "Northwind Retail," running several AI systems: an employee chatbot, a
customer-support assistant, a coding agent and a decision-support model.

## Architecture

```mermaid
flowchart TB
    Inventory[AI Inventory\nowner, purpose, model,\ndata classification,\nuser population,\nintegrations, risk tier]

    Inventory --> Register[AI Risk Register\nrisk, likelihood, impact, treatment]
    Register --> ControlMap[Control Mapping\nNIST AI RMF / GenAI Profile\nOWASP LLM Top 10\nMITRE ATLAS]
    ControlMap --> Evidence[Evidence Register\nhow each control is tested,\nwhat proof demonstrates it works]
    Evidence --> Dashboard[Executive Dashboard\nmajor risks, control weaknesses,\noverdue actions, decisions\nneeding leadership approval]

    Finding[Red-team Finding\ne.g. from Project 4] -->|logged as| Register
    Register -->|mapped to| ControlMap
    ControlMap -->|tested via| Evidence
    Evidence -->|gap found| Ticket[Remediation Ticket]
    Ticket -->|fixed, verified by| Retest[Retest]
    Retest -->|closes loop back into| Register

    style Finding fill:#3a1414,stroke:#c0392b,color:#fff
    style Retest fill:#14243a,stroke:#2980b9,color:#fff
```

## Components

- **AI Inventory** — every system's owner, purpose, model, data classification, user population,
  integrations and risk tier. "We don't even know how many AI systems we run" is a real, common
  failure.
- **AI Risk Register** — each risk, its likelihood and impact, and its treatment
- **Control Mapping** — controls aligned to the [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework),
  the NIST Generative AI Profile (NIST AI 600-1), the
  [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  and relevant [MITRE ATLAS](https://atlas.mitre.org/) techniques
- **Evidence Register** — exactly how each control is tested and what proof demonstrates it's working
- **Executive Dashboard** — major risks, control weaknesses, overdue actions, decisions needing
  leadership approval

## The Traceability Thread

Take one real red-team finding from [Project 4](../04-ai-red-teaming-lab/README.md) and follow it
all the way through: demonstrated attack → logged risk → mapped control → evidence requirement →
remediation ticket → retest. That single thread — a technical weakness becoming a managed business
risk — is the detail that elevates this project above a stack of spreadsheets, and it's the
strongest single artefact in the whole portfolio.

## Portfolio Checklist

- [ ] AI inventory covering all 4 fictional systems
- [ ] Risk register with at least the finding(s) traced from Project 4, plus any dependency or
      model-provenance findings from Projects 3 and 8
- [ ] Control mapping table (control ↔ NIST AI RMF ↔ OWASP LLM Top 10 ↔ MITRE ATLAS)
- [ ] Evidence register entries for each mapped control
- [ ] Executive dashboard (even a simple one) summarising risk posture
- [ ] The full traceability thread, documented end to end
- [ ] Written report + short demo + one-page executive summary

## Tools & References

| Standard | Link |
|---|---|
| NIST AI Risk Management Framework (AI RMF 1.0) | https://www.nist.gov/itl/ai-risk-management-framework |
| NIST Generative AI Profile (NIST AI 600-1) | https://www.nist.gov/itl/ai-risk-management-framework |
| OWASP Top 10 for LLM Applications | https://owasp.org/www-project-top-10-for-large-language-model-applications/ |
| MITRE ATLAS | https://atlas.mitre.org/ |
