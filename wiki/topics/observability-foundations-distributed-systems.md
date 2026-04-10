---
title: "Observability Foundations for Distributed Systems"
tags: [observability, distributed-systems, monitoring, tracing, metrics, logging]
my_involvement: none
sota_updated: 2026-04-09
key_venues: [ICSE, FSE, ASE, SOSP, OSDI, SREcon]
related_topics: [root-cause-analysis-microservices, anomaly-detection-cloud-native-systems, observability-engineering-tooling]
key_people: []
---

## Overview

Observability foundations encompass the theoretical principles and practical models for understanding the internal state of distributed systems from their external outputs. The "three pillars" model — logs, metrics, and distributed traces — has become the dominant conceptual framework, though the field increasingly recognizes that these signals must be correlated and contextualized to be effective. Key open-source projects (OpenTelemetry, Prometheus, Jaeger) have standardized instrumentation and data collection, while qualitative studies reveal persistent organizational and technical challenges in achieving effective observability.

## Timeline

- **2010**: Google publishes Dapper paper, establishing distributed tracing as a discipline
- **2012**: Twitter open-sources Zipkin, the first widely-adopted open-source distributed tracing system
- **2017**: Uber open-sources Jaeger; OpenTracing project gains momentum
- **2019**: OpenTelemetry project formed (merger of OpenTracing + OpenCensus), becoming the vendor-neutral standard
- **2019**: Niedermaier et al. publish qualitative industry study on observability challenges
- **2025**: Albuquerque & Correia formalize tracing and metrics design patterns for cloud-native apps

## Seminal works

- Google Dapper (2010) — pioneered distributed tracing at scale
- [[observability-monitoring-distributed-systems-industry-interview]] — qualitative study of industry practices and challenges
- [[tracing-metrics-design-patterns-monitoring-cloud]] — design patterns for monitoring cloud-native applications
- [[informed-assessable-observability-design-decisions-cloud]] — formal model of observability design space; fault visibility metrics and OXN experiment engine

## SOTA tracker

| Aspect | Current state | Key reference |
|--------|--------------|---------------|
| Instrumentation standard | OpenTelemetry (CNCF graduated) | CNCF ecosystem |
| Tracing | Context propagation via W3C Trace Context; eBPF-based non-invasive tracing | Nahida (2023) |
| Metrics | Prometheus + PromQL; application and infrastructure metrics patterns | [[tracing-metrics-design-patterns-monitoring-cloud]] |
| Organizational practices | Strategy, roles, and responsibilities recognized as critical gaps | [[observability-monitoring-distributed-systems-industry-interview]] |

## Open problems

- Bridging the gap between observability data collection and actionable insight
- Reducing instrumentation overhead in high-throughput systems
- Standardizing observability practices across heterogeneous technology stacks
- Organizational adoption: awareness and responsibility allocation for observability

## My position

Starting exploration of this domain. Primary interest in how foundational observability principles translate into automated diagnostic capabilities.

## Research gaps

- Limited formal models connecting observability coverage to fault detection capability — *partially addressed by [[informed-assessable-observability-design-decisions-cloud]] (fault visibility metrics + OFO)*
- Few studies on the cost-effectiveness of different observability configurations — *partially addressed by [[informed-assessable-observability-design-decisions-cloud]] (CPU cost vs. OFO trade-off experiments)*
- Lack of standardized benchmarks for evaluating observability system quality

## Key people

- [[jacopo-soldani]]
