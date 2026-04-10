---
title: "Distributed Storage and Databases"
tags: [distributed-storage, databases, consistency, replication, crdts, nosql, newsql]
my_involvement: reading
sota_updated: 2026-04-09
key_venues: [OSDI, SOSP, VLDB, SIGMOD, EuroSys]
related_topics:
  - consensus-coordination-distributed-systems
  - fault-tolerance-reliability
  - observability-foundations-distributed-systems
key_people: []
---

## Overview

Distributed storage systems must balance three competing concerns captured by the CAP theorem: **Consistency**, **Availability**, and **Partition tolerance** — and can achieve at most two under network partitions. In practice the design space is richer: PACELC extends CAP to cover latency-consistency trade-offs even when no partition exists.

The arc from Bigtable (2006) through Dynamo (2007) to Spanner (2012) illustrates the evolution: structured storage → eventual consistency at scale → globally consistent transactions with external consistency via TrueTime. Modern "NewSQL" systems (CockroachDB, YugabyteDB) attempt to unite SQL semantics with horizontal scalability.

Key concepts: **replication** (single-leader, multi-leader, leaderless), **sharding/partitioning**, **LSM trees vs B-trees**, **CRDTs** (conflict-free replicated data types), **vector clocks**, **write-ahead logging**, **quorum reads/writes**.

## Timeline

- **1979**: Lamport timestamps — logical ordering without global clocks
- **2003**: GFS (Google File System) — large-scale distributed file storage
- **2006**: Bigtable — wide-column store, row-level atomicity
- **2007**: Dynamo (Amazon) — eventual consistency, tunable quorums
- **2010**: Cassandra open-sourced — Dynamo + Bigtable hybrid
- **2011**: CRDT theory formalized (Shapiro et al.)
- **2012**: Spanner — globally distributed, externally consistent
- **2017**: Anna — lattice-based KV store for multi-tier environments
- **2020s**: FoundationDB, TiKV, Distributed PostgreSQL variants

## Seminal works

- DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (SOSP 2007)
- Chang et al., "Bigtable: A Distributed Storage System for Structured Data" (OSDI 2006)
- Corbett et al., "Spanner: Google's Globally Distributed Database" (OSDI 2012)
- Shapiro et al., "Conflict-free Replicated Data Types" (SSS 2011)
- Ghemawat et al., "The Google File System" (SOSP 2003)

## SOTA tracker

| System | Type | Consistency | Notes |
|---|---|---|---|
| Spanner | NewSQL | External | TrueTime-based global transactions |
| CockroachDB | NewSQL | Serializable | Open-source Spanner-inspired |
| FoundationDB | KV + Layers | ACID | Apple/Snowflake; layers model |
| TiKV | Distributed KV | Strong | Raft-based; used in TiDB |
| Cassandra 4.x | Wide-column | Tunable | LWT for lightweight transactions |

## Open problems

- Achieving low-latency global transactions without TrueTime hardware
- Efficient cross-shard transactions in sharded NewSQL systems
- Tail latency in geo-replicated systems under partition
- CRDTs for complex data models (beyond counters/sets)

## My position

The Dynamo paper's design choices (consistent hashing, sloppy quorums, vector clocks) remain influential even as the ecosystem moved back toward stronger consistency. Understanding it is essential for any distributed systems practitioner.

## Research gaps

- Limited benchmarking under realistic mixed read/write workloads with failures
- CRDT adoption in production systems — what prevents wider use?
- Interaction between storage engines and modern NVM / disaggregated storage

## Key people
