---
title: "Distributed Tracing"
aliases: ["distributed tracing", "request tracing", "trace-based monitoring", "end-to-end tracing"]
tags: [observability, distributed-systems, tracing, microservices, instrumentation]
maturity: stable
key_papers: [anomaly-detection-failure-root-cause-analysis, observability-monitoring-distributed-systems-industry-interview, eadro-end-end-troubleshooting-framework-microservices, informed-assessable-observability-design-decisions-cloud, tracing-metrics-design-patterns-monitoring-cloud, azure-monitor-application-insights-opentelemetry-overview, observability-engineering-majors-fong-jones-miranda, opentelemetry-observability-primer]
first_introduced: "Google Dapper (2010)"
date_updated: 2026-04-09
related_concepts: [log-based-anomaly-detection, causality-graph-rca]
---

## Definition

Distributed tracing is a method for profiling and monitoring multi-service applications by (1) assigning each user request a unique ID, (2) propagating this ID to all services involved in processing the request, (3) including the request ID in all log messages, and (4) recording timing information (start time, end time) about service invocations and internal operations. The resulting "traces" enable reconstructing the full request path across services.

## Intuition

When a user request enters a multi-service application, it triggers a chain of service-to-service calls. Distributed tracing stitches together the events from all these services into a single coherent narrative (trace) of what happened during request processing. This is essential for understanding latency, detecting failures, and performing root cause analysis in distributed systems.

## Formal notation

A trace $T = \{s_1, s_2, \ldots, s_n\}$ consists of spans, where each span $s_i = (id, parent\_id, service, op, t_{start}, t_{end}, tags)$ represents a unit of work. Spans form a directed acyclic graph via parent relationships, representing the causal structure of request processing.

## Variants

- **Context propagation-based** (W3C Trace Context): standard header-based propagation
- **eBPF-based** (non-invasive): kernel-level instrumentation without code changes
- **Sampling strategies**: head-based sampling, tail-based sampling, adaptive sampling

## Comparison

| Tracing approach | Code changes | Overhead | Coverage |
|-----------------|-------------|----------|----------|
| SDK instrumentation (OpenTelemetry) | Required | Low-medium | Full control |
| Auto-instrumentation | Minimal | Medium | Framework-dependent |
| eBPF-based | None | Low | Network-level only |

## When to use

- When understanding request flow across service boundaries is critical
- When diagnosing latency issues that span multiple services
- As input to automated anomaly detection and RCA pipelines
- When building service dependency topology graphs

## Known limitations

- Requires instrumentation effort across all services
- Sampling may miss rare anomalous traces
- Overhead increases with trace volume in high-throughput systems
- Cross-language/cross-framework instrumentation can be inconsistent

## Open problems

- Optimal sampling strategies that preserve anomalous traces
- Reducing instrumentation overhead in latency-sensitive paths
- Standardizing trace formats across heterogeneous technology stacks

## Key papers

- [[anomaly-detection-failure-root-cause-analysis]] — survey covering distributed tracing-based anomaly detection and RCA techniques
- [[observability-monitoring-distributed-systems-industry-interview]] — industry interview study documenting distributed tracing as a key but inconsistently adopted solution
- [[eadro-end-end-troubleshooting-framework-microservices]] — uses trace latency time series and dependency graphs as core inputs for multi-modal troubleshooting

- [[informed-assessable-observability-design-decisions-cloud]] — uses distributed traces as response variables in observability experiments; demonstrates that increasing trace sampling rate (1%→5%) can surface invisible faults (NetworkDelay) with measurable cost overhead

- [[tracing-metrics-design-patterns-monitoring-cloud]] — formalizes Distributed Tracing as a design pattern; covers tail-based vs. head-based sampling trade-offs, OpenTelemetry SDK adoption, clock skew handling via parent span IDs (EuroPLoP 2025)

## My understanding

The foundational observability primitive for microservice diagnostics. Distributed tracing provides the richest data for both anomaly detection and RCA, but at the cost of non-trivial instrumentation. The field has largely converged on OpenTelemetry as the standard, which reduces but does not eliminate this cost.
