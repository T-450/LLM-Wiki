---
title: "SLO-Driven Observability Configuration Optimizer"
slug: slo-driven-observability-configuration-optimizer
status: proposed
origin: "Gap from informed-assessable-observability-design-decisions-cloud: the OXN framework quantifies fault visibility cost/coverage trade-offs but leaves configuration selection as a manual decision"
origin_gaps:
  - fault-tolerance-reliability
  - observability-foundations-distributed-systems
tags: [observability, slo, optimization, chaos-engineering, cloud-native, automation]
domain: ML Systems
priority: 4
pilot_result: ""
failure_reason: ""
linked_experiments: []
date_proposed: 2026-04-09
date_resolved: ""
---

## Motivation

The [[informed-assessable-observability-design-decisions-cloud]] paper introduces fault visibility metrics (OFO, fault coverage) and observability experiments to *measure* how well a configuration detects faults. However, selecting the optimal configuration — which spans OpenTelemetry settings, sampling rates, metric granularity, log verbosity — remains a manual engineering decision.

As systems scale to hundreds of services, manual configuration becomes intractable. The gap is an automated optimizer that takes SLO requirements as input and outputs an observability configuration that maximizes fault visibility within a cost budget.

## Hypothesis

An optimization loop that iteratively runs observability experiments (fault injection → OFO measurement → configuration adjustment) can converge to a Pareto-optimal configuration balancing fault coverage and telemetry cost faster than manual tuning, with measurable improvement in MTTD.

## Approach sketch

1. **Formalize the configuration space**: parameterize OpenTelemetry instrumentation as a discrete/continuous search space (sampling rates, span attributes, metric cardinality, log levels)
2. **Define the objective**: maximize OFO (fault observability) subject to CPU/storage cost ≤ budget, using the OXN framework's measurement tools
3. **Search strategy**: Bayesian optimization or evolutionary search over configuration space, using observability experiments as the fitness oracle
4. **Validation**: compare MTTD before/after optimization on a benchmark microservice deployment (e.g., Sock Shop, Online Boutique)

## Expected outcome

A 20–40% improvement in OFO score at equivalent cost compared to default/manual configurations, with reduced MTTD for injected fault types. Publishable as an AutoML-for-observability contribution.

## Risks

- Configuration space may be too large for efficient search without pruning heuristics
- Fault injection diversity: optimizer may overfit to injected fault types not representative of production failures
- Generalization across service architectures is unknown

## Pilot results

_Not yet run._

## Lessons learned

_Not yet run._
