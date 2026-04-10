---
title: "Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data"
slug: eadro-end-end-troubleshooting-framework-microservices
arxiv: "2302.05092"
venue: "IEEE ISSRE"
year: 2023
tags: [anomaly-detection, root-cause-analysis, microservices, multi-modal, multi-task-learning, graph-neural-network]
importance: 4
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [microservices, root cause localization, anomaly detection, traces, logs, KPIs, multi-source data, multi-task learning, graph attention network]
domain: "ML Systems"
code_url: "https://github.com/BEbillionaireUSD/Eadro"
cited_by: []
---

## Problem

Troubleshooting microservice systems requires both anomaly detection (AD) and root cause localization (RCL), but existing approaches suffer from two limitations: (1) they rely almost exclusively on traces, which cannot reveal all anomaly types (e.g., CPU exhaustion does not cause obvious latency anomalies); (2) they treat AD and RCL as independent stages, where oversimplified anomaly detectors (e.g., N-sigma) introduce noisy labels that degrade downstream RCL accuracy. No prior work jointly addresses both tasks using multi-source monitoring data.

## Key idea

Integrate anomaly detection and root cause localization into a single end-to-end framework that fuses three data modalities — traces, system logs, and KPIs — via multi-task learning. The key insights are: (1) different data sources manifest different anomaly types (traces capture network issues, KPIs capture resource exhaustion, logs capture event-level anomalies); (2) AD and RCL share fundamental knowledge about microservice status that can be exploited via joint training with a shared objective.

## Method

Eadro has three components:

1. **Modal-wise learning**: modality-specific encoders learn intra-service behavior representations. Logs are parsed via Drain into event sequences, modeled with a Hawkes process (self-exciting point process) to capture event occurrence patterns, then embedded via an FC layer. KPIs (7 metrics per service) and trace latency time series are each processed by dilated causal convolution (DCC) layers followed by self-attention.

2. **Dependency-aware status learning**: multi-modal representations are fused via concatenation + FC projection + Gated Linear Unit (GLU), then fed into a Graph Attention Network (GAT) operating on the service dependency graph (extracted from historical traces). Global attention pooling produces a system-wide status representation.

3. **Joint detection and localization**: a shared representation feeds both a binary anomaly detector (BCE loss) and a root cause localizer (cross-entropy over service probabilities). The joint objective is $\mathfrak{L} = \beta \cdot \mathfrak{L}_1 + (1-\beta) \cdot \mathfrak{L}_2$. If no anomaly is detected, localization is skipped.

## Results

Evaluated on two benchmark microservice systems: TrainTicket (41 services) and SocialNetwork (21 services), with three injected fault types (CPU exhaustion, network jam, packet loss).

- **Anomaly detection**: F1 = 0.989 / 0.986 on the two datasets, improving over SOTA baselines by 53.82%-92.68% in F1
- **Root cause localization**: HR@1 = 0.990 / 0.974, improving over trace-based baselines by 290%-5068% and over derived multi-source methods by 26.93%-66.16%
- **Ablation study**: all three data sources contribute; removing KPIs or traces causes the largest HR@1 drops (19-35%), removing logs causes a smaller drop (6-7%), removing GAT (replacing with FC) drops HR@1 by ~19-23%

## Limitations

- Cannot detect logical bugs or silent issues that do not manifest in the three data modalities
- Requires all three data sources to be collected (though modal-wise learning is modular)
- Supervised approach requiring labeled training data (fault injection annotations)
- Evaluated only on simulated benchmark datasets with injected faults, not real production incidents
- Baseline reproduction threat: most baselines were reimplemented from papers without open-source code

## Open questions

- How does Eadro perform on real production incidents with complex, cascading failures?
- Can the supervised requirement be relaxed via semi-supervised or self-supervised pretraining?
- How does the framework scale to systems with hundreds or thousands of microservices?
- Can the Hawkes process log model be replaced with semantic-aware log analysis for richer signal?

## My take

First convincing demonstration that multi-source data fusion and joint AD+RCL training substantially outperform the traditional trace-only pipeline approach. The performance gains are dramatic, especially for HR@1 in root cause localization. The key insight — that different data modalities reveal different fault types — is well-motivated by the empirical analysis. Main weakness is evaluation on synthetic benchmarks only; real-world validation would significantly strengthen the claims. The modular modal-wise design is pragmatically useful since it degrades gracefully when some data sources are unavailable.

## Related

- [[multi-modal-observability-fusion]]
- [[log-based-anomaly-detection]]
- [[distributed-tracing]]
- [[causality-graph-rca]]
- [[monitoring-complexity-gap-distributed-systems]]
- supports: [[multi-source-data-improves-microservice-troubleshooting]]
- supports: [[joint-anomaly-detection-root-cause-localization]]
- supports: [[ad-rca-pipeline-gap]]
