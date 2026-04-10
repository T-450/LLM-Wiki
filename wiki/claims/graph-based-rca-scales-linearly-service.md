---
title: "Graph-based RCA scales linearly with service count in production microservice systems"
slug: graph-based-rca-scales-linearly-service
status: weakly_supported
confidence: 0.5
tags: [root-cause-analysis, scalability, microservices, graph-analysis, efficiency]
domain: "ML Systems"
source_papers: [microhecl-high-efficient-root-cause-localization]
evidence:
  - source: microhecl-high-efficient-root-cause-localization
    type: supports
    strength: moderate
    detail: "Execution time of MicroHECL scales linearly with service count across 28 Alibaba subsystems (7-1687 services). MonitorRank and Microscope also show linear scaling. MicroHECL's efficiency advantage becomes significant beyond 250 services due to pruning."
conditions: "Demonstrated on Alibaba subsystems. Linear scaling may not hold for highly interconnected topologies where pruning is less effective."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Graph-based root cause analysis approaches, particularly those using directed traversal with pruning, scale linearly with the number of services in the microservice system, making them viable for industrial-scale deployments with hundreds to thousands of services.

## Evidence summary

MicroHECL (Liu et al., 2021) evaluates execution time across 28 Alibaba subsystems ranging from 7 to 1,687 services. All three approaches (MicroHECL, MonitorRank, Microscope) show approximately linear scaling. MicroHECL's pruning strategy provides increasing efficiency advantage as system size grows, with the difference becoming significant above 250 services.

## Conditions and scope

- Evaluated on Alibaba's e-commerce system where service call graphs are relatively sparse (not fully connected)
- Linear scaling depends on graph sparsity; highly interconnected topologies may show worse scaling
- Only tested up to ~1,700 services; behavior at 10,000+ services is unknown

## Counter-evidence

None directly.

## Linked ideas

## Open questions

- Does linear scaling hold for systems with 10,000+ services or highly dynamic topologies?
- How does graph density (average degree) affect scaling behavior?
- Can distributed graph processing maintain linear scaling as individual machine memory limits are reached?
