---
title: "Observability Experiment"
aliases: ["observability experiments", "observability experimentation", "OXN experiment"]
tags: [observability, chaos-engineering, fault-injection, experimentation, microservices, cloud-native]
maturity: emerging
key_papers: [informed-assessable-observability-design-decisions-cloud]
first_introduced: "Borges et al. (2024)"
date_updated: 2026-04-09
related_concepts: [fault-visibility-metric, distributed-tracing]
---

## Definition

A structured empirical process for evaluating observability design decisions by combining Chaos Engineering-style fault injection with controlled modification of observability configuration. Formally, an observability experiment consists of:
- **System Under Experiment (SUE)**: the microservice application (full or subset) under evaluation
- **Workload**: a load generator producing realistic traffic (enabling comparative analysis)
- **Treatments**: controlled changes — either *fault treatments* (runtime fault injection) or *instrumentation treatments* (compile-time observability configuration changes)
- **Response variables**: collected metrics and distributed traces used to compute fault visibility metrics

## Intuition

Chaos Engineering tests whether a system *survives* faults. An observability experiment tests whether a system *sees* faults — whether the instrumentation and configuration are sufficient for the fault detection mechanism to detect injected faults. By varying instrumentation treatments alongside fault treatments, practitioners can compare the fault observability of different configurations in a controlled, reproducible way.

## Formal notation

Let $E = (SUE, W, T_f, T_i, R)$ where $W$ is the workload, $T_f$ the fault treatment set, $T_i$ the instrumentation treatment set, and $R = \{r_1, \ldots, r_k\}$ the response variable set. For each combination $(t_f, t_i) \in T_f \times T_i$, responses are collected and fault visibility metrics computed: $v_{f,m,d}$, $FC_{f,d}$, $OFO_d$.

## Variants

- **Fault-only experiments**: vary fault types, keep instrumentation fixed (baseline evaluation)
- **Instrumentation-only experiments**: vary observability configuration, keep faults fixed (design alternative comparison)
- **Full factorial**: vary both fault and instrumentation treatments
- **Subset SUE experiments**: target a single service and its dependencies rather than the full application

## Comparison

| Approach | Focus | Modifies obs. config | Quantifies obs. quality |
|----------|-------|---------------------|------------------------|
| Chaos Engineering | System resilience | No | No |
| A/B testing (perf.) | Performance | Sometimes | No |
| Observability experiment | Observability quality | Yes | Yes (OFO/FC) |
| Manual observability audit | Obs. coverage | No | Qualitatively |

## When to use

- When evaluating which observability configuration to adopt before deploying to production
- When onboarding a new service and deciding on its instrumentation strategy
- As part of a CI/CD pipeline for continuous observability assurance
- When diagnosing why certain faults were missed in production (retroactive analysis)

## Known limitations

- Requires infrastructure-as-code descriptions of both the SUE and observability configuration
- Most applicable in staging environments; production fault injection requires careful safety controls
- Representative fault set must be manually defined; unknown fault classes are not covered
- Current tooling (OXN) targets Docker Compose; Kubernetes support pending

## Open problems

- Automatic identification of relevant fault scenarios for a given application
- Integration into CI/CD pipelines for shift-left observability assurance
- Scale to production-representative load and hundreds of services

## Key papers

- [[informed-assessable-observability-design-decisions-cloud]] — defines the observability experiment formalism and implements it in the OXN tool

## My understanding

A practically grounded extension of chaos engineering. The key insight — separating fault treatments from instrumentation treatments — opens up the observability design space for systematic exploration. The formalism is clean and tool-agnostic, even though the current OXN implementation is limited in platform support. High potential for adoption once Kubernetes support and CI/CD integration are added.
