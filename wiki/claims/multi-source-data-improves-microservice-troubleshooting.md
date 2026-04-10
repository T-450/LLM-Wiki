---
title: "Multi-source observability data (traces + logs + KPIs) substantially improves microservice troubleshooting over trace-only approaches"
slug: multi-source-data-improves-microservice-troubleshooting
status: weakly_supported
confidence: 0.65
tags: [anomaly-detection, root-cause-analysis, multi-modal, microservices, observability]
domain: "ML Systems"
source_papers: [eadro-end-end-troubleshooting-framework-microservices]
evidence:
  - source: eadro-end-end-troubleshooting-framework-microservices
    type: supports
    strength: strong
    detail: "Eadro achieves F1=0.988 for AD and HR@1=0.982 for RCL using traces+logs+KPIs, vastly outperforming trace-only baselines (53-93% F1 improvement, 290-5068% HR@1 improvement). Ablation confirms each modality contributes: removing KPIs drops HR@1 by 19-35%, removing traces by 21-35%, removing logs by 6-7%."
conditions: "Demonstrated on two synthetic benchmark microservice systems (TrainTicket, SocialNetwork) with three injected fault types. Generalization to production environments with diverse failure modes is not yet validated."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Combining multiple observability data sources — distributed traces, system logs, and key performance indicators (KPIs/metrics) — for microservice anomaly detection and root cause localization yields substantially better diagnostic accuracy than approaches relying on traces alone. Different data modalities capture complementary fault signatures: traces are sensitive to network-related latency issues, KPIs capture resource exhaustion (CPU, memory), and logs capture event-level anomalies through occurrence pattern changes.

## Evidence summary

Eadro (Lee et al., 2023) provides the strongest evidence, demonstrating on two benchmark systems that multi-source fusion outperforms all trace-only baselines by large margins on both anomaly detection and root cause localization. The ablation study confirms that each data source contributes meaningfully, with KPIs and traces providing the largest individual contributions.

## Conditions and scope

- Validated only on synthetic benchmarks with injected faults (CPU exhaustion, network jam, packet loss)
- Requires all three data sources to be available and collected at sufficient granularity
- The relative contribution of each modality may vary by fault type distribution and system architecture

## Counter-evidence

None currently documented. However, the lack of real-production validation is a significant limitation.

## Linked ideas

## Open questions

- Does the multi-source advantage hold when data collection is incomplete or noisy (as common in production)?
- What is the minimum set of KPIs needed for meaningful improvement over trace-only approaches?
- How does the advantage vary across different microservice architectures and fault type distributions?
