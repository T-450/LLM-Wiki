---
title: "Type-specific anomaly detection improves root cause localization accuracy"
slug: type-specific-anomaly-detection-improves-root
status: weakly_supported
confidence: 0.6
tags: [anomaly-detection, root-cause-analysis, microservices, type-specific]
domain: "ML Systems"
source_papers: [microhecl-high-efficient-root-cause-localization]
evidence:
  - source: microhecl-high-efficient-root-cause-localization
    type: supports
    strength: moderate
    detail: "MicroHECL uses separate models for performance (Random Forest on RT), reliability (3-sigma + RT threshold on EC), and traffic (One-class SVM on QPS) anomalies, achieving HR@3=0.67 vs MonitorRank (0.40, single correlation-based detection) and Microscope (0.49, uniform 3-sigma detection). The advantage is largest for performance anomaly (HR@3 0.65 vs 0.30/0.46)."
conditions: "Compared against MonitorRank and Microscope on 75 Alibaba availability issues. The improvement is confounded with other MicroHECL innovations (pruning, propagation direction), so the isolated benefit of type-specific detection is unclear."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Using separate, specialized anomaly detection models tailored to different anomaly types (performance, reliability, traffic) improves root cause localization accuracy compared to applying a single uniform detection method across all anomaly types.

## Evidence summary

MicroHECL (Liu et al., 2021) designs customized models for three anomaly types — Random Forest for performance (RT), rule-based with threshold for reliability (EC), and One-class SVM for traffic (QPS) — based on observed statistical characteristics of each metric in production. This outperforms MonitorRank (single correlation-based approach) and Microscope (uniform 3-sigma rule) by 18-27 percentage points on HR@3. The paper argues that Microscope's uniform 3-sigma approach produces false positives from occasional fluctuations, while MonitorRank's correlation-based approach degrades with propagation distance.

## Conditions and scope

- The accuracy improvement is confounded with other MicroHECL components (pruning, directed propagation); no ablation isolates the detection model's contribution
- Only three anomaly types and three detection models were evaluated
- Applicability depends on having sufficient labeled data for supervised models (Random Forest)

## Counter-evidence

None directly.

## Linked ideas

## Open questions

- What is the isolated contribution of type-specific detection vs. other MicroHECL components?
- Can deep learning models (e.g., autoencoders, transformers) replace hand-designed type-specific models?
- Is three anomaly types sufficient, or would finer-grained types (e.g., CPU vs. memory vs. disk for performance) improve accuracy further?
