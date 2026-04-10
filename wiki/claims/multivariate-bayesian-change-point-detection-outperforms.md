---
title: "Multivariate Bayesian change point detection outperforms univariate methods for microservice anomaly detection"
slug: multivariate-bayesian-change-point-detection-outperforms
status: weakly_supported
confidence: 0.6
tags: [anomaly-detection, bayesian, change-point-detection, multivariate, microservices]
domain: "ML Systems"
source_papers: [baro-robust-root-cause-analysis-microservices]
evidence:
  - source: baro-robust-root-cause-analysis-microservices
    type: supports
    strength: moderate
    detail: "Multivariate BOCPD achieves highest F1 scores (0.82, 0.75, 0.81) across three benchmark systems, outperforming univariate methods: N-Sigma (0.70, 0.72, 0.67), SPOT (0.69, 0.69, 0.67), BIRCH (0.40, 0.05, 0.39), and UniBCP (0.67, 0.66, 0.67). The improvement is attributed to modeling inter-metric dependencies caused by failure propagation chains."
conditions: "Demonstrated on three benchmark microservice systems (Online Boutique, Sock Shop, Train Ticket) with synthetic fault injection. All baselines are univariate or clustering-based methods."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Multivariate Bayesian Online Change Point Detection, which models the dependency and correlation structure among multiple time-series metrics, outperforms univariate anomaly detection methods (N-Sigma, SPOT, BIRCH, univariate BOCPD) for detecting failures in microservice systems. The advantage stems from capturing correlated distribution changes caused by failure propagation across services.

## Evidence summary

BARO (Pham et al., FSE 2024) demonstrates that Multivariate BOCPD achieves the highest precision and F1 scores across all three benchmark systems while maintaining perfect recall. The key advantage is higher precision — baseline methods frequently misclassify normal time series as anomalous, while the multivariate approach reduces false positives by modeling inter-metric dependencies.

## Conditions and scope

- Compared against four univariate/clustering baselines; no comparison with other multivariate deep learning detectors
- Evaluated on systems with 11-64 services; scalability to larger systems is untested
- The multivariate Gaussian assumption may not hold for all metric types

## Counter-evidence

None identified. However, the comparison set is limited to methods commonly used in RCA literature; more sophisticated multivariate deep learning detectors were not compared.

## Linked ideas

## Open questions

- How does Multivariate BOCPD compare to deep learning-based multivariate anomaly detectors (e.g., LSTM autoencoders, transformers)?
- Does the advantage scale with system size, or does the multivariate model become intractable for very large systems?
- How sensitive is the approach to the Gaussian assumption?
