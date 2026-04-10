---
title: "Nonparametric RCA using median/IQR is robust to imprecise anomaly detection time"
slug: nonparametric-rca-median-iqr-robust-imprecise
status: weakly_supported
confidence: 0.65
tags: [root-cause-analysis, nonparametric, hypothesis-testing, robustness, anomaly-detection]
domain: "ML Systems"
source_papers: [baro-robust-root-cause-analysis-microservices]
evidence:
  - source: baro-robust-root-cause-analysis-microservices
    type: supports
    strength: moderate
    detail: "BARO's RobustScorer uses median and IQR instead of mean and standard deviation for hypothesis testing. Sensitivity analysis shows RobustScorer maintains stable performance across different anomaly detection times, while baseline methods (N-Sigma, epsilon-Diagnosis, CIRCA) degrade significantly. Demonstrated on 3 benchmark systems with 300 failure cases total."
conditions: "Demonstrated on synthetic fault injection benchmarks (Online Boutique, Sock Shop, Train Ticket). The robustness advantage is empirical; no formal breakdown point analysis is provided."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Using median and interquartile range (IQR) instead of mean and standard deviation in nonparametric hypothesis testing for root cause analysis makes the RCA module robust to imprecise anomaly detection times. This is because median and IQR are resistant to outliers that are introduced when the estimated anomaly time is too early (limited normal data) or too late (abnormal data contaminates the normal period).

## Evidence summary

BARO (Pham et al., FSE 2024) demonstrates that RobustScorer, which uses median/IQR, consistently outperforms N-Sigma (mean/std-based) and other baseline RCA methods across three benchmark microservice systems. The sensitivity analysis specifically evaluates RCA performance as a function of anomaly detection time accuracy, showing RobustScorer maintains stable Avg@5 scores while baselines degrade.

## Conditions and scope

- Evaluated on metric-based RCA in microservice systems with synthetic fault injection
- The robustness is empirical; no formal statistical analysis of the breakdown point is provided
- Applies to the scenario where the anomaly detection time is the primary source of imprecision

## Counter-evidence

None identified so far. The statistical robustness of median/IQR to outliers is well-established in statistics literature.

## Linked ideas

## Open questions

- Can the robustness advantage be quantified theoretically (e.g., breakdown point of median vs. mean)?
- Does the advantage persist with very large detection time errors (e.g., minutes vs. seconds)?
- How does this interact with different anomaly detection methods beyond the ones tested?
