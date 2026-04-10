---
title: "Observability design decisions involve quantifiable trade-offs between fault coverage and instrumentation cost"
slug: observability-design-decisions-involve-quantifiable-trade
status: weakly_supported
confidence: 0.55
tags: [observability, instrumentation, cost, trade-offs, microservices, cloud-native]
domain: "ML Systems"
source_papers: [informed-assessable-observability-design-decisions-cloud]
evidence:
  - source: informed-assessable-observability-design-decisions-cloud
    type: supports
    strength: moderate
    detail: "Experiments show that increasing tracing sampling rate from 1% to 5% (alt B) increases OFO from 2/3 to 3/3 with +3.05% CPU overhead, while 10% sampling (alt C) achieves the same OFO gain at +5.33% overhead. Increasing the metric sampling rate (alt A) improves fault coverage but not OFO, at +3.98% CPU overhead. This demonstrates that different observability design axes have distinct cost-effectiveness profiles."
conditions: "Measured on a specific 20-service demo application. The absolute cost overhead values are application-specific, but the existence of non-trivial cost-effectiveness differences across design alternatives is likely generalizable."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Different observability design decisions — choices about which metrics to collect, sampling rates, instrumentation points, and fault detection mechanisms — carry quantifiably different costs (CPU, storage, network overhead) and yield quantifiably different fault detection capabilities. Rational observability design requires explicitly measuring and comparing these trade-offs.

## Evidence summary

Borges et al. (2024) measure the CPU cost and OFO improvement of three design alternatives on the OpenTelemetry Astronomy Shop demo. Design B (5% trace sampling) achieves the same OFO improvement as design C (10%) at a lower cost (3.05% vs 5.33% CPU overhead). Design A (shorter metric sampling interval) improves fault coverage but not OFO, demonstrating that not all improvements are equivalent. These results quantitatively confirm that design alternatives have distinct cost-benefit profiles that cannot be evaluated without systematic measurement.

## Conditions and scope

Demonstrated for monitoring and tracing design dimensions (sampling rate, instrumentation points). The claim plausibly generalizes to logging and alerting design choices, but this has not been demonstrated. Cost is measured as CPU utilization only; other dimensions (storage, network, latency) are not included.

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- How do observability cost-benefit trade-offs scale with system size (number of services)?
- Can a Pareto-optimal observability configuration be found automatically?
- How do cost-benefit profiles change under different traffic patterns and fault frequencies?
