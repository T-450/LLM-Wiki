---
title: "Joint end-to-end anomaly detection and root cause localization outperforms pipeline (separate) approaches"
slug: joint-anomaly-detection-root-cause-localization
status: weakly_supported
confidence: 0.6
tags: [anomaly-detection, root-cause-analysis, multi-task-learning, microservices, end-to-end]
domain: "ML Systems"
source_papers: [eadro-end-end-troubleshooting-framework-microservices]
evidence:
  - source: eadro-end-end-troubleshooting-framework-microservices
    type: supports
    strength: moderate
    detail: "Eadro's joint multi-task learning approach outperforms both pipeline baselines (separate AD then RCL) and derived multi-source methods without joint training. Motivation study shows existing detectors (N-sigma, FE+ML, SPOT) have high false omission rates (0.63-0.83) that inject noisy labels into downstream RCL. Joint training avoids this by sharing representations."
  - source: baro-robust-root-cause-analysis-microservices
    type: contradicts
    strength: moderate
    detail: "BARO achieves competitive or superior RCA performance to Eadro's end-to-end approach using a modular (non-joint) pipeline where anomaly detection and RCA are separate components. BARO's robustness comes from statistical design (median/IQR) rather than joint training, suggesting that robust modular designs can match end-to-end approaches."
conditions: "Demonstrated with Eadro's specific architecture (DCC+Hawkes+GAT with shared loss). The benefit of joint training vs. the benefit of multi-source data is not fully disentangled. BARO (2024) challenges this with a robust modular approach."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Training anomaly detection and root cause localization jointly in an end-to-end model, sharing representations and objectives, outperforms the conventional pipeline approach where detection and localization are performed by separate, independently trained systems. The pipeline approach suffers from error propagation: inaccurate anomaly detectors introduce noisy labels that degrade downstream localization.

## Evidence summary

Eadro (Lee et al., 2023) demonstrates that existing localization-oriented anomaly detectors (N-sigma, FE+ML, SPOT) have high false omission rates (0.63-0.83) and false discovery rates (0-0.42), introducing substantial noise into the localization phase. Eadro's joint training with multi-task loss achieves near-perfect detection (F1=0.988) and localization (HR@1=0.982), outperforming all compared pipeline approaches. The derived multi-source baselines (MS-LSTM, MS-DCC) that also use joint learning outperform non-joint multi-source baselines (MS-RF, MS-SVM), providing partial evidence for the joint learning benefit.

## Conditions and scope

- The benefit of joint training is partially confounded with the benefit of multi-source data and deep learning in Eadro's evaluation
- Applies to supervised settings with labeled fault data; unclear if the advantage holds in unsupervised scenarios
- Evaluated on two synthetic benchmarks; generalization to production systems is unvalidated

## Counter-evidence

- BARO (2024) achieves strong RCL performance with a modular Bayesian approach, suggesting that robust modular designs may be competitive with end-to-end approaches.
- MicroHECL (2021) achieves strong results (HR@3=0.67) with a pipeline approach that integrates type-specific detection into graph traversal but trains detection and localization independently, suggesting tight integration within a pipeline can be effective without joint training.

## Linked ideas

## Open questions

- Can the joint training benefit be cleanly disentangled from the multi-source data benefit?
- Does the advantage of joint training persist when the anomaly detector is already highly accurate?
- How does joint training affect model interpretability compared to modular pipeline approaches?
