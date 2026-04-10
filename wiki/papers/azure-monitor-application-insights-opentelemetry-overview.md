---
title: "Azure Monitor Application Insights OpenTelemetry Overview"
slug: azure-monitor-application-insights-opentelemetry-overview
arxiv: ""
venue: "Microsoft Learn / Azure Documentation"
year: 2025
tags: [observability, opentelemetry, azure-monitor, application-insights, apm, instrumentation, cloud-native, distributed-tracing, metrics, ai-agents]
importance: 3
date_added: 2026-04-09
source_type: web
s2_id: ""
keywords: [OpenTelemetry, Azure Monitor, Application Insights, APM, distributed tracing, instrumentation, auto-instrumentation, AI agent observability]
domain: "ML Systems"
code_url: "https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-overview"
cited_by: []
---

## Problem

Production applications running on Azure — and cloud-native apps generally — need a unified way to collect and analyze telemetry (traces, metrics, logs) across heterogeneous services, languages, and deployment environments. Proprietary SDK lock-in has historically made it hard to switch observability backends or adopt standard tooling.

## Key idea

Azure Monitor Application Insights now uses **OpenTelemetry (OTel)** as its primary instrumentation framework for server-side applications. OTel is a vendor-neutral CNCF standard that separates telemetry collection from the backend, enabling portability. Microsoft provides the **Azure Monitor OpenTelemetry Distro** — a pre-configured OTel distribution with Azure-specific exporters, sampling defaults, and integrations — as the recommended on-ramp.

For browser/JavaScript apps, the legacy Application Insights JavaScript SDK is still used (OTel is not yet available for browsers).

## Method

**Data collection paths by scenario:**

| Scenario | Recommended approach |
|---|---|
| Server-side web apps | Azure Monitor OpenTelemetry Distro |
| VM / VMSS | Azure Monitor OpenTelemetry Distro |
| Azure Functions | `telemetryMode: OpenTelemetry` in host.json |
| AKS | Azure Monitor OpenTelemetry Distro (auto-instrumentation in preview) |
| JavaScript / Browser | Application Insights JavaScript SDK (not OTel) |
| AI Agents | Azure AI OpenTelemetry Tracer; Foundry SDK; Agent Framework |

**Application Insights experiences** (analysis features built on collected telemetry):

- *Application map* — visual topology of service dependencies with health indicators
- *Live metrics* — real-time stream of requests, failures, and server performance
- *Failures view / Performance view* — failure rate analysis and latency percentile drilldown
- *Availability view* — synthetic monitoring (outside-in probing)
- *Agents details view* — unified monitoring for AI agents (Microsoft Foundry, Copilot Studio, third-party)

**Instrumentation options:**

- **Auto-instrumentation (codeless)** — platform-level injection, no code changes; limited configuration
- **Code-based (OpenTelemetry Distro)** — full configuration and extensibility

**AI agent observability (new in 2025):**

- Capture full prompt/response data via `EnableSensitiveData` flag
- View conversation traces (system prompts, tool calls, assistant messages) in Transaction Details
- Supports LangChain, LangGraph, OpenAI Agents SDK, Copilot Studio, Foundry-managed agents

## Results

This is documentation, not an empirical study. Key architectural decisions documented:

- OTel is now the recommended path for all new server-side instrumentation (legacy Classic API SDKs are deprecated migration target)
- Connection string replaces instrumentation key as the primary configuration identifier
- The JavaScript SDK deliberately does NOT adopt OTel (browser OTel support is pending)
- Application Insights resource connects directly to an Azure Monitor Log Analytics workspace

## Limitations

- Browser/JavaScript instrumentation is not yet on OpenTelemetry — a notable gap given frontend observability importance
- Azure Functions C# in-process model does not support OTel
- Auto-instrumentation for AKS is still in public preview (2025)
- Vendor-specific: documentation covers Azure Monitor backend; OTel data can be exported elsewhere but Azure-specific features (application map, live metrics) require Application Insights ingestion

## Open questions

- When will the Application Insights JavaScript SDK migrate to OpenTelemetry?
- How does Azure Monitor handle OpenTelemetry sampling decisions in conjunction with server-side head/tail-based sampling?
- What are the cost implications of switching from auto-instrumentation to code-based (more data volume)?
- How do the "Agents details" telemetry features handle privacy/PII in captured prompts?

## My take

This page documents the state of Microsoft's observability platform as of late 2025. The OTel migration is significant: it means Application Insights data can now be exported to any OTel-compatible backend, reducing vendor lock-in. The AI agent observability section reflects the industry shift toward LLM-based system observability. The JavaScript/browser gap is a known limitation worth tracking. For practitioners using Azure, this is the authoritative starting point for setting up application observability.

## Related

- [[distributed-tracing]] — OTel is the current standard for distributed trace instrumentation
- [[application-metrics-instrumentation-cloud-native]] — Application Insights implements metrics collection via OTel signals
- [[monitoring-design-patterns-cloud-native]] — Application Insights features map to several patterns from the design patterns paper
- [[observability-experiment]] — OTel auto-instrumentation and its limitations are relevant to observability coverage experiments
