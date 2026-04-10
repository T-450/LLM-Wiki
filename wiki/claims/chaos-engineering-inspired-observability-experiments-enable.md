---
title: "Chaos engineering-inspired observability experiments enable systematic assessment of instrumentation configurations"
slug: chaos-engineering-inspired-observability-experiments-enable
status: weakly_supported
confidence: 0.6
tags: [observability, chaos-engineering, fault-injection, experimentation, microservices]
domain: "ML Systems"
source_papers: [informed-assessable-observability-design-decisions-cloud]
evidence:
  - source: informed-assessable-observability-design-decisions-cloud
    type: supports
    strength: moderate
    detail: "OXN extends chaos engineering by adding instrumentation treatments alongside fault treatments. Experiments consist of SUE, workload, treatments (fault and instrumentation), and response variables. Applied to 3 fault types × 3 design alternatives with 10 repetitions each, producing quantified OFO and cost results. The YAML-based configuration enables reproducibility and comparison of observability configurations."
conditions: "Demonstrated on a single open-source application in a staging environment with Docker Compose. The approach requires infrastructure-as-code (IaC) descriptions of both the SUE and observability configuration."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

By adapting the chaos engineering experimental paradigm to target observability configuration rather than system resilience, practitioners can systematically compare observability design alternatives using controlled, reproducible experiments with quantified fault visibility metrics.

## Evidence summary

Borges et al. (2024) define the observability experiment formalism: System Under Experiment (SUE), workload, treatments (fault treatments: pause, packet loss, network delay; instrumentation treatments: sampling rate changes), and response variables (metrics and traces). The OXN tool automates this process. The approach successfully differentiates three design alternatives, reveals the invisible NetworkDelay fault in the baseline configuration, and provides cost estimates alongside observability improvements.

## Conditions and scope

The approach is most applicable in staging environments where both the SUE and observability system are described as infrastructure-as-code. Production application of fault injection requires careful safety measures. The current implementation targets Docker Compose; Kubernetes support is a stated future goal.

## Counter-evidence

None documented yet. Critics may argue that staging environments may not faithfully represent production fault behavior due to traffic and scale differences.

## Linked ideas

## Open questions

- How representative are staging environment results for production fault observability?
- Can observability experiments be integrated into CI/CD pipelines for continuous assurance?
- What is the minimum set of fault scenarios needed to provide meaningful OFO coverage?
