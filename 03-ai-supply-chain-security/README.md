# 3. AI Supply Chain Security

The AI supply chain now has five layers most orgs don't audit: base models, fine-tuning data,
ML-specific packages, model file formats, and the infrastructure they run on. Unlike Project 2
(which attacks a system you built), this project attacks — and then defends against — the
components you *pull in*. Given the tooling you already run daily (Claude Code across three
machines with SSH-key access to production), this is the one project on this list that doubles as
hardening your own dev environment, not just a portfolio exercise.

> **Safety note.** All malicious artefacts (typosquat packages, poisoned pickle files) are
> self-authored, clearly labelled, and only ever installed inside a disposable container or VM —
> never on a machine with real credentials.

## Business Scenario

"Northwind Retail" pulls a base model from a public model hub, several ML-specific Python/npm
packages, and a third-party MCP server package (linking back to Project 2) into its build
pipeline. You play both attacker (planting the compromise) and defender (building the gate that
should have caught it).

## Architecture

```
flowchart LR
    subgraph Sources["External Sources"]
        Hub[(Model Hub\ne.g. HF-style registry)]
        Reg[(PyPI / npm\nML packages)]
        MCPPkg[MCP server\npackage]
    end

    Sources -->|pip/npm install,\nmodel download| Gate{Ingestion Gate}
    Gate -->|picklescan, modelscan,\nCVE scan, provenance verify,\nsafetensors-only policy| Pass{Pass?}
    Pass -->|yes| Build[Build Pipeline]
    Pass -->|no, blocked| Quarantine[Quarantine + Alert]

    Attacker([Attacker]) -.->|typosquat package,\npickle RCE in checkpoint,\nfalsified provenance| Sources

    style Attacker fill:#3a1414,stroke:#c0392b,color:#fff
    style Quarantine fill:#14243a,stroke:#2980b9,color:#fff
```

    Loading

## Attack Catalogue

- **Dependency confusion / typosquatting** — a malicious package that mimics a legitimate
  ML/MCP package name, installed via a near-identical import; the real-world pattern behind
  campaigns that exfiltrated SSH keys and cloud credentials from AI coding assistants in early
  2026.
- **Pickle deserialization RCE** — a model checkpoint saved in Python's pickle format that
  executes arbitrary code on load, still common across public model hubs.
- **Falsified provenance** — a model or dataset claiming an origin, license, or architecture it
  doesn't actually have.
- **Unpinned dependency drift** — a "latest" tag silently pulling in a compromised release between
  builds.
- **MCP package supply-chain compromise** — tie back to Project 2: the same ingestion gate applies
  to third-party MCP server packages, not just model weights.

## Methodology

1. Build the ingestion gate: `picklescan` + `modelscan` for model files, a CVE scan for
   dependencies, and a provenance-verification step (checksum/signature check).
2. Demonstrate each attack above succeeding against a build pipeline *without* the gate.
3. Add the gate and retest — the same artefacts should now be caught and quarantined.
4. Move to a **safetensors-only policy** for model weights and pin every dependency (no floating
   tags) as the durable fix, not just the detection layer.
5. Generate an ML-BOM (CycloneDX ML-BOM or SPDX AI Profile) for the final build — this is the
   artefact that lets you answer "which of our systems use this compromised component?" in
   minutes instead of days.

## Findings Mapping

| Attack                                | Reference                                       |
| --------------------------------------- | -------------------------------------------------- |
| Typosquatting, dependency confusion    | OWASP LLM03 — Supply Chain Vulnerabilities        |
| Pickle RCE, falsified provenance       | MITRE ATLAS (ML Supply Chain Compromise)          |
| Missing SBOM / provenance              | NIST AI RMF — Map function; NIST SP 800-218A       |

## Portfolio Checklist

- [ ] Ingestion gate implementation (picklescan, modelscan, CVE scan, provenance check)
- [ ] Demonstrated attack: typosquat or pickle RCE succeeding pre-gate, blocked post-gate
- [ ] Safetensors-only policy and pinned-dependency manifest
- [ ] Generated ML-BOM (CycloneDX or SPDX AI Profile) for the build
- [ ] Findings mapped to OWASP LLM03, MITRE ATLAS, NIST AI RMF
- [ ] Written report + short demo + one-page executive summary

## Tools & References

| Tool / Standard              | Link                                                                          |
| ------------------------------ | -------------------------------------------------------------------------------- |
| picklescan                     | <https://github.com/mmaitre314/picklescan>                                       |
| modelscan (Protect AI)         | <https://github.com/protectai/modelscan>                                         |
| safetensors                    | <https://github.com/huggingface/safetensors>                                     |
| CycloneDX ML-BOM               | <https://cyclonedx.org/capabilities/mlbom/>                                      |
| SLSA                           | <https://slsa.dev/>                                                              |
| Sigstore / Cosign / in-toto    | <https://www.sigstore.dev/>                                                      |
| OWASP Top 10 for LLM Applications | <https://owasp.org/www-project-top-10-for-large-language-model-applications/> |
| MITRE ATLAS                    | <https://atlas.mitre.org/>                                                       |
