---
title: "Log-Based Anomaly Detection"
aliases: ["log anomaly detection", "log-based fault detection", "service log analysis"]
tags: [anomaly-detection, log-analysis, unsupervised-learning, microservices]
maturity: active
key_papers: [anomaly-detection-failure-root-cause-analysis, eadro-end-end-troubleshooting-framework-microservices]
first_introduced: "Nandi et al. (OASIS, 2016)"
date_updated: 2026-04-09
related_concepts: [distributed-tracing, causality-graph-rca]
---

## Definition

Log-based anomaly detection identifies failures in multi-service applications by analyzing the native logs produced by application services, without requiring additional instrumentation such as distributed tracing or monitoring agents. Techniques learn baseline models of normal logging behavior from failure-free runs and detect deviations at runtime.

## Intuition

Services naturally produce logs during operation. By learning what "normal" log patterns look like (which events occur, in what order, with what timing), deviations from these patterns signal anomalies. This is the lowest-instrumentation approach — it works with data services already produce.

## Formal notation

Given a service $s$ with log stream $L_s = \{e_1, e_2, \ldots\}$ where each event $e_i$ maps to a template $t_i$ via template mining, a control-flow graph $G = (V, E, w)$ models baseline behavior where $V$ are template clusters, $E$ are sequencing relationships, and $w: E \to (\mathbb{R}^+, [0,1])$ assigns time lags and branching probabilities. An anomaly is detected when the observed sequence violates $G$.

## Variants

- **Control-flow graph mining** (OASIS): mines temporal sequencing of log templates with branching probabilities and time lags
- **Hawkes process model** (Eadro): models log event occurrence patterns via self-exciting point processes with exponential decay kernels; captures temporal dynamics without semantic parsing
- **Hybrid graph model** (Jia et al.): combines service topology graph with per-service time-weighted control flow graphs
- **LogSed**: similar to Jia et al., detects both functional and performance anomalies from log template sequences

## Comparison

| Approach | Instrumentation | Anomaly type | Granularity |
|----------|----------------|--------------|-------------|
| Log-based | None (native logs) | Functional + performance | Service-level |
| Distributed tracing-based | Trace instrumentation | Functional + performance | Application + service |
| Monitoring-based | Agent installation | Performance | Service-level |

Log-based approaches have the lowest setup cost but are limited by the information content of native logs.

## When to use

- When services cannot be instrumented with distributed tracing or monitoring agents
- When log data is already being collected and stored
- When detecting both functional anomalies (missing/unexpected events) and performance anomalies (delayed events)

## Known limitations

- Requires sufficient log verbosity to capture meaningful behavioral patterns
- Template mining quality affects detection accuracy
- Baseline models need retraining when services are updated
- Cannot capture inter-service causal relationships as precisely as tracing-based methods

## Open problems

- Handling log format changes across service versions
- Scaling to applications with hundreds of services producing high-volume logs
- Reducing false positives from benign behavioral variations

## Key papers

- [[anomaly-detection-failure-root-cause-analysis]] — survey covering log-based anomaly detection techniques
- [[eadro-end-end-troubleshooting-framework-microservices]] — models log event occurrences via Hawkes process as part of multi-modal fusion for troubleshooting

## My understanding

The simplest instrumentation approach — works with what services already produce. The tradeoff is lower observability fidelity compared to tracing, but zero additional instrumentation overhead. Useful as a baseline or in brownfield systems where adding tracing is costly.
