---
title: "Fault Tolerance and Reliability in Distributed Systems"
tags: [fault-tolerance, reliability, replication, recovery, circuit-breaker, sre, slo]
my_involvement: reading
sota_updated: 2026-04-09
key_venues: [OSDI, SOSP, EuroSys, NSDI, DSN, USENIX ATC]
related_topics:
  - consensus-coordination-distributed-systems
  - distributed-storage-databases
  - observability-foundations-distributed-systems
  - root-cause-analysis-microservices
key_people: []
---

## Overview

Fault tolerance is the ability of a system to continue operating correctly in the presence of failures — hardware faults, software bugs, network partitions, or malicious actors. Distributed systems must handle **crash failures** (processes stop), **omission failures** (messages lost), and in adversarial settings, **Byzantine failures** (arbitrary behavior).

Reliability in production systems is operationalized through **Service Level Objectives (SLOs)** and **error budgets** — measuring and bounding how much downtime or latency degradation is acceptable. SRE (Site Reliability Engineering) provides the organizational and tooling framework.

Key patterns: **replication** (active-active, active-passive), **circuit breakers**, **bulkheads**, **retry with exponential backoff**, **chaos engineering**, **graceful degradation**, **timeouts and deadlines**.

## Timeline

- **1978**: Lamport — "Time, Clocks, and the Ordering of Events"
- **1982**: Byzantine Generals Problem (Lamport, Shostak, Pease)
- **1999**: PBFT — practical BFT for state machine replication
- **2003**: Erlang/OTP supervision trees — fault tolerance by design
- **2014**: Netflix Hystrix — circuit breaker pattern popularized
- **2016**: Google SRE Book — SLO/error budget framework published
- **2019**: AWS: "Formal reasoning about the Amazon S3 ShardStore" (TLA+ in prod)
- **2020s**: Chaos engineering standardized (Chaos Monkey, Litmus, Chaos Mesh)

## Seminal works

- Lamport, Shostak, Pease, "The Byzantine Generals Problem" (ACM TOPLAS 1982)
- Castro & Liskov, "Practical Byzantine Fault Tolerance" (OSDI 1999)
- Beyer et al., "Site Reliability Engineering" (O'Reilly 2016)
- Birman, "Reliable Distributed Systems" (Springer 2005)

## SOTA tracker

| Technique | Maturity | Notes |
|---|---|---|
| Raft-based replication | Production-standard | etcd, CockroachDB, TiKV |
| Chaos engineering | Widely adopted | Netflix, Google, Alibaba |
| Observability experimentation | Emerging | [[informed-assessable-observability-design-decisions-cloud]] (OXN) |
| SLO-based alerting | Industry standard | Google SRE model |
| BFT (HotStuff/Tendermint) | Blockchain-adjacent | Performance still limited |

## Open problems

- Lightweight BFT for non-blockchain settings
- Automatic recovery from partial failure without operator intervention
- Failure modes at the intersection of hardware (NVM, RDMA) and software stacks
- Formal verification of fault-tolerant protocols at scale (beyond TLA+)

## My position

Most production reliability improvements come from better observability and faster diagnosis rather than more sophisticated fault-tolerance mechanisms. The SRE error budget model has been transformative — it converts reliability into a quantifiable engineering trade-off.

## Research gaps

- Interaction between microservice-level and infrastructure-level fault tolerance mechanisms
- How to set SLOs for ML/AI-serving components (non-deterministic behavior)
- Chaos engineering coverage — what classes of faults are systematically under-tested?

## Key people
