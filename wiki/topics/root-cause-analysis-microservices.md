---
title: "Root Cause Analysis in Microservices"
tags: [root-cause-analysis, microservices, fault-diagnosis, causal-inference, service-dependency-graph]
my_involvement: none
sota_updated: 2026-04-09
key_venues: [ICSE, FSE, ASE, ISSRE, WWW, KDD]
related_topics: [observability-foundations-distributed-systems, anomaly-detection-cloud-native-systems, observability-engineering-tooling]
key_people: [jacopo-soldani, michael-lyu, hongyu-zhang]
---

## Overview

Root cause analysis (RCA) in microservice systems addresses the challenge of automatically identifying the origin of failures in complex, distributed service topologies. When a fault occurs, it typically propagates along service dependency chains, manifesting as symptoms in multiple services simultaneously. RCA techniques analyze observability data — call graphs, performance metrics, logs, and traces — to trace anomalies back to their origin. Key approaches include graph-based traversal of service dependency graphs, causal inference using Bayesian networks, statistical hypothesis testing, and multi-modal data fusion. The field has matured from rule-based approaches to ML-driven methods with demonstrated industrial deployment (Alibaba, Microsoft).

## Timeline

- **2018-2019**: Early graph-based RCA methods for microservices emerge
- **2021**: MicroHECL deployed at Alibaba with 68% top-3 hit ratio, establishing industrial viability
- **2022**: CIRCA introduces causal inference (intervention recognition) for RCA
- **2023**: Eadro proposes first end-to-end framework integrating detection and localization
- **2024**: BARO demonstrates robustness to inaccurate anomaly detection via Bayesian methods
- **2025**: DynaCausal introduces dynamic causality modeling for evolving service topologies

## Seminal works

- [[microhecl-high-efficient-root-cause-localization]] — industrial-scale graph-based RCA
- [[causal-inference-based-root-cause-analysis]] — causal inference approach (CIRCA)
- [[eadro-end-end-troubleshooting-framework-microservices]] — end-to-end multi-source framework
- [[baro-robust-root-cause-analysis-microservices]] — Bayesian robust RCA

## SOTA tracker

| Method | Approach | Key metric | Reference |
|--------|----------|-----------|-----------|
| MicroHECL | Graph + correlation analysis | Top-3 hit: 68% (production) | [[microhecl-high-efficient-root-cause-localization]] |
| CIRCA | Causal Bayesian Network | +25% recall@1 over baselines | [[causal-inference-based-root-cause-analysis]] |
| Eadro | Multi-source multi-task learning | Outperforms SOTA on 2 benchmarks | [[eadro-end-end-troubleshooting-framework-microservices]] |
| BARO | Bayesian change-point detection | Best on 3 benchmark systems | [[baro-robust-root-cause-analysis-microservices]] |

## Open problems

- Sensitivity to anomaly detection accuracy (cascading errors from detection to localization)
- Handling dynamic, evolving service topologies and dependency graphs
- Scalability to systems with hundreds of services and high request volumes
- Multi-root-cause scenarios where multiple faults occur simultaneously
- Generalizability across different microservice architectures and deployment environments

## My position

Key research direction with strong practical impact. The coupling between anomaly detection and RCA is an important unsolved challenge.

## Research gaps

- Limited evaluation on real production incidents (most benchmarks are synthetic)
- Few methods handle concept drift in service behavior over time
- Cross-modal fusion for RCA remains underexplored relative to its potential
- No standardized evaluation protocol across RCA studies

## Key people

- [[jacopo-soldani]]
- [[michael-lyu]]
- [[hongyu-zhang]]
