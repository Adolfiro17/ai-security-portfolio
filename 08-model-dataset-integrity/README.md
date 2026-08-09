# 8. Model & Dataset Integrity

Every other project in this portfolio attacks a system *after* the model is trained. This one goes
one layer deeper: what happens before deployment, when the model itself learns the wrong thing.
Optional relative to Projects 1–7 — it's the one category with the least overlap to SOC/agent-ops
work — but it closes the one gap NIST AI RMF's Map function explicitly calls out: risk introduced
by training data and third-party models, not runtime behaviour.

> **Safety note.** All poisoning is performed on a small model you train yourself on a fictional
> dataset, offline, never against a production or third-party model.

## Business Scenario

"Northwind Retail" fine-tunes a small open-weight classifier (e.g. a support-ticket triage or
sentiment model) on an internal dataset. You play the role of an insider or compromised vendor
poisoning a small fraction of that dataset before training.

## Architecture

```
flowchart LR
    subgraph Pipeline["Training Pipeline"]
        Data[(Training Dataset)]
        Curate[Curation /\nProvenance Tracking]
        Train[Training / Fine-tuning]
        Eval[Behavioural\nEvaluation Gate]
    end

    Poison([Poisoned Samples\n~0.1-1% of dataset]) -.->|inserted before curation| Data
    Data --> Curate --> Train --> Eval
    Eval -->|pass| Deploy[Deployed Model]
    Eval -->|backdoor detected,\nblocked| Quarantine[Quarantine + Retrain]

    style Poison fill:#3a1414,stroke:#c0392b,color:#fff
    style Quarantine fill:#14243a,stroke:#2980b9,color:#fff
```

    Loading

## Attack Catalogue

- **Targeted data poisoning** — insert a small number of mislabeled or adversarially crafted
  samples designed to shift the model's behaviour on a specific input pattern; research shows a
  tiny fraction of a dataset (often under 1%) is enough to embed an effective backdoor.
- **Trigger-based backdoor** — poison the fine-tuning set so the model behaves normally except
  when a specific trigger phrase or pattern appears in the input, then produces attacker-chosen
  output.
- **Label-flipping** — corrupt training labels on a subset of legitimate data to degrade accuracy
  on a targeted class without an obvious trigger.
- **Provenance gap exploitation** — demonstrate how the absence of dataset chain-of-custody makes
  the poisoning invisible after the fact.

## Methodology

1. Train a clean baseline model and record its behavioural profile.
2. Poison a small, documented fraction of the training set with a chosen trigger; retrain.
3. Confirm the backdoor: normal accuracy on clean inputs, attacker-chosen output on triggered
   inputs.
4. Build detection: activation clustering and/or a neural-cleanse-style search for anomalous
   trigger patterns; test whether it flags the poisoned model.
5. Build prevention: data provenance tracking with source/collection/curation records, outlier
   detection on the training set before training, and a behavioural evaluation gate that must pass
   before a model is promoted to "deployed."
6. Retest — clean pipeline should train normally; the same poisoning attempt should now be caught
   at either the data-validation or evaluation-gate stage.

## Findings Mapping

| Attack                          | Reference                                                    |
| ---------------------------------- | ---------------------------------------------------------------- |
| Data/label poisoning, backdoors   | MITRE ATLAS (Poison Training Data); OWASP LLM04 — Data/Model Poisoning |
| Missing provenance / chain of custody | NIST AI RMF — Map function; NIST SP 800-218A                |

## Portfolio Checklist

- [ ] Clean baseline model + documented poisoned variant (small, labeled poisoning fraction)
- [ ] Demonstrated backdoor: clean-input accuracy vs. triggered-input behaviour, side by side
- [ ] Detection method (activation clustering / neural-cleanse-style) run against both models
- [ ] Data provenance record and evaluation-gate implementation
- [ ] Retest evidence: poisoning attempt caught pre-deployment
- [ ] Written report + short demo + one-page executive summary

## Tools & References

| Tool / Standard                  | Link                                                                          |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| Adversarial Robustness Toolbox (ART) | <https://github.com/Trusted-AI/adversarial-robustness-toolbox>                 |
| NIST AI Risk Management Framework  | <https://www.nist.gov/itl/ai-risk-management-framework>                        |
| NIST SP 800-218A                   | <https://csrc.nist.gov/pubs/sp/800/218/a/final>                                |
| OWASP Top 10 for LLM Applications  | <https://owasp.org/www-project-top-10-for-large-language-model-applications/> |
| MITRE ATLAS                        | <https://atlas.mitre.org/>                                                     |
