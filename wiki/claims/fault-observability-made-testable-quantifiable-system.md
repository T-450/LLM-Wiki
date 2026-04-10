---
title: "Fault observability can be made a testable and quantifiable system property through systematic experimentation"
slug: fault-observability-made-testable-quantifiable-system
status: weakly_supported
confidence: 0.6
tags: [observability, fault-visibility, microservices, cloud-native, metrics]
domain: "ML Systems"
source_papers: [informed-assessable-observability-design-decisions-cloud]
evidence:
  - source: informed-assessable-observability-design-decisions-cloud
    type: supports
    strength: moderate
    detail: "Borges et al. define fault visibility, fault coverage (FC), and overall fault observability (OFO) as quantifiable metrics, and demonstrate their calculation on a 20-service microservice application. OFO goes from 2/3 to 3/3 after a configuration change, with measurable cost overhead of 3.05%."
conditions: "Demonstrated in a controlled experiment on OpenTelemetry Astronomy Shop demo with Docker Compose. Generalizability to production Kubernetes deployments with diverse workloads and hundreds of services is unvalidated."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Fault observability — the degree to which instrumentation and configuration allows a system's faults to be detected — can be formalized as a testable and quantifiable system property, analogous to test coverage. This enables empirical comparison of observability design alternatives and objective evaluation of instrumentation decisions.

## Evidence summary

Borges et al. (2024) propose three metrics: fault visibility (binary per fault-metric-detector triple), fault coverage (ratio of metrics observing a fault), and overall fault observability (fraction of all faults detectable in at least one metric). Applied to the OpenTelemetry Astronomy Shop demo, OFO is computed as 2/3 for a baseline configuration, improving to 3/3 after a 5% trace sampling rate increase, with quantified CPU overhead of 3.05%. The OXN tool automates this measurement process.

## Conditions and scope

Validated in a controlled simulation environment. Requires infrastructure-as-code description of both the system under experiment and its observability configuration. Practicality for live production systems or highly heterogeneous environments remains to be demonstrated.

## Counter-evidence

None documented yet. The binary nature of the visibility score may oversimplify continuous observability quality; borderline detection scenarios near the threshold are counted as 0 or 1.

## Linked ideas

## Open questions

- How does the metric framework handle partial or probabilistic fault detection?
- What is the minimum viable set of fault scenarios for a comprehensive OFO measurement?
- Can the approach scale to production systems without dedicated staging environments?
