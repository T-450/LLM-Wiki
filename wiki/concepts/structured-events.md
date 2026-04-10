---
title: "Structured Events"
aliases: ["structured event", "wide events", "arbitrarily wide events", "rich events"]
tags: [observability, instrumentation, events, high-cardinality, debugging]
maturity: stable
key_papers: [observability-engineering-majors-fong-jones-miranda]
first_introduced: "Majors, Fong-Jones, Miranda — Observability Engineering (O'Reilly, 2022)"
date_updated: 2026-04-09
related_concepts: [distributed-tracing, application-metrics-instrumentation-cloud-native, log-based-anomaly-detection]
---

## Definition

A structured event is an arbitrarily wide key-value record that captures all context for a single unit of work — one request invocation, one job execution, one transaction. Unlike metrics (which aggregate many events into a scalar) or unstructured logs (which encode context as free-form text), a structured event preserves every individual field value for post-hoc querying.

## Intuition

When a request fails in production, you need to know not just that it failed, but which user, which feature flag variant, which database shard, which downstream service, and what the timing was at each step. A pre-aggregated metric (e.g., `error_rate = 0.5%`) cannot answer any of these questions. A structured event with 100+ fields can answer all of them — if the fields were recorded.

The key insight: observability is a property of **data richness**, not data volume. A system emitting 1 million narrow events (5 fields each) is less observable than one emitting 100,000 wide events (100+ fields each).

## Formal notation

An event $E = \{(k_1, v_1), (k_2, v_2), \ldots, (k_n, v_n)\}$ where each key $k_i$ is a string and each value $v_i$ is a primitive (string, number, boolean). An event is scoped to one unit of work and includes a timestamp and duration. Cardinality refers to the number of distinct values for a given key; high-cardinality keys (user_id, request_id, trace_id) are what enable per-entity debugging.

## Variants

- **Trace span**: a structured event with additional fields encoding causal relationships (`trace_id`, `span_id`, `parent_span_id`) — the building block of [[distributed-tracing]]
- **Structured log line**: a JSON log entry with consistent field naming — a partial structured event, often missing duration and trace linkage
- **Custom event**: developer-added event for business-logic context (e.g., `checkout.complete = true, cart.item_count = 5`)

## Comparison

| Telemetry type | Granularity | Query flexibility | Storage per event |
|----------------|------------|-------------------|-------------------|
| Pre-aggregated metric | Aggregate only | Fixed at write time | Very low |
| Unstructured log | Per-event | Text search only | Low-medium |
| Structured event | Per-event | Any field, any value | Medium-high |

## When to use

- When you need to debug production issues involving specific users, requests, or entities
- When failure modes are not known in advance (unknown unknowns)
- When correlating business outcomes with technical performance metrics
- As the input to distributed tracing pipelines

## Known limitations

- High-cardinality field storage is expensive — user_id as a metric label will explode storage; as an event field, it is queryable but only via column-oriented scan
- Width increases per-event serialization and network overhead
- Requires discipline to add context-rich fields consistently across all services (instrumentation hygiene)

## Open problems

- Optimal event width: at what field count does the storage/query cost exceed the debugging benefit?
- Automated event enrichment: inferring missing fields from context without developer annotation
- Privacy-safe structured events: redacting PII from high-cardinality fields without losing debuggability

## Key papers

- [[observability-engineering-majors-fong-jones-miranda]] — canonical definition; argues structured events are the necessary foundation of true observability, with metrics as a derivative/lossy compression

## My understanding

The most important observability concept that practitioners get wrong. The instinct is to add more dashboards (more metrics); the correct response to unknown failures is to add more event fields (more context). The shift from "what metrics do I need?" to "what context should every event carry?" is the core mental model shift of modern observability practice.
