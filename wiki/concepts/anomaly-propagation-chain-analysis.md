---
title: "Anomaly Propagation Chain Analysis"
aliases: ["anomaly propagation chain", "fault propagation chain analysis", "anomaly chain tracing", "propagation chain RCA"]
tags: [root-cause-analysis, microservices, fault-propagation, graph-traversal, anomaly-detection]
maturity: active
key_papers: [microhecl-high-efficient-root-cause-localization, baro-robust-root-cause-analysis-microservices, causal-inference-based-root-cause-analysis]
first_introduced: "MicroHECL (Liu et al., 2021)"
date_updated: 2026-04-09
related_concepts: [causality-graph-rca, distributed-tracing]
---

## Definition

Anomaly propagation chain analysis is a root cause localization technique that identifies the originating fault service by tracing the path of anomaly propagation through a service call graph. Starting from the initially reported anomalous service, the analysis traverses the graph along edges consistent with the propagation direction of each anomaly type, building chains of anomalous services. The endpoints of these chains (services where no further anomalous upstream/downstream services are found) are reported as candidate root causes.

## Intuition

When a downstream service experiences a latency spike, that spike propagates upstream to its callers, creating a chain of degraded services. By following this chain backward — from the observed symptom through each anomalous link — we can trace back to the service where the anomaly originated. The key insight is that different anomaly types propagate in different directions: performance and reliability issues propagate downstream-to-upstream (callee problems affect callers), while traffic anomalies propagate upstream-to-downstream (a caller routing issue affects callees).

## Formal notation

Given a service call graph $G = (V, E)$ with initial anomalous service $s_0 \in V$, for each anomaly type $t \in \{performance, reliability, traffic\}$ with propagation direction $d_t$:
1. For each neighbor $s_1$ of $s_0$ consistent with $d_t$: if $anomaly_t(s_0 \leftrightarrow s_1)$, start chain $C = [s_0, s_1]$
2. Iteratively extend: for each $s_k$ at chain end, find neighbors $s_{k+1}$ along $d_t$ where $anomaly_t(s_k \leftrightarrow s_{k+1})$ and $corr(metrics(s_{k-1}, s_k), metrics(s_k, s_{k+1})) \geq \theta$
3. Report chain endpoints as candidate root causes, ranked by correlation with business metrics

## Variants

- **Basic propagation chain** (MicroHECL): BFS extension with type-specific anomaly detection and Pearson correlation pruning
- **Random walk propagation** (MonitorRank): probabilistic traversal using PageRank-style scoring — explores more broadly but less efficiently
- **Causal propagation** (CIRCA): uses causal Bayesian networks instead of correlation to determine propagation paths

## Comparison

| Feature | Propagation chain (MicroHECL) | Random walk (MonitorRank) | Causal inference (CIRCA) |
|---------|-------------------------------|---------------------------|--------------------------|
| Traversal | Directed BFS with pruning | Random walk over full graph | Bayesian network inference |
| Anomaly detection | Type-specific (RF, OC-SVM, rules) | Correlation with front-end | Statistical tests |
| Pruning | Correlation-based edge pruning | None | Intervention recognition |
| Scalability | Linear (with pruning) | Quadratic in practice | Depends on graph structure |

## When to use

- When service call graph is available and anomalies propagate along call dependencies
- When different anomaly types need to be distinguished (performance vs. reliability vs. traffic)
- When efficiency is critical (large-scale systems with hundreds of services)

## Known limitations

- Assumes anomalies propagate strictly along call graph edges — misses indirect causation
- Single propagation direction per anomaly type is a simplification (mixed propagation patterns exist)
- Pruning threshold must be empirically tuned per deployment
- Cannot handle multi-root-cause scenarios where chains from different root causes overlap

## Open problems

- Extending to multi-root-cause scenarios with overlapping propagation chains
- Adaptive pruning thresholds that adjust to system characteristics
- Incorporating non-call-graph causal relationships (e.g., shared resource contention)

## Key papers

- [[microhecl-high-efficient-root-cause-localization]] — introduces the concept and demonstrates it at Alibaba scale with type-specific detection and correlation-based pruning
- [[baro-robust-root-cause-analysis-microservices]] — leverages the failure propagation chain assumption (first anomaly approximates failure time) for anomaly detection via Multivariate BOCPD

## My understanding

A practical and efficient approach to RCA that encodes domain knowledge about anomaly propagation directions. The pruning strategy is the key innovation — it converts what would be exponential graph exploration into a focused, linear-time search. The main conceptual limitation is the assumption of clean, directed propagation along call edges, which may not hold in complex failure scenarios.
