---
title: "Regression-based hypothesis testing improves root cause localization accuracy over anomaly detection baselines"
slug: regression-based-hypothesis-testing-improves-rca
status: weakly_supported
confidence: 0.65
tags: [root-cause-analysis, hypothesis-testing, regression, anomaly-detection, online-service-systems]
domain: "ML Systems"
source_papers: [causal-inference-based-root-cause-analysis]
evidence:
  - source: causal-inference-based-root-cause-analysis
    type: supports
    strength: moderate
    detail: "RHT (regression-based hypothesis testing) scores each metric by comparing its observed value to its regression-predicted value conditioned on parent metrics in the CBN. In the Oracle database real-world evaluation (99 cases), RHT alone achieves AC@1=0.328 vs. NSigma baseline AC@1=0.323, a modest improvement. Adding descendant adjustment (CIRCA = RHT + DA) improves to AC@1=0.404 (+23% over NSigma). The key advantage is handling out-of-distribution faulty data by conditioning on parent metrics, avoiding spurious anomaly scores from correlated propagation effects."
  - source: baro-robust-root-cause-analysis-microservices
    type: contradicts
    strength: moderate
    detail: "BARO outperforms CIRCA on 3 benchmark systems using nonparametric hypothesis testing (median/IQR) rather than regression-based testing. BARO's RobustScorer does not require a causal graph, suggesting that simpler statistical approaches may match or exceed regression-based approaches in microservice settings."
conditions: "RHT advantage is clearest when parent-child metric relationships are well-captured by the structural graph and the regression model (SVR in practice). Performance improves significantly when combined with descendant adjustment. Evaluated on Oracle database data; generalization to other OSS types is not validated."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

By conditioning anomaly scoring on parent metrics in the Causal Bayesian Network via regression, regression-based hypothesis testing (RHT) avoids false positives from anomaly propagation — metrics that deviate from baseline because of upstream faults, not because they are the root cause. This produces more accurate root cause rankings than univariate anomaly detection methods that ignore causal structure.

## Evidence summary

CIRCA's ablation on the Oracle database dataset (99 real-world fault cases) shows: NSigma (univariate) AC@1=0.323; RHT alone AC@1=0.328; RHT + descendant adjustment (CIRCA) AC@1=0.404. The simulation study shows the theoretical advantage more clearly: RHT-PG outperforms all baselines by a large margin. The key mechanism is that conditioning on parent values removes propagation effects, isolating genuine distributional changes at the root cause metric. Case study shows CIRCA correctly ranks "log file sync" (true root cause) first while all non-causal baselines miss it in top-5.

## Conditions and scope

- Advantage strongest when structural graph is accurate
- SVR regression requires sufficient fault-free training data
- Assumes residuals are i.i.d. normally distributed — may not hold for all metric types
- Evaluated primarily on Oracle database metrics; behavior on microservice KPIs may differ

## Counter-evidence

- BARO (Ikram et al., 2024) shows nonparametric methods (no regression, no causal graph) can outperform CIRCA on microservice benchmarks
- RHT alone provides only marginal improvement over NSigma on the real-world Oracle dataset (+0.5% AC@1); the main gain comes from descendant adjustment, raising questions about which component drives accuracy

## Linked ideas

## Open questions

- Can more expressive regression models (e.g., neural networks) better approximate L1 and close the gap between RHT and RHT-PG?
- How sensitive is RHT to regression model misspecification?
- Is there a unified framework that combines the robustness of BARO's nonparametric approach with CIRCA's causal conditioning?
