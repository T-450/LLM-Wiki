---
title: "Structural graphs built from system architecture outperform data-driven causal discovery for RCA graph construction"
slug: structural-graph-construction-outperforms-learned-causal
status: weakly_supported
confidence: 0.55
tags: [root-cause-analysis, causal-discovery, structural-graph, system-architecture, microservices]
domain: "ML Systems"
source_papers: [causal-inference-based-root-cause-analysis]
evidence:
  - source: causal-inference-based-root-cause-analysis
    type: supports
    strength: moderate
    detail: "On the Oracle database real-world dataset, CIRCA with the structural graph achieves AC@5=0.763, while random walk methods using PCTS (data-driven) achieve AC@5=0.449. For DFS-based methods, the structural graph consistently outperforms PC-gauss and PC-gsq (data-driven). The structural graph is also dramatically faster to construct (no runtime causal discovery needed). Ablation (Figure 7) shows structural graph improves AC@5 for DFS-based methods and CIRCA over data-driven alternatives. However, random walk methods (RW-Par, RW-2) achieve better results with PCTS than with the structural graph."
conditions: "Advantage demonstrated on Oracle database with 197 metrics. The structural graph requires manual classification of metrics to meta-metric dimensions (done once per metric type). Advantage may not generalize to domains without clear architecture documentation or where service topology is highly dynamic."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

For online service systems with documented architecture, a structural causal graph built from system architecture knowledge (using meta-metric causal assumptions: Traffic → Saturation → Latency → Errors, extended across call graph) produces more accurate RCA results than graphs learned from observational data via algorithms like PC, PCTS, or PC-gsq, especially when combined with regression-based scoring.

## Evidence summary

CIRCA (KDD 2022) evaluates structural graph vs. PC-gauss, PC-gsq, and PCTS on 197 Oracle database metrics (99 fault cases). CIRCA (structural + RHT + DA): AC@5=0.763. Best random walk with PCTS: AC@5=0.449. DFS with PC-gsq or PCTS: AC@5 near zero in the box plot. The structural graph avoids the small-sample causal discovery problem (few faults, many metrics), making it more reliable in practice. The mapping from metrics to meta-metrics can be shared across instances of the same system type, amortizing the manual effort.

## Conditions and scope

- Requires system architecture documentation (call graph) and expert knowledge of metric semantics
- One-time manual effort to classify metrics to Traffic/Saturation/Errors/Latency dimensions
- Most effective when combined with regression-based scoring (RHT); less clear advantage for random walk methods
- Data-driven methods (PCTS) work better for random walk methods on this dataset

## Counter-evidence

- Random walk methods (RW-Par, RW-2) achieve better AC@5 with PCTS (data-driven) than with the structural graph, suggesting the best graph construction method depends on the scoring approach
- MicroHECL constructs graphs from distributed traces automatically without architecture documentation, suggesting practical alternatives exist

## Linked ideas

## Open questions

- Can the structural graph construction be partially automated using LLMs that can parse architecture documentation?
- How does the structural graph perform in polyglot microservice environments where the TSEL meta-metric model may not apply uniformly?
- Is there a hybrid approach combining structural priors with data-driven refinement that outperforms either alone?
