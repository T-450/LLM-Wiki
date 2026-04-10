---
title: "Structured metric selection frameworks (Four Golden Signals, USE, RED) improve monitoring coverage over ad-hoc metric collection"
slug: structured-metric-selection-frameworks-improve-monitoring
status: weakly_supported
confidence: 0.55
tags: [metrics, observability, sre, cloud-native, monitoring, four-golden-signals, use-method]
domain: "ML Systems"
source_papers: [tracing-metrics-design-patterns-monitoring-cloud, monitoring-distributed-systems-google-sre]
evidence:
  - source: tracing-metrics-design-patterns-monitoring-cloud
    type: supports
    strength: moderate
    detail: "Paper advocates Four Golden Signals (latency, traffic, errors, saturation), RED (rate, errors, duration), READS, and USE method as structured starting points for metric selection; industry use cases (THRON using RED, GumGum using Prometheus exporters) demonstrate real-world adoption of these frameworks"
  - source: monitoring-distributed-systems-google-sre
    type: supports
    strength: strong
    detail: "Original source of the Four Golden Signals framework (Latency, Traffic, Errors, Saturation); argues these four signals are sufficient for any service as a minimal viable monitoring configuration. Validated across Google's production fleet."
conditions: "Frameworks serve as starting baselines; teams extend with domain-specific business metrics as needed. Effectiveness measured in terms of coverage of common failure modes, not absolute anomaly detection accuracy."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Using established metric selection frameworks (Google's Four Golden Signals for application health; Gregg's USE method for infrastructure resources; RED method for request-driven microservices) as starting points for instrumentation produces more systematic, complete monitoring coverage than purely ad-hoc or tool-driven metric collection.

## Evidence summary

[[tracing-metrics-design-patterns-monitoring-cloud]] formalizes these frameworks as design pattern guidance backed by industry known-use cases. The USE method is credited with forcing teams to enumerate resources before selecting metrics — improving systematic coverage. THRON's adoption of RED in production is cited as a known use. Evidence is primarily qualitative and practitioner-validated; no controlled empirical comparison exists in this paper.

## Conditions and scope

- Frameworks are starting points; teams should extend with business KPIs and domain-specific indicators
- USE method is most appropriate for infrastructure monitoring; RED/Four Golden Signals for application-level
- Applies to cloud-native microservice architectures; effectiveness in monolithic or serverless contexts may differ

## Counter-evidence

- Excessive metric collection (GumGum's node exporter with 600+ metrics) can introduce processing overhead that negates instrumentation benefits — frameworks may encourage over-collection
- The claim is hard to falsify without a controlled comparison baseline (what constitutes "ad-hoc"?)

## Linked ideas

## Open questions

- Which frameworks are most effective for ML/AI-serving microservices where behavior is non-deterministic?
- How should frameworks be adapted for serverless (FaaS) where traditional resource metrics are provider-managed?
