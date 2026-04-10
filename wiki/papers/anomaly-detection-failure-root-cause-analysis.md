---
title: "Anomaly Detection and Failure Root Cause Analysis in (Micro)Service-Based Cloud Applications: A Survey"
slug: anomaly-detection-failure-root-cause-analysis
arxiv: "2105.12378"
venue: "ACM Computing Surveys (CSUR)"
year: 2022
tags: [anomaly-detection, root-cause-analysis, microservices, cloud-native, survey, distributed-tracing, log-analysis, monitoring]
importance: 5
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [log-based anomaly detection, root cause analysis, distributed tracing, service interaction monitoring, multi-service application failure diagnosis]
domain: "ML Systems"
code_url: ""
cited_by: [eadro-end-end-troubleshooting-framework-microservices]
---

## Problem

Modern multi-service (microservice-based) cloud applications consist of hundreds of interacting services, making it extremely difficult to detect failures and identify their root causes. Failures propagate along service dependency chains, manifesting as anomalies (symptoms) in multiple services simultaneously. Application operators face the concrete "pain" of monitoring distributed services, inspecting distributed logs, and understanding cascading failures. Existing solutions are scattered across different research communities, focusing on either anomaly detection or root cause analysis in isolation, with no unified view of how these techniques can be composed into end-to-end diagnostic pipelines.

## Key idea

The survey provides the first structured taxonomy that jointly covers anomaly detection and root cause analysis techniques for multi-service applications. It organizes techniques along three instrumentation axes: (1) log-based approaches that process native service logs, (2) distributed tracing-based approaches requiring trace instrumentation, and (3) monitoring-based approaches using installed agents. For each axis, the survey catalogs the ML methods used (unsupervised learning, supervised learning, statistical methods, graph-based analysis), the granularity of detection (application-level vs. service-level), and the setup costs. Crucially, it identifies which anomaly detection techniques can be pipelined with which RCA techniques based on compatible anomaly types and data requirements.

## Method

Systematic survey methodology covering 30+ techniques published between 2013 and 2021. The paper:
1. Defines clear terminology distinguishing failures, anomalies (symptoms), KPIs, service logs, application logs, and distributed traces
2. Classifies anomaly detection techniques into three categories by instrumentation type (log-based, distributed-tracing-based, monitoring-based) and further by ML approach
3. Classifies RCA techniques along the same three instrumentation axes, with sub-categories for visualization-based, direct analysis, topology graph-based, and causality graph-based methods
4. Provides recapping comparison tables for both anomaly detection (Table 1) and RCA (Table 2) techniques
5. Discusses cross-cutting concerns: setup costs, accuracy under dynamic changes, explainability, and countermeasure recommendation

## Results

- Identifies that most anomaly detection techniques require either distributed tracing or monitoring agent instrumentation; pure log-based approaches are rarer
- Shows that unsupervised learning dominates anomaly detection (avoids need for labeled failure data), while RCA techniques more commonly use graph-based analysis
- Reveals a critical gap: most techniques address either detection or RCA but not both; only a few (e.g., TraceAnomaly, Seer) provide integrated pipelines
- Highlights that technique accuracy degrades when services or runtime environments change over time, requiring costly retraining
- Finds that no technique provides explainability for its decisions or recommends countermeasures

## Limitations

- Qualitative comparison only; no quantitative benchmarking of surveyed techniques on common datasets
- Survey scope ends around 2021, missing more recent multi-modal and causal inference approaches
- Limited coverage of techniques from the cloud infrastructure provider perspective
- Does not address multi-root-cause scenarios in depth

## Open questions

- How can anomaly detection and RCA techniques be made robust to continuous changes in service deployments (continual learning)?
- Can explainable-by-design techniques be developed that provide human-interpretable reasons for detected anomalies and identified root causes?
- How can automated countermeasure recommendation be integrated into the detection-diagnosis pipeline?
- What would a standardized quantitative benchmark for comparing these techniques look like?
- Can false positive/negative rates be reduced without sacrificing detection coverage?

## My take

This is the seminal survey paper for the anomaly detection and RCA space in microservice systems. Its three-axis taxonomy (log/tracing/monitoring) provides a clean organizational framework that subsequent work has adopted. The most valuable insight is the pipeline compatibility analysis — showing which detection techniques can feed into which RCA techniques. The identified research gaps (explainability, countermeasures, continual learning) have driven much of the subsequent research in 2022-2026. The lack of quantitative comparison is a known limitation that Arya et al. (2021) partially addressed for RCA techniques.

## Related

- [[anomaly-detection-cloud-native-systems]]
- [[root-cause-analysis-microservices]]
- [[observability-foundations-distributed-systems]]
- [[log-based-anomaly-detection]]
- [[distributed-tracing]]
- [[causality-graph-rca]]
- supports: [[ad-rca-pipeline-gap]]
- supports: [[ml-retraining-cost-accuracy-tradeoff]]
- supports: [[explainability-gap-aiops]]
