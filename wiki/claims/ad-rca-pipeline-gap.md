---
title: "Most anomaly detection and RCA techniques are developed independently, creating a pipeline integration gap"
slug: ad-rca-pipeline-gap
status: supported
confidence: 0.8
tags: [anomaly-detection, root-cause-analysis, microservices, pipeline, integration]
domain: "ML Systems"
source_papers: [anomaly-detection-failure-root-cause-analysis, eadro-end-end-troubleshooting-framework-microservices, microhecl-high-efficient-root-cause-localization]
evidence:
  - source: anomaly-detection-failure-root-cause-analysis
    type: supports
    strength: strong
    detail: "Survey of 30+ techniques finds that most address either detection or RCA in isolation; only a few (TraceAnomaly, Seer) provide integrated pipelines. The survey explicitly catalogs which detection outputs are compatible with which RCA inputs."
  - source: eadro-end-end-troubleshooting-framework-microservices
    type: supports
    strength: strong
    detail: "Eadro demonstrates the pipeline gap empirically: existing localization-oriented detectors (N-sigma, FE+ML, SPOT) have false omission rates of 0.63-0.83, injecting massive noise into downstream RCL. Eadro's end-to-end approach closing this gap achieves HR@1=0.982 vs 0.001-0.273 for pipeline baselines."
  - source: baro-robust-root-cause-analysis-microservices
    type: supports
    strength: strong
    detail: "BARO demonstrates the pipeline gap empirically: combining existing anomaly detectors (N-Sigma, SPOT, BIRCH, UniBCP) with existing RCA methods (RCD, CIRCA, epsilon-Diagnosis) yields highly variable and often poor results. BARO's end-to-end approach with Multivariate BOCPD + RobustScorer consistently outperforms all pipeline combinations across 3 benchmark systems."
conditions: "Applies to techniques surveyed up to 2021; more recent end-to-end frameworks (e.g., Eadro, BARO) have begun addressing this gap. MicroHECL (2021) partially addresses this by integrating type-specific detection within the RCA pipeline."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

The majority of existing anomaly detection and root cause analysis techniques for microservice-based cloud applications are developed as standalone solutions, not as components of an integrated diagnostic pipeline. This creates a practical gap for operators who must manually compose compatible detection and analysis techniques, matching anomaly type granularity and data format requirements.

## Evidence summary

The Soldani & Brogi (2022) survey systematically catalogs 30+ techniques and explicitly identifies pipeline compatibility between detection and RCA methods. The survey finds that only a handful of techniques (TraceAnomaly, Seer) provide both detection and RCA in an integrated pipeline. Most techniques require different instrumentation (logs vs. traces vs. monitoring agents) and produce outputs at different granularity levels (application-level vs. service-level), complicating integration.

## Conditions and scope

This claim is strongest for the 2013-2021 period covered by the survey. Post-2021 work has increasingly addressed integration (e.g., Eadro's end-to-end framework), though the fundamental challenge of matching detection and RCA granularity persists.

## Counter-evidence

- Eadro (2023) and BARO (2024) demonstrate end-to-end approaches, suggesting the gap is narrowing.
- MicroHECL (2021) integrates type-specific anomaly detection directly into the RCA graph traversal, partially bridging the detection-localization gap within its pipeline.

## Linked ideas

## Open questions

- What is the minimum set of shared abstractions (data formats, anomaly types) needed for plug-and-play pipeline composition?
- Does tighter integration improve diagnostic accuracy, or do modular pipelines offer better flexibility?
