---
title: "Cross-Modal RCA Pipeline with Unified Anomaly Detection"
slug: cross-modal-rca-pipeline-unified-anomaly
status: proposed
origin: "AD-RCA pipeline gap identified in anomaly-detection-failure-root-cause-analysis survey; cross-modal fusion underexplored per root-cause-analysis-microservices topic"
origin_gaps:
  - ad-rca-pipeline-gap
  - root-cause-analysis-microservices
tags: [root-cause-analysis, anomaly-detection, multi-modal, cross-modal, microservices, pipeline]
domain: ML Systems
priority: 4
pilot_result: ""
failure_reason: ""
linked_experiments: []
date_proposed: 2026-04-09
date_resolved: ""
---

## Motivation

The survey ([[anomaly-detection-failure-root-cause-analysis]]) identifies a critical gap: AD and RCA techniques are almost always developed and evaluated independently, but production use requires a tightly integrated pipeline. When the AD component produces noisy alerts, RCA performance degrades catastrophically.

Eadro ([[eadro-end-end-troubleshooting-framework-microservices]]) shows that combining metrics, logs, and traces significantly improves both AD and RCA. But Eadro's fusion is architecture-specific (GNN + Hawkes process). A general, modular cross-modal fusion framework would allow components to be swapped and evaluated systematically.

## Hypothesis

A pipeline that jointly optimizes anomaly detection and root cause localization across metrics, logs, and traces — with learnable cross-modal attention — will outperform independent AD → RCA on MTTD and AC@K metrics, especially for cascading failures where the root cause's direct signal is weak.

## Approach sketch

1. **Unified representation**: embed metrics (time-series), logs (semantic vectors), traces (DAG features) into a shared latent space using modality-specific encoders
2. **Cross-modal attention**: learn attention weights between modalities at each service node in the dependency graph
3. **Joint training objective**: multi-task loss combining anomaly detection (binary) + root cause ranking (ListNet-style) — forcing the model to reason about both simultaneously
4. **Modular evaluation**: swap individual encoders to quantify contribution of each modality; test with simulated AD noise to measure pipeline robustness
5. **Baseline**: Eadro, MicroHECL, BARO (run independently then pipelined naively)

## Expected outcome

5–15% improvement in AC@3 over best independent baseline on public benchmarks (AIOPS, Sock Shop). More importantly: graceful degradation when one modality is unavailable (e.g., traces disabled) — the existing models fail silently in this scenario.

## Risks

- Joint training may be harder to converge than independent training; may need curriculum learning
- Public benchmarks lack sufficient incident diversity for cross-modal training
- Interpretability of cross-modal attention may be difficult to validate

## Pilot results

_Not yet run._

## Lessons learned

_Not yet run._
