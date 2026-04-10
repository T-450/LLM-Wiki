---
title: "Anomaly Detection in Cloud-Native Systems"
tags: [anomaly-detection, cloud-native, microservices, time-series, multi-modal, fault-detection]
my_involvement: none
sota_updated: 2026-04-09
key_venues: [ICSE, FSE, ASE, ISSRE, KDD, ICDM]
related_topics: [observability-foundations-distributed-systems, root-cause-analysis-microservices, observability-engineering-tooling]
key_people: [jacopo-soldani]
---

## Overview

Anomaly detection in cloud-native systems focuses on identifying abnormal behavior in microservice applications from observability data. The proliferation of services and their interactions creates high-dimensional monitoring data streams where anomalies may manifest subtly across multiple signals. Techniques range from statistical methods and threshold-based alerting to deep learning approaches that model temporal dependencies and inter-service relationships. A key trend is the integration of multiple data modalities — traces, logs, and KPIs — to capture different facets of system behavior, as single-source approaches often miss anomalies that manifest only in specific signal types.

## Timeline

- **2015-2018**: Statistical and threshold-based approaches dominate; focus on single-signal detection
- **2019-2021**: ML-driven methods emerge; survey work catalogs the landscape
- **2021**: Soldani & Brogi publish comprehensive survey covering anomaly detection and RCA techniques
- **2023-2024**: Multi-modal approaches gain traction; end-to-end frameworks emerge
- **2026**: AnoMod dataset provides first comprehensive multi-modal benchmark

## Seminal works

- [[anomaly-detection-failure-root-cause-analysis]] — comprehensive survey of the field
- [[eadro-end-end-troubleshooting-framework-microservices]] — multi-source anomaly detection integrated with RCA
- [[baro-robust-root-cause-analysis-microservices]] — Multivariate Bayesian Online CPD for robust anomaly detection

## SOTA tracker

| Aspect | Current state | Reference |
|--------|--------------|-----------|
| Survey coverage | 100+ techniques catalogued | [[anomaly-detection-failure-root-cause-analysis]] |
| Multi-modal detection | Traces + logs + KPIs fusion | [[eadro-end-end-troubleshooting-framework-microservices]] |
| Bayesian detection | Multivariate Bayesian Online CPD | [[baro-robust-root-cause-analysis-microservices]] |
| Benchmarks | AnoMod (2026): 4 anomaly categories, 5 modalities | AnoMod paper |

## Open problems

- Reducing false positive rates without missing critical anomalies
- Handling concept drift as service behavior evolves over time
- Scalable detection across hundreds of services and thousands of metrics
- Lack of standardized, realistic benchmarks with multi-modal data
- Unsupervised methods that work without labeled anomaly data

## My position

Essential prerequisite for effective RCA. The quality of anomaly detection directly impacts downstream diagnostic capabilities.

## Research gaps

- Limited understanding of which anomaly types are best captured by which data modalities
- Few studies on the trade-off between detection latency and accuracy
- Transfer learning for anomaly detection across different microservice deployments
- Integration of domain knowledge (architecture, SLOs) into detection models

## Key people

- [[jacopo-soldani]]
- [[michael-lyu]]
