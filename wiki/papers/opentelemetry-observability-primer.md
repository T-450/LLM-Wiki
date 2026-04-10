---
title: "OpenTelemetry Observability Primer"
slug: opentelemetry-observability-primer
arxiv: ""
venue: "OpenTelemetry Documentation (CNCF)"
year: 2024
tags: [observability, opentelemetry, distributed-tracing, metrics, logs, instrumentation, slo, sli, cloud-native]
importance: 3
date_added: 2026-04-09
source_type: web
s2_id: ""
keywords: [observability, telemetry, traces, metrics, logs, spans, SLI, SLO, reliability, instrumentation]
domain: "ML Systems"
code_url: "https://opentelemetry.io/docs/concepts/observability-primer/"
cited_by: []
---

## Problem

Modern distributed systems fail in ways that cannot be predicted in advance. Traditional monitoring relies on knowing what questions to ask ahead of time (known-unknowns), but distributed systems generate "unknown unknowns" — failure modes that nobody anticipated. Developers need a framework for reasoning about and instrumenting systems that can explain any state the system enters, including novel ones.

## Key idea

Observability is the ability to understand a system's internal state by examining its outputs. A system is observable when you can ask arbitrary questions about its behavior without deploying new code. The key distinction: **reliability is not the same as uptime** — a system can be "up" while silently failing a fraction of requests.

OpenTelemetry (OTel) operationalizes observability through three complementary signals:
- **Traces**: end-to-end records of a request path through a distributed system; composed of spans
- **Metrics**: aggregated numerical measurements over time (counters, gauges, histograms)
- **Logs**: timestamped records of discrete events

## Method

**Core vocabulary:**

| Concept | Definition |
|---------|-----------|
| Telemetry | Data emitted by a system about its own behavior |
| Span | A named, timed operation representing a unit of work; carries trace_id, span_id, parent_span_id, timestamps, attributes, events, status |
| Trace | A directed acyclic graph of spans representing a complete request traversal |
| SLI (Service Level Indicator) | A quantitative measure of service quality (e.g., fraction of requests under 200ms) |
| SLO (Service Level Objective) | A target threshold for an SLI over a time window (e.g., 99.9% of requests under 200ms over 30 days) |

**Distributed tracing is the key primitive for unknown unknowns**: it records causal relationships between operations across service boundaries, enabling post-hoc reconstruction of failure paths without pre-defined dashboards.

**Reliability from an observability lens**: reliability is about the user experience, not system uptime. A system that is "up" but returning errors 5% of the time is unreliable. SLOs define reliability in terms of user-visible behavior.

## Results

Conceptual documentation — not an empirical study. Key principles stated:

1. Observability enables debugging unknown unknowns; monitoring alone cannot
2. Distributed tracing is uniquely suited to non-deterministic, multi-service failures
3. Three signals (traces, metrics, logs) together provide complementary coverage
4. SLIs and SLOs connect technical observability signals to user-visible reliability commitments
5. OTel provides vendor-neutral instrumentation APIs for all three signals

## Limitations

- Does not address sampling strategies or cost vs. coverage trade-offs
- SLO target-setting methodology not covered
- Does not discuss the cardinality challenges of high-dimensional telemetry
- Vendor-neutral by design — does not guide backend selection

## Open questions

- How should SLI granularity be chosen to capture user-visible failures without alert noise?
- What sampling strategies preserve the diagnostic value of traces at scale?
- How do the three signals (traces, metrics, logs) interact in practice for multi-layer failures?

## My take

The canonical entry point for anyone working with modern observability tooling. The OTel standard has essentially won the instrumentation layer — the ecosystem has converged on it. The "unknown unknowns" framing is the right mental model for why observability matters beyond traditional monitoring. The SLI/SLO definitions here are the reference definitions used in practice.

## Related

- [[distributed-tracing]] — OTel's tracing signal; spans and trace propagation
- [[application-metrics-instrumentation-cloud-native]] — OTel's metrics signal
- [[log-based-anomaly-detection]] — OTel's logs signal and its use in anomaly detection
- [[azure-monitor-application-insights-opentelemetry-overview]] — Azure's OTel-based APM implementation
- [[observability-engineering-majors-fong-jones-miranda]] — book-length treatment of observability concepts with same "unknown unknowns" framing
