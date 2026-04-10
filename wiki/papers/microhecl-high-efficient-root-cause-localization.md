---
title: "MicroHECL: High-Efficient Root Cause Localization in Large-Scale Microservice Systems"
slug: microhecl-high-efficient-root-cause-localization
arxiv: "2103.01782"
venue: "ICSE-SEIP"
year: 2021
tags: [root-cause-analysis, microservices, anomaly-detection, service-call-graph, anomaly-propagation, pruning, industrial-deployment]
importance: 4
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [microservice, availability, root-cause-localization, anomaly-detection, service-call-graph, anomaly-propagation-chain, pruning-strategy]
domain: "ML Systems"
code_url: ""
cited_by: []
---

## Problem

Large-scale industrial microservice systems (e.g., Alibaba's e-commerce system with 30,000+ services) suffer from availability issues caused by service anomalies that propagate along dependency chains. When an availability issue is detected (e.g., drop in successful orders), the root cause service and anomaly type must be located within minutes. Existing approaches are limited by: (1) inaccurate anomaly detection that treats all anomaly types uniformly, and (2) inefficient graph traversal that explores irrelevant branches in large service dependency graphs.

## Key idea

MicroHECL introduces a three-stage root cause localization pipeline operating on a dynamically constructed service call graph: (1) entry node analysis identifies neighboring anomalous services of the initially reported service, (2) anomaly propagation chain extension traces anomalies backward along propagation directions using type-specific anomaly detectors, and (3) candidate root cause ranking uses Pearson correlation between business metrics and quality metrics. The key innovations are type-specific anomaly detection models (separate models for performance/RT, reliability/EC, and traffic/QPS anomalies) and a correlation-based pruning strategy that eliminates irrelevant propagation branches by checking metric similarity between successive edges.

## Method

1. **Service Call Graph Construction**: Dynamically constructs a weighted directed graph from service calls in the last 30 minutes, with quality metrics (RT, EC, QPS) recorded per minute for the last 60 minutes. Uses Flink for real-time aggregation. Graph construction is on-demand and incremental — data is pulled only when a service call is reached during analysis.

2. **Anomaly Propagation Chain Analysis**:
   - *Entry node analysis*: For each neighboring service of the initial anomalous service, detect anomalies using type-specific models and check consistency with propagation direction (downstream-to-upstream for performance/reliability, upstream-to-downstream for traffic).
   - *Chain extension*: Iteratively extend chains by backtracking along the propagation direction, detecting anomalies at each step. End when no more anomalous nodes are found.
   - *Pruning*: Before adding a node to a chain, check Pearson correlation between the quality metric time series of the current edge and the adjacent edge. If below threshold (default 0.7), prune the branch.

3. **Type-Specific Anomaly Detection**:
   - *Performance (RT)*: Random Forest classifier trained on features extracted from RT time series (mean, std, percentiles).
   - *Reliability (EC)*: Rule-based detection combining 3-sigma on error counts with RT threshold (50ms) to filter normal fluctuations.
   - *Traffic (QPS)*: One-class SVM on QPS time series to detect both increases and decreases.

4. **Candidate Root Cause Ranking**: Rank candidate root causes by absolute Pearson correlation coefficient between the business metric of the initial anomalous service and the quality metric of each candidate.

## Results

- **Overall accuracy**: HR@1=0.48, HR@3=0.67, HR@5=0.72, MRR=0.58 — significantly outperforming MonitorRank (HR@3=0.40) and Microscope (HR@3=0.49) on 75 real availability issues from Alibaba.
- **By anomaly type**: Largest advantage for performance anomaly (HR@3=0.65 vs 0.30/0.46); smallest for traffic anomaly (HR@3=0.55 vs 0.36/0.46).
- **Efficiency**: 22.3% faster than Microscope, 31.7% faster than MonitorRank. Advantage grows with system size (significant when >250 services). Execution time scales linearly with service count.
- **Pruning effect**: Pruning with threshold 0.7 reduces execution time from 75s to 46s (39% reduction) while maintaining HR@3=0.67.
- **Production deployment**: Deployed at Alibaba for 5+ months, handled 600+ availability issues. HR@3=68% in production. Root cause localization time reduced from 30 minutes to 5 minutes (average 76 seconds for recommendations).

## Limitations

- Assumes single root cause per anomaly type per availability issue — does not handle multi-root-cause scenarios.
- Fixed time windows (30 min for graph, 60 min for metrics) may miss slowly accumulating anomalies.
- Detection models require labeled training data, which is expensive to obtain in production.
- HR@3 of 68% means 32% of cases still require manual investigation.
- Only handles three anomaly types (performance, reliability, traffic) — does not cover resource-level or infrastructure-level anomalies.
- Pruning threshold (0.7) is empirically set and may need tuning for different systems.

## Open questions

- How to extend to multi-root-cause scenarios where multiple independent faults co-occur?
- Can the approach be adapted for dynamically evolving service topologies where the call graph changes during analysis?
- How to combine MicroHECL's graph-based approach with trace-level and log-level analysis for more comprehensive diagnosis?
- Can the type-specific anomaly detection models be made self-adaptive to reduce dependence on labeled data?

## My take

A solid industrial contribution that demonstrates graph-based RCA at Alibaba scale. The key insights — type-specific anomaly detection and correlation-based pruning — are well-motivated by production data characteristics. The pruning strategy is particularly elegant: it provides a 39% speedup with zero accuracy loss at the optimal threshold. The main weakness is the single-root-cause assumption and fixed time windows. The paper's production deployment data (600+ incidents, 68% hit ratio, 30 min to 5 min reduction) provides strong evidence of practical value. This work establishes an important baseline for industrial-scale RCA.

## Related

- [[causality-graph-rca]] — core concept: graph-based traversal for root cause analysis
- [[anomaly-propagation-chain-analysis]] — concept introduced by this paper
- [[root-cause-analysis-microservices]] — parent topic
- [[anomaly-detection-cloud-native-systems]] — related topic
- supports: [[anomaly-propagation-chain-pruning-improves-rca]]
- supports: [[type-specific-anomaly-detection-improves-root]]
- supports: [[graph-based-rca-scales-linearly-service]]
- supports: [[ad-rca-pipeline-gap]]
- supports: [[joint-anomaly-detection-root-cause-localization]]
