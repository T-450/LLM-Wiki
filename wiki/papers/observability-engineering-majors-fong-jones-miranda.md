---
title: "Observability Engineering"
slug: observability-engineering-majors-fong-jones-miranda
arxiv: ""
venue: "O'Reilly Media"
year: 2022
tags: [observability, structured-events, distributed-tracing, sampling, slo, instrumentation, opentelemetry, observability-driven-development, high-cardinality]
importance: 5
date_added: 2026-04-09
source_type: web
s2_id: ""
keywords: [observability, structured events, high cardinality, high dimensionality, explorability, ODD, sampling, SLO, traces, Honeycomb]
domain: "ML Systems"
code_url: ""
cited_by: []
---

## Problem

The industry conflates "monitoring" with "observability", treating the three pillars (logs, metrics, traces) as a definition rather than a starting point. This framing leads teams to build elaborate dashboards of pre-aggregated metrics that can only answer questions anticipated at design time — leaving them helpless against novel failure modes in production. The book argues this is a fundamental architectural problem, not an operational one.

## Key idea

True observability requires three properties beyond the traditional three-pillar framing:

1. **High cardinality**: the ability to query on individual values of high-cardinality fields (e.g., user_id, request_id) — metrics cannot do this because aggregation destroys granularity
2. **High dimensionality**: the ability to explore data along arbitrary combinations of attributes in real time — pre-built dashboards cannot do this because they fix the query structure at creation time
3. **Explorability**: the ability to ask new questions of data already collected, without deploying new instrumentation — the key differentiator from monitoring

The fundamental building block is the **structured event**: an arbitrarily wide key-value record capturing all context for one unit of work (one request, one job execution).

## Method

**Structured events as the foundation** (Ch. 5):
- An event is a map of key-value pairs scoped to a single request invocation
- Example fields: `trace.trace_id`, `duration_ms`, `user.id`, `http.status_code`, `db.query_time_ms`, `feature_flag.variant`
- Width is the differentiator: 100+ fields per event provides debuggable context; 5-10 fields per metric does not
- Metrics are pre-aggregated events — they are a lossy compression that cannot be reversed

**Stitching events into traces** (Ch. 6):
- A trace is a set of causally related events sharing a `trace_id`
- Each event carries `span_id` and `parent_span_id` to encode the causal DAG
- Context propagation via HTTP headers (B3 format, later W3C TraceContext) carries `trace_id` across service boundaries
- Traces go beyond service-to-service calls: background jobs, database queries, cache accesses are all valid spans

**Instrumentation with OpenTelemetry** (Ch. 7):
- OTel provides vendor-neutral APIs for generating traces, metrics, and logs
- Auto-instrumentation (agent/library injection) gives baseline coverage without code changes
- Custom instrumentation adds business-logic context that auto-instrumentation cannot capture
- The two complement each other: auto for breadth, custom for depth

**Observability-Driven Development** (Ch. 11):
- Observability is a complement to TDD, not a replacement: debugger finds WHAT in code, observability finds WHERE in the system
- Instrumentation should be a requirement of every PR, not a follow-up task
- The "glass castle" anti-pattern: systems that look fine from outside dashboards but are internally fragile because operators never explore the data
- Progressive delivery (feature flags, canary releases) becomes meaningfully safe only with observability feedback loops

**SLO-based alerting** (Ch. 12):
- Threshold-based monitoring produces alert fatigue and "normalization of deviance" — teams learn to ignore pages
- SLOs decouple "what is broken" from "why it is broken": SLO breach = user impact, investigation = root cause
- Event-based SLIs (fraction of good events over all events in window) are more robust than time-based (uptime over a window) because they capture partial failures (e.g., 5% of requests failing)
- Case study: Honeycomb detected a brownout affecting a subset of users via SLO alerts; traditional threshold monitoring showed all services "green"

**Sampling strategies** (Ch. 17):

| Strategy | Description | Best for |
|----------|-------------|---------|
| Constant-probability | Fixed rate (e.g., 1%) | Baseline overhead control |
| Traffic-volume-based | Rate inversely proportional to traffic | High-volume services; preserves rare-event signals |
| Key-based | Rate tied to a field value (e.g., user_id) | Ensuring full coverage per entity |
| Tail-based | Decision made after trace completion | Preserving anomalous/slow traces |

**Head-based vs. tail-based sampling trade-off**: head-based sampling decides at trace entry (low overhead, may discard anomalous traces); tail-based sampling decides at trace completion (can preserve errors and slow requests, but requires buffering full traces before forwarding).

**Consistent sampling for traces**: all spans from the same trace must share the same sampling decision to preserve trace integrity — key-based sampling on `trace_id` achieves this.

## Results

Practitioner book — not an empirical study. Impact: the book is the defining text for the modern observability-as-practice movement. Its structured event / high-cardinality / high-dimensionality framing has shaped tooling design at Honeycomb, Lightstep, and influenced OpenTelemetry's data model.

**Key operational insights:**
- Pre-aggregated metrics cannot answer questions about individual users or requests — structured events can
- SLO-based alerts detect partial failures that threshold-based monitoring misses
- Tail-based sampling is operationally superior for preserving diagnostic traces, despite higher infrastructure overhead

## Limitations

- Strongly influenced by Honeycomb's product perspective; recommendations favor wide-event/trace-centric approaches
- Cost models for high-cardinality storage at scale not deeply addressed
- Sampling strategies presented qualitatively; no empirical comparison of strategies on real workloads
- ODD adoption challenges in large organizations not fully addressed

## Open questions

- At what event width does the storage and query cost of structured events exceed the benefit over pre-aggregated metrics?
- How should sampling rates be set dynamically in response to incident detection?
- How does ODD integrate with legacy codebases where instrumentation cannot be added to every PR?

## My take

The most influential practitioner text on observability. The high-cardinality/high-dimensionality/explorability framing is correct and clarifying — it explains why metrics-only monitoring fails at scale in a way that the "three pillars" framing does not. The SLO-based alerting argument is compelling and backed by a concrete case study. The sampling chapter is the best practical treatment I've seen on the topic outside of academic work. This book should be paired with [[monitoring-distributed-systems-google-sre]] (Four Golden Signals for what to measure) and [[opentelemetry-observability-primer]] (OTel for how to instrument).

## Related

- [[distributed-tracing]] — core technique; Ch. 6 covers trace structure and propagation
- [[application-metrics-instrumentation-cloud-native]] — metrics as one signal; book argues metrics are insufficient alone
- [[observability-experiment]] — OXN experiments address the observability configuration optimization the book identifies as an open problem
- [[monitoring-distributed-systems-google-sre]] — Four Golden Signals; this book extends and critiques threshold-based alerting
- [[opentelemetry-observability-primer]] — OTel as instrumentation standard; Ch. 7 covers OTel adoption
- [[structured-events]] — core concept introduced in Ch. 5
- [[observability-driven-development]] — concept introduced in Ch. 11
- [[service-level-objectives]] — SLO-based alerting; Ch. 12
- supports: [[tail-based-sampling-outperforms-head-based]]
