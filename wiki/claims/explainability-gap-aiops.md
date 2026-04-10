---
title: "Current AIOps anomaly detection and RCA techniques lack explainability and countermeasure recommendation"
slug: explainability-gap-aiops
status: proposed
confidence: 0.6
tags: [explainability, aiops, anomaly-detection, root-cause-analysis, countermeasures]
domain: "ML Systems"
source_papers: [anomaly-detection-failure-root-cause-analysis]
evidence:
  - source: anomaly-detection-failure-root-cause-analysis
    type: supports
    strength: moderate
    detail: "Survey finds that no surveyed technique provides explainability for detected anomalies or identified root causes, and none recommends countermeasures. The survey argues for 'explainable by design' approaches and automated countermeasure recommendation as key research directions."
conditions: "Based on techniques surveyed up to 2021. More recent work may have begun addressing explainability."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Existing techniques for anomaly detection and root cause analysis in microservice systems do not provide human-interpretable explanations for why an anomaly was flagged or why a particular service was identified as the root cause. Additionally, no technique recommends countermeasures to prevent recurrence. This limits operator trust and makes it difficult to distinguish true positives from false positives without manual investigation.

## Evidence summary

The Soldani & Brogi (2022) survey explicitly identifies explainability and countermeasure recommendation as open research directions. The survey notes that associating anomalies with explanations would allow operators to directly exclude false positives. It draws an analogy to the broader AI explainability movement and argues for techniques that are "explainable by design."

## Conditions and scope

Claim is based on the 2013-2021 survey period. The broader XAI (Explainable AI) movement has since influenced AIOps research, though concrete progress in this specific domain remains limited.

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- What form should explanations take for operators (natural language, causal graphs, counterfactual examples)?
- Can post-hoc explainability methods (SHAP, LIME) be effectively applied to trace-based anomaly detection?
- What countermeasure ontology would support automated recommendation (circuit breakers, scaling, rollback)?
