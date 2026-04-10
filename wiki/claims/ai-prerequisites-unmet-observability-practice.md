---
title: "AI/ML prerequisites for effective anomaly detection remain unmet in observability practice"
slug: ai-prerequisites-unmet-observability-practice
status: weakly_supported
confidence: 0.55
tags: [aiops, anomaly-detection, observability, data-quality, industry-practice]
domain: "ML Systems"
source_papers: [observability-monitoring-distributed-systems-industry-interview]
evidence:
  - source: observability-monitoring-distributed-systems-industry-interview
    type: supports
    strength: moderate
    detail: "Industry interviews reveal that while practitioners appreciate AI's potential for mastering complexity and data flood, sufficient preconditions are still missing: right data collection, data quality, context propagation, and central storage. Practitioners express concerns about cost-value ratio and reliability, with one stating 'I don't know if we will ever have a solution that we can rely on confidently.'"
conditions: "Based on 2019 interviews. Data infrastructure maturity may have improved since then, though the fundamental data quality challenge likely persists."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Despite the recognized potential of AI and ML techniques for anomaly detection and monitoring in distributed systems, the practical prerequisites -- correct data collection, data quality assurance, context propagation across services, and centralized data storage -- remain insufficiently addressed in industry practice. This creates a gap between AI/ML research capabilities and their effective deployment in production observability systems.

## Evidence summary

Niedermaier et al. (2019) found that almost all interview participants appreciated AI's potential for mastering monitoring complexity and data flood, but many pointed out that sufficient preconditions are still missing. Specifically: (1) the right data must be collected, (2) data quality must be ensured, (3) context must be propagated, and (4) data must be stored centrally. Cost-value concerns and reliability doubts further limit adoption.

## Conditions and scope

Based on 2019 data. The observability data infrastructure has matured significantly (OpenTelemetry, centralized observability platforms). However, the challenge of ensuring data quality and appropriate context for ML models likely remains relevant, especially for organizations earlier in their observability maturity.

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- What is the current state of AI/ML precondition readiness in industry observability practice (post-2023)?
- Can OpenTelemetry's standardized data model serve as a sufficient foundation for AI-driven anomaly detection?
- What minimum data quality thresholds are needed for effective ML-based anomaly detection?
