---
title: "Bayesian Online Change Point Detection"
aliases: ["BOCPD", "Bayesian change point detection", "online change point detection", "multivariate BOCPD"]
tags: [anomaly-detection, bayesian-inference, change-point-detection, time-series, microservices]
maturity: active
key_papers: [baro-robust-root-cause-analysis-microservices]
first_introduced: "Adams & MacKay (2007)"
date_updated: 2026-04-09
related_concepts: [log-based-anomaly-detection, anomaly-propagation-chain-analysis]
---

## Definition

Bayesian Online Change Point Detection (BOCPD) is a statistical method for identifying points in time-series data where the underlying data distribution changes significantly. It models the "run length" — the number of consecutive data points from the same distribution since the last change point — and uses Bayesian inference to compute the posterior probability of the run length at each time step. Change points are identified where the most probable run length decreases.

## Intuition

Imagine monitoring a stream of metrics from a running service. The data follows some pattern, and BOCPD keeps track of how long the current pattern has been going on. When a failure occurs, the pattern changes — BOCPD detects this by noticing that the "current segment length" suddenly drops to zero, signaling a new distribution has begun. The Bayesian framework naturally handles uncertainty about when exactly the change occurred.

## Formal notation

Given time-series data $\mathcal{M}_{t_0:t}$, the posterior probability of run length $r_t$ is:

$$p(r_t | \mathcal{M}_{t_0:t}) = \frac{\sum_{r_{t-1}} p(r_t | r_{t-1}) \cdot p(\mathcal{M}_t | r_{t-1}, \mathcal{M}^{(r)}) \cdot p(r_{t-1} | \mathcal{M}_{t_0:t-1})}{p(\mathcal{M}_{t_0:t})}$$

The conditional prior $p(r_t | r_{t-1})$ uses a hazard function with geometric distribution. The marginal likelihood uses an exponential family distribution (univariate) or multivariate Gaussian with inverse Wishart prior (multivariate extension).

## Variants

- **Univariate offline BOCPD** (Adams & MacKay, 2007): original formulation for univariate time series; used in CauseInfer for RCA
- **Multivariate BOCPD** (BARO, 2024): extends BOCPD with multivariate CPD (Xuan et al., 2007) to model dependencies among multiple metrics using multivariate Gaussian likelihood with inverse Wishart prior $\Sigma \sim IW(N_0, V_0)$

## Comparison

| Feature | BOCPD | N-Sigma | SPOT/dSPOT | BIRCH |
|---------|-------|---------|------------|-------|
| Multivariate | Yes (with extension) | No | No | No |
| Threshold-free | Yes | No (3-sigma) | No (EVT threshold) | No (cluster threshold) |
| Online | Yes | Yes | Yes | Yes |
| Models dependencies | Yes (multivariate) | No | No | No |

## When to use

- When detecting distribution changes in streaming multivariate time-series data
- When no labeled anomaly data is available (unsupervised)
- When modeling correlations between metrics is important (e.g., failure propagation in microservices)
- When threshold-free detection is desired

## Known limitations

- Multivariate Gaussian assumption may not hold for all metric types
- Computational cost scales with the number of time series in the multivariate case
- Sensitivity to the choice of prior parameters ($N_0$, $V_0$)
- Only detects distributional changes, not specific anomaly patterns

## Open problems

- Scaling multivariate BOCPD to systems with thousands of metrics
- Non-Gaussian extensions for heavy-tailed or discrete metric distributions
- Adaptive priors that learn from historical change points
- Integration with other detection paradigms (e.g., deep learning) for hybrid approaches

## Key papers

- [[baro-robust-root-cause-analysis-microservices]] — applies multivariate BOCPD for anomaly detection in microservices, achieving best F1 scores across three benchmark systems

## My understanding

A principled Bayesian approach to change point detection that is especially well-suited for microservice anomaly detection because it models inter-metric dependencies. The threshold-free nature is a major practical advantage over methods like N-Sigma and SPOT. The multivariate extension by BARO is the key innovation for microservices, where failure propagation creates correlated changes across metrics.
