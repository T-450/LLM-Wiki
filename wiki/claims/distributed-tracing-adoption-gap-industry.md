---
title: "Distributed tracing is recognized as essential but its instrumentation is not consistently adopted in industry"
slug: distributed-tracing-adoption-gap-industry
status: weakly_supported
confidence: 0.55
tags: [distributed-tracing, observability, industry-adoption, instrumentation, microservices]
domain: "ML Systems"
source_papers: [observability-monitoring-distributed-systems-industry-interview]
evidence:
  - source: observability-monitoring-distributed-systems-industry-interview
    type: supports
    strength: moderate
    detail: "Industry interviews reveal that practitioners recognize distributed tracing as a key solution for holistic observability ('bird's eye view' of request flow), but instrumentation to propagate trace IDs through services developed by different teams is 'not consistently assured'. Cross-team coordination for instrumentation is a significant barrier."
conditions: "Based on 2019 interviews, pre-OpenTelemetry maturity. OpenTelemetry auto-instrumentation may have reduced this gap since then."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

While distributed tracing is widely recognized by practitioners as an essential solution for understanding request flows and diagnosing faults in distributed systems, its consistent adoption is hampered by the instrumentation burden -- particularly the need for cross-team coordination to propagate trace IDs through independently developed services.

## Evidence summary

Niedermaier et al. (2019) found that distributed tracing was emphasized as a solution (S3) for providing holistic views and capturing causal relationships among events. However, participants noted that "the instrumentation in order to propagate trace IDs through individual services, developed by different teams, is at the moment not consistently assured." This gap between recognition and adoption reflects the broader organizational challenges of observability.

## Conditions and scope

Strongest for the 2019 timeframe. OpenTelemetry's maturation (CNCF graduated project), auto-instrumentation libraries, and eBPF-based non-invasive tracing may have narrowed this gap. However, heterogeneous technology stacks and legacy systems likely still present instrumentation challenges.

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- Has OpenTelemetry auto-instrumentation effectively closed the adoption gap identified in 2019?
- What percentage of microservice requests in typical production systems are fully traced end-to-end?
- Do eBPF-based approaches eliminate the cross-team coordination barrier?
