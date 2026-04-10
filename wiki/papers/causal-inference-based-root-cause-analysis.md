---
title: "Causal Inference-Based Root Cause Analysis for Online Service Systems with Intervention Recognition"
slug: causal-inference-based-root-cause-analysis
arxiv: "2206.05871"
venue: "KDD 2022"
year: 2022
tags: [root-cause-analysis, causal-inference, intervention-recognition, bayesian-network, microservices, online-service-systems, hypothesis-testing]
importance: 4
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [root cause analysis, causal inference, intervention recognition, causal Bayesian network, structural graph, regression hypothesis testing, descendant adjustment]
domain: "ML Systems"
code_url: "https://github.com/NetManAIOps/CIRCA"
cited_by: [baro-robust-root-cause-analysis-microservices]
---

## Problem

Online service systems (OSS) generate massive monitoring data during failures. When a fault propagates through a microservice system, it triggers an "anomaly storm" — many metrics become abnormal simultaneously. Identifying a small set of root cause indicators from hundreds or thousands of monitoring metrics is essential for rapid failure mitigation. Prior work lacks a rigorous theoretical formulation connecting RCA to causal inference, relying instead on heuristic graph traversal and anomaly scoring.

A second key obstacle: faulty data are sparse (operators mitigate failures quickly) and may not overlap in distribution with fault-free data, making direct distribution comparison infeasible.

## Key idea

Map the RCA problem to a new causal inference task called **intervention recognition (IR)**: given observational distribution L1 and the interventional distribution Pm (observed during failure), find the intervened variables M (root causes). The Intervention Recognition Criterion (Theorem) shows that a metric Vi is a root cause iff its conditional distribution given parents in the Causal Bayesian Network (CBN) changes: P_m(Vi | pa(Vi)) ≠ L1(Vi | pa(Vi)). RCA thus requires Layer 2 (interventional) causal knowledge — not counterfactual (Layer 3).

This criterion is implemented in **CIRCA** (Causal Inference-based Root Cause Analysis), which combines: (1) a structural graph constructed from system architecture knowledge, (2) regression-based hypothesis testing (RHT) to compare distributions pointwise despite distributional overlap issues, and (3) descendant adjustment to reduce bias from incomplete L1 knowledge.

## Method

**Structural Graph Construction**: Monitoring metrics are classified into four meta-metrics from site reliability engineering: Traffic, Saturation, Errors, Latency (TSEL). Causal assumptions among these (e.g., Traffic → Saturation → Latency → Errors) provide a skeleton. The architecture call graph extends this across services: caller Traffic influences callee Traffic; callee Latency contributes to caller Latency; callee Errors propagate. Actual monitoring metrics are then plugged into corresponding meta-metric positions.

**Regression-Based Hypothesis Testing (RHT)**: A regression model (SVR in real-world experiments, linear in simulation) is trained per metric on fault-free data. During a failure, the anomaly score for metric Vi at time t is the normalized residual: a(t) = |(vi(t) - v̄i(t) - μ_ε) / σ_ε|. The final score s_Vi = max_t a(t).

**Descendant Adjustment**: When a metric and its parent are both anomalous, we prefer to attribute the root cause to the parent (actionable interpretation). Metrics with score ≥ 3 (three-sigma rule) are candidate root causes. Each candidate's score is boosted by the maximum score of its downstream descendants, propagating scores upward through the CBN.

## Results

**Simulation**: Three datasets (50/100/500 nodes). RHT with perfect graph (RHT-PG) approaches ideal performance and significantly outperforms all baselines (p < 0.001). On Dsim-50: AC@1=0.615, AC@5=0.952 vs. best baseline DFS: AC@1=0.541, AC@5=0.682. RHT-PG is robust to both weak and strong faults; baselines degrade significantly on strong faults.

**Real-world (Oracle database, 99 cases from a large banking system)**: CIRCA achieves AC@1=0.404, AC@5=0.763, Avg@5=0.603 — a 25% improvement in top-1 recall over the best baseline (NSigma: AC@1=0.323). Analysis completes in under 1 second per fault using the structural graph. Component ablation confirms all three techniques (structural graph, RHT, descendant adjustment) contribute positively.

## Limitations

- Structural graph construction requires manual mapping of metrics to meta-metrics; this is a one-time effort but requires domain expertise.
- Regression-based testing assumes i.i.d. normal residuals; this may not hold for all metric types.
- The Markovian assumption (no hidden common causes) may be violated when meta-metrics have no corresponding monitoring metrics, introducing confounding.
- Evaluated on Oracle database data only; generalization to multi-service microservice environments with hundreds of services is not demonstrated.
- The effectiveness of descendant adjustment has not been validated on additional real-world datasets beyond the Oracle case.

## Open questions

- Can faulty data be incorporated into regression training to improve L1 approximation?
- How does CIRCA perform when multiple simultaneous faults occur?
- How to automatically construct the structural graph without manual metric classification?
- Does the intervention recognition framework extend naturally to log and trace data (not just metrics)?

## My take

The most theoretically principled RCA paper in this wiki. The formulation of RCA as intervention recognition is elegant and fills a gap: previous work (Sage) implicitly assumed no interventions occur, which is logically inconsistent with fault diagnosis. The Intervention Recognition Criterion gives a provably sound basis for root cause scoring. The structural graph is a pragmatic solution to the causal discovery problem — rather than learning from data (which is noisy and unreliable for causal structure), it encodes engineering knowledge. The 25% top-1 improvement over best baselines on real data is meaningful. Main weakness: the evaluation is limited to Oracle databases; the microservice setting with many services is tested only in simulation.

## Related

- [[causality-graph-rca]] — CIRCA uses CBN as a special case; extends graph-based RCA with formal causal theory
- [[bayesian-online-change-point-detection]] — related approach for detecting distributional changes
- [[anomaly-propagation-chain-analysis]] — descendant adjustment relates to propagation chain reasoning
- supports: [[causal-bayesian-network-enables-intervention-based]]
- supports: [[regression-based-hypothesis-testing-improves-rca]]
- supports: [[structural-graph-construction-outperforms-learned-causal]]
