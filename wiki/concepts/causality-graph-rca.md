---
title: "Causality Graph-Based Root Cause Analysis"
aliases: ["causality graph", "causal graph RCA", "topology graph analysis", "service dependency graph RCA"]
tags: [root-cause-analysis, causal-inference, graph-analysis, microservices, fault-localization]
maturity: active
key_papers: [anomaly-detection-failure-root-cause-analysis, eadro-end-end-troubleshooting-framework-microservices, microhecl-high-efficient-root-cause-localization, baro-robust-root-cause-analysis-microservices, causal-inference-based-root-cause-analysis]
first_introduced: "MonitorRank (Kim et al., 2013)"
date_updated: 2026-04-09
related_concepts: [distributed-tracing, log-based-anomaly-detection]
---

## Definition

Causality graph-based root cause analysis constructs a directed graph where vertices represent application services and directed edges represent causal relationships (an anomaly in the source service may cause an anomaly in the target service). The graph is then traversed using algorithms (random walk, BFS, PageRank) to identify the most probable root cause services for an observed anomaly.

## Intuition

When a failure occurs in a microservice system, it propagates along service dependency chains. By building a graph of these causal dependencies and analyzing which services show correlated anomalies, we can trace back from the observed symptom to the originating fault — much like following a chain of dominoes back to the first one that fell.

## Formal notation

Given a causality graph $G = (V, E, w)$ where $V$ is the set of services, $E \subseteq V \times V$ represents causal dependencies, and $w: E \to \mathbb{R}^+$ represents dependency strength (often derived from Granger causality tests or correlation analysis). Root cause identification involves finding $v^* = \arg\max_{v \in V} score(v)$ where $score$ is computed via graph traversal (e.g., personalized PageRank starting from the anomalous service).

## Variants

- **Random walk / PageRank** (MonitorRank): personalized PageRank on topology graph, weighted by performance metric correlation
- **BFS propagation chain** (MicroHECL): breadth-first search along anomaly propagation directions (callee-to-caller for latency, caller-to-callee for throughput)
- **Granger causality** (Aggarwal et al.): temporal causal modeling on multivariate time series of error logs
- **Bayesian network** (CIRCA): causal Bayesian network with intervention recognition

## Comparison

| Method | Graph construction | Traversal | Anomaly type |
|--------|-------------------|-----------|--------------|
| MonitorRank | From traces (periodic) | Personalized PageRank | Application-level performance |
| MicroHECL | From traces (windowed) | BFS with ML anomaly check | Service-level performance |
| Aggarwal et al. | Granger causality on logs | Random walk scoring | Frontend functional |
| CloudRanger | From monitoring + PC algorithm | Random walk with second-order | Service-level performance |

## When to use

- When service topology is available or can be inferred from traces
- When anomalies propagate along known dependency chains
- When determining which of multiple anomalous services is the originating cause

## Known limitations

- Accuracy depends on the completeness and correctness of the inferred topology graph
- Static topology graphs may not reflect dynamic service interactions
- Random walk methods can be sensitive to graph structure and initial conditions
- Assumes anomaly propagation follows dependency edges (may miss indirect causes)

## Open problems

- Handling dynamic, evolving service topologies in real-time
- Multi-root-cause scenarios where multiple independent faults co-occur
- Incorporating heterogeneous evidence (logs + traces + metrics) into graph edge weights
- Scaling to systems with thousands of services

## Key papers

- [[anomaly-detection-failure-root-cause-analysis]] — survey covering graph-based RCA techniques including MonitorRank, MicroHECL, CloudRanger, and CauseInfer
- [[eadro-end-end-troubleshooting-framework-microservices]] — applies GAT on service dependency graphs built from traces for dependency-aware root cause localization
- [[microhecl-high-efficient-root-cause-localization]] — BFS propagation chain traversal with type-specific anomaly detection and correlation-based pruning, deployed at Alibaba

- [[baro-robust-root-cause-analysis-microservices]] — proposes an alternative to graph-based RCA: nonparametric hypothesis testing (RobustScorer) that does not require service topology or causal graphs, outperforming graph-based methods (CausalRCA, RCD, CIRCA) on 3 benchmarks
- [[causal-inference-based-root-cause-analysis]] — introduces CIRCA: formal Causal Bayesian Network with intervention recognition criterion; structural graph built from system architecture; regression-based hypothesis testing conditioned on parent metrics in CBN

## My understanding

The dominant paradigm for RCA in microservices. The key insight is that service dependency graphs encode the "failure propagation highway" — traversing this graph with the right scoring function localizes root causes. The main challenge is building accurate, up-to-date graphs in dynamic environments. MicroHECL's deployment at Alibaba (68% top-3 hit ratio) validates practical viability.
