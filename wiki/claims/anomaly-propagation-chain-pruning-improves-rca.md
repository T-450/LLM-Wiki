---
title: "Anomaly propagation chain pruning improves RCA efficiency without accuracy loss"
slug: anomaly-propagation-chain-pruning-improves-rca
status: weakly_supported
confidence: 0.6
tags: [root-cause-analysis, pruning, efficiency, microservices, anomaly-propagation]
domain: "ML Systems"
source_papers: [microhecl-high-efficient-root-cause-localization]
evidence:
  - source: microhecl-high-efficient-root-cause-localization
    type: supports
    strength: moderate
    detail: "Pruning with Pearson correlation threshold 0.7 reduces execution time from 75s to 46s (39% reduction) while maintaining HR@3=0.67 on 75 real availability issues from Alibaba. Accuracy remains stable for thresholds 0-0.7, then drops for higher thresholds."
conditions: "Demonstrated on Alibaba e-commerce system with threshold 0.7. The optimal threshold may vary for different systems and anomaly type distributions."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Correlation-based pruning of anomaly propagation chains — eliminating branches where successive service call edges show low metric correlation — significantly improves RCA efficiency (execution time) without degrading localization accuracy, up to an empirically determined threshold.

## Evidence summary

MicroHECL (Liu et al., 2021) evaluates pruning on 75 availability issues from 28 Alibaba subsystems. With correlation threshold 0.7, HR@3 remains at 0.67 (identical to no pruning) while execution time decreases from 75s to 46s. This confirms that many branches explored without pruning are irrelevant to the actual root cause. Beyond threshold 0.7, accuracy begins to degrade as legitimate propagation paths are also pruned.

## Conditions and scope

- Evaluated on a single production system (Alibaba e-commerce) with specific anomaly type distribution
- Only one pruning mechanism tested (Pearson correlation of successive edge metrics)
- Threshold 0.7 is empirically optimal for this dataset — generalizability to other systems is unvalidated

## Counter-evidence

None directly. However, the technique has only been validated on one system.

## Linked ideas

## Open questions

- Is the optimal pruning threshold consistent across different microservice architectures and scales?
- Can adaptive pruning thresholds (learned per-system or per-anomaly-type) further improve the efficiency-accuracy tradeoff?
- Does pruning interact with multi-root-cause scenarios (potentially pruning one root cause's propagation path)?
