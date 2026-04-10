---
title: "BARO: Robust Root Cause Analysis for Microservices via Multivariate Bayesian Online Change Point Detection"
slug: baro-robust-root-cause-analysis-microservices
arxiv: "2405.09330"
venue: "FSE"
year: 2024
tags: [root-cause-analysis, anomaly-detection, microservices, bayesian, change-point-detection, hypothesis-testing, nonparametric]
importance: 4
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [root-cause-analysis, anomaly-detection, microservices, bayesian-online-change-point-detection, nonparametric-hypothesis-testing, multivariate-time-series]
domain: "ML Systems"
code_url: "https://github.com/phamquiluan/baro"
cited_by: []
---

## Problem

Existing RCA methods for microservices either treat anomaly detection and root cause analysis independently, or rely on overly simplistic anomaly detection techniques (e.g., N-Sigma, BIRCH). Most RCA methods assume accurate knowledge of the failure occurrence time, but existing anomaly detectors frequently provide imprecise estimates. This inaccuracy in anomaly detection propagates errors into the RCA phase, degrading root cause localization. Additionally, many RCA methods require operational knowledge such as service call graphs or causal graphs, which are difficult to obtain in large-scale, evolving systems.

## Key idea

BARO is an end-to-end approach combining two key innovations: (1) Multivariate Bayesian Online Change Point Detection (BOCPD) for anomaly detection, which models the dependency and correlation structure of multivariate time-series metrics to detect distribution changes caused by failures, and (2) RobustScorer, a nonparametric statistical hypothesis testing technique that uses median and interquartile range (IQR) instead of mean and standard deviation to score potential root causes. The use of median/IQR makes RobustScorer inherently robust to imprecise anomaly detection times, since these statistics are resilient to outliers introduced by early or delayed detection.

## Method

1. **Multivariate BOCPD**: Combines Bayesian Online Change Point Detection with multivariate CPD to model dependencies among metrics. Uses run length modeling with multivariate Gaussian likelihood (inverse Wishart prior) to detect distribution changes. Only uses Latency and Error metrics for detection (following the four golden signals of SRE). Outputs the first detected change point as the estimated anomaly time.

2. **RobustScorer**: For each metric, learns the median and IQR from the normal period (before estimated anomaly time). For each data point in the anomalous period, computes deviation as $a^{(i,j)}_t = |x^{(i,j)}_t - \text{med}| / \text{IQR}$. The maximum deviation across the anomalous period becomes the metric's root cause score $\rho^{(i,j)}$. Metrics are ranked by $\rho$ in descending order. The approach is nonparametric, scale-equivalent, and rotation-invariant.

3. **Properties**: Unsupervised (no labeled data needed), does not require service call graphs or causal graphs, no user-specified thresholds for anomaly detection.

## Results

Evaluated on three benchmark microservice systems (Online Boutique: 12 services, Sock Shop: 11 services, Train Ticket: 64 services) with 100 failure cases each (4 fault types x 5 services x 5 repetitions).

**Anomaly detection**: BARO achieves the highest F1 scores across all three systems (0.82, 0.75, 0.81) compared to baselines N-Sigma (0.70, 0.72, 0.67), SPOT (0.69, 0.69, 0.67), BIRCH (0.40, 0.05, 0.39), and UniBCP (0.67, 0.66, 0.67).

**Coarse-grained RCA (Avg@5)**: BARO achieves 0.86, 0.95, 0.81 on the three systems, consistently outperforming CausalRCA (0.80, 0.60, 0.28), RCD (0.47-0.48, 0.45-0.48, 0.05-0.08), CIRCA (0.13-0.77, 0.20-0.95, 0.08-0.70), and epsilon-Diagnosis (0.12-0.24, 0.21-0.46, 0.01-0.07).

**Key finding**: BARO is the only method that consistently performs well across all three systems, including the large-scale Train Ticket system (64 services) where most baselines degrade severely.

## Limitations

- Only uses metric data (no logs or traces); future work plans to incorporate multimodal data
- Assumes anomalies are visible in Latency and Error metrics (following SRE golden signals)
- Assumes the first detected anomaly corresponds to the failure occurrence time
- Evaluated on synthetic fault injection in benchmark systems, not real production incidents
- Single deployment setting per system; limited generalizability analysis
- Cannot distinguish correlated failures from multi-root-cause scenarios (ranks affected services as top candidates but cannot identify the true underlying cause like a firewall misconfiguration)

## Open questions

- How does BARO perform with multimodal data (logs, traces) in addition to metrics?
- Can RobustScorer's robustness advantage be quantified theoretically (breakdown point analysis)?
- How does performance scale beyond 64 services to production systems with hundreds of services?
- Does the multivariate Gaussian assumption of BOCPD hold for all types of microservice metrics?

## My take

A well-executed paper with a simple but effective insight: using median/IQR instead of mean/std makes hypothesis testing robust to the very inaccuracies that plague the AD-RCA pipeline. The comprehensive evaluation on three benchmarks (especially Train Ticket with 64 services) is stronger than most RCA papers. The approach is refreshingly practical — unsupervised, no graph requirements, no thresholds. The main limitation is the metrics-only focus; real-world incidents often require log and trace analysis. Published at FSE 2024, which validates the contribution's significance.

## Related

- [[bayesian-online-change-point-detection]]
- [[causality-graph-rca]]
- [[anomaly-propagation-chain-analysis]]
- supports: [[nonparametric-rca-median-iqr-robust-imprecise]]
- supports: [[multivariate-bayesian-change-point-detection-outperforms]]
- supports: [[ad-rca-pipeline-gap]]
