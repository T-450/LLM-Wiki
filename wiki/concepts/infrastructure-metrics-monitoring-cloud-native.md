---
title: "Infrastructure Metrics Monitoring"
aliases: ["infrastructure metrics", "system metrics", "resource metrics", "inside-out health check"]
tags: [observability, metrics, infrastructure, cloud-native, monitoring, use-method, sre]
maturity: stable
key_papers: [tracing-metrics-design-patterns-monitoring-cloud]
first_introduced: "USE method by Gregg (2013); pattern formalized by Albuquerque & Correia (2025)"
date_updated: 2026-04-09
related_concepts: [application-metrics-instrumentation-cloud-native, distributed-tracing, monitoring-design-patterns-cloud-native, fault-visibility-metric]
---

## Definition

The practice of instrumenting operating systems, runtimes, and cloud infrastructure to collect resource utilization, saturation, and error metrics (the USE method). Data is centralized in a Metrics Service for real-time monitoring, autoscaling triggers, SLA verification, and correlation with application-level symptoms.

## Intuition

Application behavior is ultimately grounded in physical resource availability. Infrastructure metrics expose when a system is approaching its limits (high CPU, memory pressure, disk saturation) before these constraints cause observable failures. They also enable correlating end-user symptoms ("page loads slowly") with underlying causes ("database node disk I/O saturated").

## Formal notation

Same metric tuple as Application Metrics: $(name, value, timestamp, tags)$. Tags include infrastructure context (instance ID, container name, node label, deployment timestamp) to enable post-hoc reconstruction of resource topology, especially important in cloud environments where infrastructure is ephemeral.

## Variants

- **USE Method** (Gregg 2013): utilization, saturation, errors — applied per resource (CPU, memory, disk, network)
- **Node exporter** (Prometheus): exposes 600+ OS/hardware metrics for *nix systems
- **Cloud provider APIs** (GCP, AWS): managed infrastructure metrics endpoints; limited configurability
- **Container-level metrics**: cAdvisor, kubelet metrics for Kubernetes pod/container resources

## Comparison

| Approach | Configurability | Coverage | Overhead |
|----------|----------------|----------|---------|
| Prometheus node exporter | High | OS + hardware | Low |
| Cloud provider API | Low | Provider-defined | Minimal |
| Custom agent | Full | Arbitrary | Variable |

## When to use

- When diagnosing performance issues that may stem from resource constraints (CPU, memory, disk)
- When managing autoscaling policies and SLA compliance in pay-as-you-go cloud environments
- When correlating application-level anomalies with infrastructure resource states
- As complementary signal alongside application metrics for complete system visibility

## Known limitations

- Infrastructure metrics identify symptoms (resource pressure) but not root causes (faulty code)
- Clock skew across distributed nodes can misalign infrastructure metric timestamps
- In PaaS/FaaS environments, teams may only have access to provider-managed metrics with limited granularity
- High-volume metric collection (node exporter's 600+ metrics) introduces significant storage and processing overhead
- Data siloing: uncorrelated infrastructure metrics from multiple services reduce diagnostic value

## Open problems

- Automated correlation between infrastructure metrics and application metrics without manual tag alignment
- Efficient anomaly detection on high-cardinality, high-volume infrastructure metric streams
- Predictive autoscaling using infrastructure metric patterns rather than reactive thresholds

## Key papers

- [[tracing-metrics-design-patterns-monitoring-cloud]] — formalizes Infrastructure Metrics as a design pattern; covers USE method, sampling resolution trade-offs, autoscaling implications, push/pull collection models

## My understanding

The complementary pair to application metrics. The USE method is a practical starting framework that forces teams to enumerate resources before selecting metrics — a useful discipline. The main pitfall is treating infrastructure metrics as the sole observability signal; they must be correlated with application and trace data for effective RCA.
