---
title: "Service Level Objectives"
aliases: ["SLO", "SLI", "service level indicator", "error budget", "SLOs", "SLIs"]
tags: [observability, slo, sli, reliability, alerting, sre, error-budget]
maturity: stable
key_papers: [monitoring-distributed-systems-google-sre, observability-engineering-majors-fong-jones-miranda, opentelemetry-observability-primer]
first_introduced: "Google SRE Book (2016); formalized in Observability Engineering (2022)"
date_updated: 2026-04-09
related_concepts: [application-metrics-instrumentation-cloud-native, distributed-tracing, monitoring-design-patterns-cloud-native]
---

## Definition

A **Service Level Indicator (SLI)** is a quantitative measure of a service quality dimension visible to users (e.g., the fraction of requests completed in under 200ms). A **Service Level Objective (SLO)** is a target threshold for an SLI over a defined time window (e.g., 99.9% of requests under 200ms over a 30-day rolling window). An **error budget** is the allowable failure rate implied by the SLO — the complement of the SLO (e.g., 0.1% failures = the budget to spend on risky deployments, maintenance, and incidents).

## Intuition

Traditional alerting asks "is CPU > 80%?" — this is a cause-based alert that fires for reasons unrelated to user impact. SLO-based alerting asks "are users experiencing the service we promised?" — this is a symptom-based alert that fires only when the user experience degrades. The shift from cause to symptom reduces alert fatigue and focuses on-call attention on incidents that actually matter.

The error budget provides a communication mechanism between reliability (SRE) and velocity (product): when the budget is full, you can ship freely; when it's exhausted, reliability work takes priority.

## Formal notation

$$\text{SLI} = \frac{\text{count of good events}}{\text{count of all events}} \in [0, 1]$$

$$\text{SLO} = P(\text{SLI} \geq \theta) \text{ over window } W$$

$$\text{Error budget} = 1 - \text{SLO threshold}$$

**Burn rate**: the rate at which the error budget is consumed; a burn rate > 1 means the budget will be exhausted before the window ends.

## Variants

- **Event-based SLI**: fraction of good requests over all requests in a window — preferred; captures partial failures (e.g., 5% error rate while service is "up")
- **Time-based SLI**: fraction of time the service was "available" — coarser; misses brownouts and partial failures
- **Latency SLO**: fraction of requests under a latency threshold (e.g., p99 < 500ms)
- **Availability SLO**: fraction of requests without errors
- **Multi-window SLO**: burn rate alerts using short and long windows to balance alerting latency and precision

## Comparison

| Alerting approach | What it detects | Alert noise | User impact focus |
|-------------------|----------------|-------------|-------------------|
| Threshold (CPU > 80%) | Internal resource | High | No |
| Error rate threshold | User-visible errors | Medium | Partial |
| SLO burn rate | Error budget depletion rate | Low | Yes |

## When to use

- As the primary alerting mechanism for any service with defined reliability requirements
- When establishing a shared language between engineering and product/business stakeholders
- For prioritizing reliability work against feature development (error budget policy)
- As the "what is broken" detection layer before root cause analysis

## Known limitations

- SLO target-setting is difficult without historical traffic and failure data — targets set too tight generate alert fatigue; set too loose, miss real incidents
- Event-based SLIs require consistent event counting (can be skewed by traffic patterns)
- Error budgets can create perverse incentives (deliberately burning budget to justify reliability investment)
- Multi-window burn rate alerts add configuration complexity

## Open problems

- Automated SLO target recommendation from traffic patterns and incident history
- Composing SLOs across dependent services (upstream failures cascade into downstream SLO breaches)
- SLO-aware capacity planning: how does traffic growth affect budget consumption?

## Key papers

- [[monitoring-distributed-systems-google-sre]] — defines SLI/SLO as part of the Four Golden Signals framework; introduces error budgets
- [[observability-engineering-majors-fong-jones-miranda]] — argues event-based SLIs are superior to time-based; case study showing SLO detected brownout missed by threshold monitoring
- [[opentelemetry-observability-primer]] — defines SLI/SLO as core observability vocabulary

## My understanding

SLOs are the observability concept with the highest organizational impact — they connect technical measurement to business commitments. The event-based SLI model is strictly better than time-based for detecting partial failures, but requires structured event infrastructure to implement correctly. The error budget framework is elegant but its effectiveness depends heavily on organizational culture and explicit policy.
