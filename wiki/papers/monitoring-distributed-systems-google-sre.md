---
title: "Monitoring Distributed Systems"
slug: monitoring-distributed-systems-google-sre
arxiv: ""
venue: "Site Reliability Engineering (O'Reilly / Google)"
year: 2016
tags: [observability, monitoring, sre, four-golden-signals, alerting, distributed-systems, metrics, white-box-monitoring, slo]
importance: 5
date_added: 2026-04-09
source_type: web
s2_id: ""
keywords: [Four Golden Signals, latency, traffic, errors, saturation, white-box monitoring, black-box monitoring, symptom-based alerting, tail latency, SLO]
domain: "ML Systems"
code_url: "https://sre.google/sre-book/monitoring-distributed-systems/"
cited_by: []
---

## Problem

As distributed systems scale, monitoring configurations grow complex — teams accumulate hundreds of dashboards and alert rules that become impossible to maintain. Alert fatigue produces on-call engineers who ignore pages, defeating the purpose of monitoring. The field lacked a principled, minimal framework for deciding what to monitor and how to alert.

## Key idea

Google's SRE discipline distilled production monitoring into the **Four Golden Signals** — the minimal set of metrics that, if measured for any service, provide sufficient visibility for on-call response. Equally important is an alert philosophy grounded in symptoms (user-visible impact) rather than causes (internal system state).

## Method

**Four Golden Signals** (Rob Ewaschuk, Google SRE):

| Signal | Definition | Why it matters |
|--------|-----------|----------------|
| **Latency** | Time to service a request | Distinguish slow successful requests from slow errors; use percentiles (p50, p99), not means |
| **Traffic** | Demand on the system | Requests/sec, active connections, I/O rate; provides baseline for error rate context |
| **Errors** | Rate of failed requests | Explicit (HTTP 500) and implicit (HTTP 200 with wrong content); separate by error type |
| **Saturation** | How "full" the service is | Resource utilization approaching limits; predictive indicator before failures manifest |

**Alert philosophy — 5 questions every page should answer:**

1. Does this page detect a condition that is urgent, actionable, and requiring human intelligence?
2. Could the alert be safely ignored without user impact?
3. Does the alert definitively indicate user harm?
4. Can the alert be acted upon by the on-call engineer?
5. Is the alert simple enough to act on at 3am?

**Symptom vs. cause monitoring:**
- **Symptom-based** (preferred): alerts on user-visible impact (e.g., error rate > 1%) — durable, stable, actionable
- **Cause-based** (supplementary): alerts on internal conditions (CPU, memory) — brittle, requires constant tuning, generates false positives

**White-box vs. black-box monitoring:**
- **White-box**: instrumentation of internal state (logs, metrics, profiling) — enables proactive detection but may miss user experience
- **Black-box**: synthetic probing from outside (uptime checks, synthetic transactions) — detects user-visible failures; complements white-box

**Tail latency principle**: Latency should be tracked as distributions (histograms), not means. The p99 latency is often the experience of 1% of users — in high-traffic systems, that's many users. Mean latency systematically undercounts slow requests.

**Simplicity principle**: The value of an observability system comes from its use in debugging. Complex configurations get abandoned. Every monitoring rule that is never triggered should be deleted. The goal is the minimal viable monitoring setup, not comprehensive coverage.

## Results

Practical framework validated across Google's production fleet. The Four Golden Signals have become the de facto starting point for service instrumentation across the industry, adopted in RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) method variants.

**Key operational insight**: a controlled short-term decrease in availability (e.g., allowing a rolling restart to take a service briefly below SLO) is sometimes correct to accept for long-run stability. Error budgets formalize this reasoning.

## Limitations

- Prescriptive framework designed for Google's scale; small services may need fewer signals
- Does not address cardinality constraints in metric storage
- Tail latency discussion predates widespread histogram support in time-series databases
- Black-box monitoring section is brief; doesn't address synthetic transaction complexity

## Open questions

- How should the Four Golden Signals be adapted for asynchronous/event-driven systems (no request-response cycle)?
- At what service complexity does the minimal monitoring principle break down?
- How should error budget burn rates be incorporated into alert severity?

## My take

Seminal — this chapter effectively defined production monitoring practice for the cloud-native era. The Four Golden Signals have the rare quality of being both theoretically sound (orthogonal, necessary, sufficient) and practically teachable. The symptom vs. cause framing is the right mental model for reducing alert fatigue. The simplicity principle is routinely violated and routinely causes problems when it is.

## Related

- [[application-metrics-instrumentation-cloud-native]] — Four Golden Signals as a metric selection framework; RED and READS are direct extensions
- [[distributed-tracing]] — white-box monitoring complement to metrics
- [[observability-engineering-majors-fong-jones-miranda]] — book-length extension; SLO-based alerting supersedes threshold-based
- [[opentelemetry-observability-primer]] — OTel operationalizes the signal types described here
- supports: [[structured-metric-selection-frameworks-improve-monitoring]]
